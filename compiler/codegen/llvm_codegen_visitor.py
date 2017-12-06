from compiler.common.context import LyaContext, Definition, Type, INT_MODE, BOOL_MODE
from compiler.common.visitor import Visitor
from compiler.semantic.declaration_type_extraction_visitor import DeclarationTypeExtractionVisitor
from compiler.semantic.expression_type_extraction_visitor import ExpressionTypeExtractionVisitor

from llvmlite import ir

i32 = ir.IntType(32)
char = ir.IntType(8)
b = ir.IntType(1)
void = ir.VoidType()
main_function_type = ir.FunctionType(i32, ())


class LLVMCodeGenVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
        self.declaration_type_extractor = DeclarationTypeExtractionVisitor(self.context)
        self.expression_type_extractor = ExpressionTypeExtractionVisitor(self.context)

        self.function_returned = False

        self.module = ir.Module(name=__file__)
        self.main = ir.Function(self.module, main_function_type, name="main")

        self.print_int_function = ir.Function(self.module, ir.FunctionType(void, [i32]), name='print_int')
        self.print_bool_function = ir.Function(self.module, ir.FunctionType(void, [b]), name='print_bool')

        block = self.main.append_basic_block(name="entry")

        self.builder = ir.IRBuilder(block)

    def visit_program(self, node):
        self.visit_children(node)

        ptr = self.builder.alloca(i32, 1, 'test_ptr')
        self.builder.store(i32(10), ptr)

        self.builder.ret(i32(0))

        return self.module

    # Procedure
    def visit_procedure_statement(self, node):
        procedure_name = node[1][0][2]

        procedure = self.context.find_procedure(procedure_name)
        return_type = procedure.return_type.to_llvm()
        parameters = list(map(lambda parameter: parameter.type.to_llvm(), procedure.parameters))

        function_type = ir.FunctionType(return_type, parameters)

        func = ir.Function(self.module, function_type, name=procedure_name)

        bb_entry = func.append_basic_block('entry')

        current_builder = self.builder

        self.builder = ir.IRBuilder(bb_entry)

        for idx, parameter in enumerate(procedure.parameters):
            ptr = self.builder.alloca(parameter.type.to_llvm(), 1, parameter.name)
            self.context.register_definition(Definition(parameter.name, ptr))

            self.builder.store(func.args[idx], ptr)

        self.function_returned = False

        if len(node[1][1][1]) == 3:
            self.visit(node[1][1][1][2])
        else:
            self.visit(node[1][1][1][1])

        if self.function_returned is False:
            self.builder.ret_void()

        self.builder = current_builder

        return func

    # Literals
    def visit_integer_literal(self, node):
        return i32(node[2])

    def visit_boolean_literal(self, node):
        if node[2]:
            return b(1)

        return b(0)

    def visit_character_literal(self, node):
        return node[2]

    def visit_character_string_literal(self, node):
        string_type = ir.ArrayType(char, len(node[2]))
        return string_type(node[2])

    def visit_empty_literal(self, node):
        return None

    # Declaration
    def visit_declaration(self, node):
        identifiers = node[1][0][1]

        for identifier in identifiers:
            symbol = self.context.find_symbol(identifier[2])

            if symbol is None:
                raise "Symbol {} not defined".format(identifier[2])

            ptr = self.builder.alloca(symbol.type.to_llvm(), 1, identifier[2])
            self.context.register_definition(Definition(identifier[2], ptr))

        if len(node[1]) >= 3:
            initialization_node = node[1][2]

            initialization_value = self.visit(initialization_node)

            for identifier in identifiers:
                definition = self.context.find_definition(identifier[2])

                if definition is None:
                    raise "Definition {} not found".format(identifier[2])

                self.builder.store(initialization_value, definition.value)

        return None

    # Location
    def visit_location_name(self, node):
        location_name = node[2]

        location_definition = self.context.find_definition(location_name)

        if location_definition is not None:
            return self.builder.load(location_definition.value)

        return None

    # Assignment
    def visit_assigning_operator(self, node):
        identifier = node[1][0][2]
        expression_node = node[1][1]

        expression_value = self.visit(expression_node)

        definition = self.context.find_definition(identifier)

        if definition is None:
            raise "Definition {} not found".format(identifier)

        self.builder.store(expression_value, definition.value)

        return None

    # Operators
    # Arithmetic Operators
    def visit_binary_operator(self, node, binary_operator):
        a_node = node[1][0]
        b_node = node[1][1]

        a = self.visit(a_node)
        b = self.visit(b_node)

        return binary_operator(a, b)

    # Integer operators
    def visit_plus_operator(self, node):
        return self.visit_binary_operator(node, self.builder.add)

    def visit_minus_operator(self, node):
        return self.visit_binary_operator(node, self.builder.sub)

    def visit_times_operator(self, node):
        return self.visit_binary_operator(node, self.builder.mul)

    def visit_divide_operator(self, node):
        return self.visit_binary_operator(node, self.builder.sdiv)

    def visit_modulo_operator(self, node):
        return self.visit_binary_operator(node, self.builder.srem)

    # Boolean operators
    def visit_and_operator(self, node):
        return self.visit_binary_operator(node, self.builder.and_)

    def visit_or_operator(self, node):
        return self.visit_binary_operator(node, self.builder.or_)

    def visit_not_operator(self, node):
        value_node = node[1][0]

        value = self.visit(value_node)

        return self.builder.not_(value)

    # Comparison operators
    def visit_comparison_operator(self, node, type):
        a_node = node[1][0]
        b_node = node[1][1]

        a = self.visit(a_node)
        b = self.visit(b_node)

        return self.builder.icmp_signed(type, a, b)

    def visit_eq_operator(self, node):
        return self.visit_comparison_operator(node, "==")

    def visit_neq_operator(self, node):
        return self.visit_comparison_operator(node, "!=")

    def visit_lt_operator(self, node):
        return self.visit_comparison_operator(node, "<")

    def visit_le_operator(self, node):
        return self.visit_comparison_operator(node, "<=")

    def visit_gt_operator(self, node):
        return self.visit_comparison_operator(node, ">")

    def visit_ge_operator(self, node):
        return self.visit_comparison_operator(node, ">=")

    # Control flow
    def visit_if(self, node):
        condition_node = node[1][0]
        then_node = node[1][1]

        condition_value = self.visit(condition_node)

        comparison = self.builder.icmp_signed('!=', condition_value, b(0))

        then_bb = self.builder.function.append_basic_block('then')
        else_bb = ir.Block(self.builder.function, 'else')
        fi_bb = ir.Block(self.builder.function, 'fi')

        if len(node[1]) == 3:
            self.builder.cbranch(comparison, then_bb, else_bb)

            self.builder.position_at_start(then_bb)

            self.visit(then_node)

            self.builder.branch(fi_bb)

            else_node = node[1][2]

            self.builder.function.basic_blocks.append(else_bb)
            self.builder.position_at_start(else_bb)

            self.visit(else_node)

            self.builder.branch(fi_bb)
        else:
            self.builder.cbranch(comparison, then_bb, fi_bb)

            self.builder.position_at_start(then_bb)

            self.visit(then_node)

            self.builder.branch(fi_bb)

        self.builder.function.basic_blocks.append(fi_bb)
        self.builder.position_at_start(fi_bb)

    def visit_while(self, node):
        condition_node = node[1][0]
        then_node = node[1][1]

        do_bb = self.builder.function.append_basic_block('do_while')
        od_bb = ir.Block(self.builder.function, 'od')
        then_bb = ir.Block(self.builder.function, 'then')

        self.builder.branch(do_bb)
        self.builder.position_at_start(do_bb)

        condition_value = self.visit(condition_node)

        comparison = self.builder.icmp_signed('!=', condition_value, b(0))

        self.builder.cbranch(comparison, then_bb, od_bb)

        self.builder.function.basic_blocks.append(then_bb)
        self.builder.position_at_start(then_bb)

        self.visit(then_node)

        self.builder.branch(do_bb)

        self.builder.function.basic_blocks.append(od_bb)
        self.builder.position_at_start(od_bb)

    def visit_for(self, node):
        iteration_node = node[1][0]
        then_node = node[1][1]

        if iteration_node[0] == 'STEP_ENUMERATION' or\
                iteration_node[0] == 'STEP_ENUMERATION_DOWN':
            loop_counter = iteration_node[1][0][2]
            start_value_node = iteration_node[1][1]
            end_value_node = iteration_node[1][2] if len(iteration_node[1]) == 3 else iteration_node[1][3]
            step_value_node = iteration_node[1][2] if len(iteration_node[1]) == 4 else ('INTEGER_LITERAL', [], 1)

            if iteration_node[0] == 'STEP_ENUMERATION_DOWN':
                step_value_node = ('MINUS_OPERATOR', [step_value_node])

            loop_declaration_node = \
                ('DECLARATION',
                 [('IDENTIFIER_LIST', [('IDENTIFIER', [], loop_counter)]), ('DISCRETE_MODE', [], 'INT'),
                 start_value_node])

            condition_node = ('NEQ_OPERATOR', [('LOCATION_NAME', [], loop_counter), end_value_node])

            step_node = \
                ('ASSIGNING_OPERATOR',
                 [('LOCATION_NAME', [], loop_counter),
                  ('PLUS_OPERATOR', [('LOCATION_NAME', [], loop_counter), step_value_node])])

            then_node[1].append(step_node)

            while_node = ('WHILE', [condition_node, then_node])

            self.visit(loop_declaration_node)

            self.visit(while_node)
        else:
            raise NotImplementedError()

    def visit_procedure_call(self, node):
        r'''procedure_call : procedure_name LPARENS RPARENS
                                | procedure_name LPARENS parameter_list RPARENS'''

        procedure_name = node[1][0][2]

        func = self.module.globals.get(procedure_name, None)

        args = []
        if len(node[1]) == 2:
            arg_nodes = node[1][1][1]

            args = [self.visit(arg_node) for arg_node in arg_nodes]

        return self.builder.call(func, args, 'call_{}'.format(procedure_name))

    def visit_return_action(self, node):
        self.function_returned = True

        if len(node[1]) > 0:
            self.builder.ret(self.visit(node[1][0]))

    def visit_print(self, node):
        parameters = node[1][0]

        for parameter in parameters[1]:
            parameter_type = self.expression_type_extractor.visit(parameter)
            parameter_value = self.visit(parameter)

            if parameter_type == Type(INT_MODE):
                self.builder.call(self.print_int_function, [parameter_value])
            elif parameter_type == Type(BOOL_MODE):
                self.builder.call(self.print_bool_function, [parameter_value])
