from ..common.context import LyaContext, Type, INT_MODE, BOOL_MODE, CHAR_MODE, STRING_MODE, EMPTY_MODE
from ..common.visitor import Visitor


class ExpressionTypeExtractionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

    # Visitors
    def visit_integer_literal(self, node):
        return Type(INT_MODE)

    def visit_bool_literal(self, node):
        return Type(BOOL_MODE)

    def visit_character_literal(self, node):
        return Type(CHAR_MODE)

    def visit_character_string_literal(self, node):
        return Type(STRING_MODE)

    def visit_empty_literal(self, node):
        return Type(EMPTY_MODE)

    # Operators
    # Arithmetic Operators
    def visit_arithmetic_operator(self, node):
        a = node[1][0]
        b = node[1][1]

        a_mode = self.visit(a)
        b_mode = self.visit(b)

        if a_mode != Type(INT_MODE):
            raise Exception("{} should be of mode 'int' on operation {}".format(a, node))

        if b_mode != Type(INT_MODE):
            raise Exception("{} should be of mode 'int' on operation {}".format(b, node))

        return Type(INT_MODE)

    def visit_plus_operator(self, node):
        return self.visit_arithmetic_operator(node)

    def visit_minus_operator(self, node):
        return self.visit_arithmetic_operator(node)

    def visit_times_operator(self, node):
        return self.visit_arithmetic_operator(node)

    def visit_divide_operator(self, node):
        return self.visit_arithmetic_operator(node)

    def visit_modulo_operator(self, node):
        return self.visit_arithmetic_operator(node)

    def visit_monadic_minus_operator(self, node):
        value = node[1][0]

        value_mode = self.visit(value)

        if value_mode != Type(INT_MODE):
            raise Exception("{} should be of mode 'int' on operation {}".format(value, node))

        return Type(INT_MODE)

    # Relational Operators
    def visit_bool_relational_operator(self, node):
        a = node[1][0]
        b = node[1][1]

        a_mode = self.visit(a)
        b_mode = self.visit(b)

        if a_mode != Type(BOOL_MODE):
            raise Exception("{} should be of mode 'bool' on operation {}".format(a, node))

        if b_mode != Type(BOOL_MODE):
            raise Exception("{} should be of mode 'bool' on operation {}".format(b, node))

        return Type(BOOL_MODE)

    def visit_and_operator(self, node):
        return self.visit_bool_relational_operator(node)

    def visit_or_operator(self, node):
        return self.visit_bool_relational_operator(node)

    def visit_monadic_not_operator(self, node):
        value = node[1][0]

        value_mode = self.visit(value)

        if value_mode != Type(BOOL_MODE):
            raise Exception("{} should be of mode 'bool' on operation {}".format(value, node))

        return Type(BOOL_MODE)

    def visit_comparison_operator(self, node):
        a = node[1][0]
        b = node[1][1]

        a_mode = self.visit(a)
        b_mode = self.visit(b)

        if a_mode != b_mode:
            raise Exception("{} and {} are not the same mode".format(a_mode, b_mode))

        return Type(BOOL_MODE)

    def visit_eq_operator(self, node):
        return self.visit_comparison_operator(node)

    def visit_neq_operator(self, node):
        return self.visit_comparison_operator(node)

    def visit_lt_operator(self, node):
        return self.visit_comparison_operator(node)

    def visit_le_operator(self, node):
        return self.visit_comparison_operator(node)

    def visit_gt_operator(self, node):
        return self.visit_comparison_operator(node)

    def visit_ge_operator(self, node):
        return self.visit_comparison_operator(node)

    # Locations
    def visit_location_name(self, node):
        symbol_name = node[2]

        symbol = self.context.find_symbol(symbol_name)

        if symbol is None:
            raise Exception("Symbol {} has not been declared".format(symbol_name))

        return symbol.type

    def visit_procedure_call(self, node):
        procedure_name = node[1][0][2]

        procedure = self.context.find_procedure(procedure_name)

        if procedure is None:
            raise Exception("Procedure {} has not been declared".format(procedure_name))

        return procedure.return_type

    def visit_builtin_call(self, node):
        procedure_name = node[1][0][2]

        procedure = self.context.find_procedure(procedure_name)

        if procedure is None:
            raise Exception("Procedure {} has not been declared".format(procedure_name))

        return procedure.return_type

    # TODO:
    # Visit dereferenced_reference
    # Visit array_element
    # Visit array_slice
    # Visit string_element
    # Visit string_slice
    # Visit referenced_location
