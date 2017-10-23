import unittest

from compiler.common.context import LyaContext, Symbol, Type, INT_MODE, Mode, CHAR_MODE, Alias
from compiler.semantic.declaration_type_extraction_visitor import DeclarationTypeExtractionVisitor


class DeclarationTypeExtractionVisitorTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()
        self.visitor = DeclarationTypeExtractionVisitor(self.context)

    def testExtractDiscreteType(self):
        result = self.visitor.visit(("DISCRETE_MODE", [], "int"))

        self.assertEqual(result, Type(INT_MODE))

    def testExtractModeType(self):
        self.context.register_mode(Mode("foo"))
        result = self.visitor.visit(("MODE_NAME", [], "foo"))

        self.assertEqual(result, Type(Mode("foo")))

    def testExtractReferenceType(self):
        self.context.register_mode(Mode("foo"))
        result = self.visitor.visit(("REFERENCE_MODE", [("MODE_NAME", [], "foo")]))

        self.assertEqual(result, Type(Mode("foo"), is_reference=True))

    def testExtractAliasType(self):
        self.context.register_alias(Alias("foo", INT_MODE))
        result = self.visitor.visit(("", [("MODE_NAME", [], "foo")]))

        self.assertEqual(result, Type(INT_MODE))


if __name__ == "__main__":
    unittest.main()
