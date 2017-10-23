import unittest

from compiler.common.context import LyaContext
from compiler.syntatic.parser import parser
from compiler.semantic.alias_definition_visitor import AliasDefinitionVisitor


class AliasDefinitionVisitorTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()
        self.visitor = AliasDefinitionVisitor(self.context)

    def testSingleAliasExtraction(self):
        s = '''
            type a = int;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        alias = self.context.find_alias("a")
        self.assertIsNotNone(alias)
        self.assertEqual(alias.mode.name, "int")

    def testMultipleAliasExtraction(self):
        s = '''
            type a, b = int;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        alias = self.context.find_alias("a")
        self.assertIsNotNone(alias)
        self.assertEqual(alias.mode.name, "int")

        alias = self.context.find_alias("b")
        self.assertIsNotNone(alias)
        self.assertEqual(alias.mode.name, "int")

    def testInvalidAliasModeRaisesException(self):
        s = '''
            type a = foo;
        '''
        result = parser.parse(s)

        with self.assertRaises(Exception):
            self.visitor.visit(result)

    def testInvalidAliasIdentifierRaisesException(self):
        s = '''
            type a = int;
            type a = bool;
        '''
        result = parser.parse(s)

        with self.assertRaises(Exception):
            self.visitor.visit(result)

if __name__ == "__main__":
    unittest.main()
