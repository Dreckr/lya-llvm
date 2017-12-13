import operator

from compiler.common.context import LyaContext
from compiler.common.visitor import Visitor


class ConstantLiteralEvaluationVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

    # Literals
    def visit_integer_literal(self, node):
        return node[2]

    def visit_bool_literal(self, node):
        return node[2]

    def visit_character_literal(self, node):
        return node[2]

    def visit_character_string_literal(self, node):
        return node[2]

    def visit_empty_literal(self, node):
        return None

    # Operators
    # Arithmetic Operators
    def visit_arithmetic_operator(self, node, arithmetic_operator):
        a_node = node[1][0]
        b_node = node[1][1]

        a = self.visit(a_node)
        b = self.visit(b_node)

        if not isinstance(a, int):
            raise Exception("{} should be of mode 'int' on operation {}".format(a, node))

        if not isinstance(b, int):
            raise Exception("{} should be of mode 'int' on operation {}".format(b, node))

        return arithmetic_operator(a, b)

    def visit_plus_operator(self, node):
        return self.visit_arithmetic_operator(node, operator.add)

    def visit_minus_operator(self, node):
        return self.visit_arithmetic_operator(node, operator.sub)

    def visit_times_operator(self, node):
        return self.visit_arithmetic_operator(node, operator.mul)

    def visit_divide_operator(self, node):
        return self.visit_arithmetic_operator(node, operator.floordiv)

    def visit_modulo_operator(self, node):
        return self.visit_arithmetic_operator(node, operator.mod)

    def visit_monadic_minus_operator(self, node):
        value_node = node[1][0]

        value = self.visit(value_node)

        if not isinstance(value, int):
            raise Exception("{} should be of mode 'int' on operation {}".format(value, node))

        return -value

    # Relational Operators
    def visit_bool_relational_operator(self, node, relational_operator):
        a_node = node[1][0]
        b_node = node[1][1]

        a = self.visit(a_node)
        b = self.visit(b_node)

        if not isinstance(a, bool):
            raise Exception("{} should be of mode 'bool' on operation {}".format(a, node))

        if not isinstance(b, bool):
            raise Exception("{} should be of mode 'bool' on operation {}".format(b, node))

        return relational_operator(a, b)

    def visit_and_operator(self, node):
        return self.visit_bool_relational_operator(node, operator.and_)

    def visit_or_operator(self, node):
        return self.visit_bool_relational_operator(node, operator.or_)

    def visit_monadic_not_operator(self, node):
        value_node = node[1][0]

        value = self.visit(value_node)

        if not isinstance(value, bool):
            raise Exception("{} should be of mode 'bool' on operation {}".format(value, node))

        return not value

    # Comparison Operators
    def visit_comparison_operator(self, node, comparison_operator):
        a_node = node[1][0]
        b_node = node[1][1]

        a = self.visit(a_node)
        b = self.visit(b_node)

        return comparison_operator(a, b)

    def visit_eq_operator(self, node):
        return self.visit_comparison_operator(node, operator.eq)

    def visit_neq_operator(self, node):
        return self.visit_comparison_operator(node, operator.ne)

    def visit_lt_operator(self, node):
        return self.visit_comparison_operator(node, operator.lt)

    def visit_le_operator(self, node):
        return self.visit_comparison_operator(node, operator.le)

    def visit_gt_operator(self, node):
        return self.visit_comparison_operator(node, operator.gt)

    def visit_ge_operator(self, node):
        return self.visit_comparison_operator(node, operator.ge)