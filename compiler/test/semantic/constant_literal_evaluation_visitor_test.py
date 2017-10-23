import unittest

from compiler.common.context import LyaContext
from compiler.semantic.constant_literal_evaluation_visitor import ConstantLiteralEvaluationVisitor


class ConstantLiteralEvaluationVisitorTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()
        self.visitor = ConstantLiteralEvaluationVisitor(self.context)

    def testIntegerLiteral(self):
        self.assertEqual(self.visitor.visit(("INTEGER_LITERAL", [], 10)), 10)

    def testBooleanLiteral(self):
        self.assertEqual(self.visitor.visit(("BOOL_LITERAL", [], True)), True)

    def testCharLiteral(self):
        self.assertEqual(self.visitor.visit(("CHARACTER_LITERAL", [], 'a')), 'a')

    def testStringLiteral(self):
        self.assertEqual(self.visitor.visit(("CHARACTER_STRING_LITERAL", [], "Hello, world!")), "Hello, world!")

    def testEmptyLiteral(self):
        self.assertEqual(self.visitor.visit(("EMPTY_LITERAL", [])), None)

    def testSumExpression(self):
        node = ("PLUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), 30)

    def testSubstractionExpression(self):
        node = ("MINUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), -10)

    def testMultiplicationExpression(self):
        node = ("TIMES_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), 200)

    def testDivisionExpression(self):
        node = ("DIVIDE_OPERATOR", [("INTEGER_LITERAL", [], 100), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), 5)

    def testModuloExpression(self):
        node = ("MODULO_OPERATOR", [("INTEGER_LITERAL", [], 100), ("INTEGER_LITERAL", [], 21)])
        self.assertEqual(self.visitor.visit(node), 16)

    def testAndExpression(self):
        node = ("AND_OPERATOR", [("BOOL_LITERAL", [], True), ("BOOL_LITERAL", [], True)])
        self.assertEqual(self.visitor.visit(node), True)

    def testOrExpression(self):
        node = ("OR_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])
        self.assertEqual(self.visitor.visit(node), True)

    def testNotExpression(self):
        node = ("NOT_OPERATOR", [("BOOL_LITERAL", [], False)])
        self.assertEqual(self.visitor.visit(node), True)

    def testEqualityExpression(self):
        node = ("EQ_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

        node = ("EQ_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

    def testInequalityExpression(self):
        node = ("NEQ_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

        node = ("NEQ_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

    def testGreaterThanExpression(self):
        node = ("GT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

        node = ("GT_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

        node = ("GT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), False)

    def testGreaterThanOrEqualExpression(self):
        node = ("GE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

        node = ("GE_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

        node = ("GE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), False)

    def testLessThanExpression(self):
        node = ("LT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

        node = ("LT_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

        node = ("LT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), True)

    def testLessThanOrEqualExpression(self):
        node = ("LE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), True)

        node = ("LE_OPERATOR", [("INTEGER_LITERAL", [], 20), ("INTEGER_LITERAL", [], 10)])
        self.assertEqual(self.visitor.visit(node), False)

        node = ("LE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])
        self.assertEqual(self.visitor.visit(node), True)


if __name__ == "__main__":
    unittest.main()
