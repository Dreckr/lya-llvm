import unittest

from compiler.common.context import LyaContext, Type, Symbol, INT_MODE, BOOL_MODE, CHAR_MODE, EMPTY_MODE, STRING_MODE, \
    Procedure
from compiler.semantic.expression_type_extraction_visitor import ExpressionTypeExtractionVisitor


class ExpressionTypeExtractionVisitorTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()
        self.visitor = ExpressionTypeExtractionVisitor(self.context)

    # Literals
    def testIntegerLiteralExtraction(self):
        node = ("INTEGER_LITERAL", [], 10)

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testBoolLiteralExtraction(self):
        node = ("BOOL_LITERAL", [], False)

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testCharacterLiteralExtraction(self):
        node = ("CHARACTER_LITERAL", [], 'a')

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(CHAR_MODE))

    def testEmptyLiteralExtraction(self):
        node = ("EMPTY_LITERAL", [])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(EMPTY_MODE))

    def testCharacterStringLiteralExtraction(self):
        node = ("CHARACTER_STRING_LITERAL", [], "Hello, world!")

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(STRING_MODE))

    # Operators
    # Arithmetic Operators
    def testPlusOperationExtraction(self):
        node = ("PLUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidPlusOperationRaisesException(self):
        node = ("PLUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testMinusOperationExtraction(self):
        node = ("MINUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidMinusOperationRaisesException(self):
        node = ("MINUS_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testTimesOperationExtraction(self):
        node = ("TIMES_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidTimesOperationRaisesException(self):
        node = ("TIMES_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testDivideOperationExtraction(self):
        node = ("DIVIDE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidDivideOperationRaisesException(self):
        node = ("DIVIDE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testModuloOperationExtraction(self):
        node = ("MODULO_OPERATOR", [("INTEGER_LITERAL", [], 10), ("INTEGER_LITERAL", [], 20)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidModuloOperationRaisesException(self):
        node = ("MODULO_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    # Relational Operators
    def testAndOperationExtraction(self):
        node = ("AND_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidAndOperationRaisesException(self):
        node = ("AND_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testOrOperationExtraction(self):
        node = ("OR_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidOrOperationRaisesException(self):
        node = ("OR_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testNotOperationExtraction(self):
        node = ("NOT_OPERATOR", [("BOOL_LITERAL", [], False)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidNotOperationRaisesException(self):
        node = ("NOT_OPERATOR", [("INTEGER_LITERAL", [], 10)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testEqOperationExtraction(self):
        node = ("EQ_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidEqOperationRaisesException(self):
        node = ("EQ_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testNeqOperationExtraction(self):
        node = ("NEQ_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidNeqOperationRaisesException(self):
        node = ("NEQ_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testLtOperationExtraction(self):
        node = ("LT_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidLtOperationRaisesException(self):
        node = ("LT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testLeOperationExtraction(self):
        node = ("LE_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidLeOperationRaisesException(self):
        node = ("LE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testGtOperationExtraction(self):
        node = ("GT_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidGtOperationRaisesException(self):
        node = ("GT_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testGeOperationExtraction(self):
        node = ("GE_OPERATOR", [("BOOL_LITERAL", [], False), ("BOOL_LITERAL", [], True)])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(BOOL_MODE))

    def testInvalidGeOperationRaisesException(self):
        node = ("GE_OPERATOR", [("INTEGER_LITERAL", [], 10), ("BOOL_LITERAL", [], True)])

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    # Location
    def testLocationNameExtraction(self):
        self.context.register_symbol(Symbol("foo", Type(INT_MODE)))
        node = ("LOCATION_NAME", [], "foo")
        
        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidLocationNameRaisesException(self):
        node = ("LOCATION_NAME", [], "foo")

        with self.assertRaises(Exception):
            self.visitor.visit(node)

    def testProcedureCallExtraction(self):
        self.context.register_procedure(Procedure("foo", return_type=Type(INT_MODE)))
        node = ("PROCEDURE_CALL", [("PROCEDURE_NAME", [], "foo")])

        extracted_type = self.visitor.visit(node)

        self.assertEqual(extracted_type, Type(INT_MODE))

    def testInvalidProcedureCallRaisesException(self):
        node = ("PROCEDURE_CALL", [("PROCEDURE_NAME", [], "foo")])

        with self.assertRaises(Exception):
            self.visitor.visit(node)


if __name__ == "__main__":
    unittest.main()
