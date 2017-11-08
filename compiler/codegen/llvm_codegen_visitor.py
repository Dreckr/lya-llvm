from compiler.common.context import LyaContext, Definition
from compiler.common.visitor import Visitor

from llvmlite import ir

i32 = ir.IntType(32)
char = ir.IntType(8)
b = ir.IntType(1)
void = ir.VoidType()
main_function_type = ir.FunctionType(i32, ())


class LLVMCodeGenVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

        self.module = ir.Module(name=__file__)
        self.main = ir.Function(self.module, main_function_type, name="main")

        block = self.main.append_basic_block(name="entry")

        self.builder = ir.IRBuilder(block)

    def visit_program(self, node):
        self.visit_children(node)

        a = i32(10)
        b = i32(12)

        result = self.builder.add(a, b, name="res")
        self.builder.ret(result)

        return self.module

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

        if len(node[1]) >= 3:
            initialization_node = node[1][2]

            initialization_value = self.visit(initialization_node)

            for identifier in identifiers:
                self.context.register_definition(Definition(identifier[2], initialization_value))

        return None

    # Location
    def visit_location_name(self, node):
        location_name = node[2]

        location_definition = self.context.find_definition(location_name)

        if location_definition is not None:
            return location_definition.value

        return None

    # Assignment
    def visit_assigning_operator(self, node):
        identifier = node[1][0][2]
        expression_node = node[1][1]

        expression_value = self.visit(expression_node)

        self.context.register_definition(Definition(identifier, expression_value))

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