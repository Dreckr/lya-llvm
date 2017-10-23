import unittest

from compiler.common.context import LyaContext, Symbol, Type, INT_MODE, Mode, CHAR_MODE, Alias
from compiler.semantic.procedure_definition_visitor import ProcedureDefinitionVisitor
from compiler.syntatic.parser import parser


class ProcedureDefinitionVisitorTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()
        self.visitor = ProcedureDefinitionVisitor(self.context)

    def testNoParameterNoReturnProcedure(self):
        s = '''
            foo: proc(); println("Hello, world!"); end;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        procedure = self.context.find_procedure("foo")
        self.assertIsNotNone(procedure)
        self.assertEqual(procedure.name, "foo")
        self.assertEqual(procedure.return_type, None)
        self.assertListEqual(procedure.parameters, list())

    def testOneDiscreteModeParameterNoReturnProcedure(self):
        s = '''
            foo: proc(a int); println(a); end;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        procedure = self.context.find_procedure("foo")
        self.assertIsNotNone(procedure)
        self.assertEqual(procedure.name, "foo")
        self.assertEqual(procedure.return_type, None)
        self.assertSequenceEqual(procedure.parameters, [Symbol("a", Type(INT_MODE))])

    def testOneModeParameterNoReturnProcedure(self):
        s = '''
            foo: proc(a bar); println(a); end;
        '''
        result = parser.parse(s)

        self.context.register_mode(Mode("bar"))

        self.visitor.visit(result)

        procedure = self.context.find_procedure("foo")
        self.assertIsNotNone(procedure)
        self.assertEqual(procedure.name, "foo")
        self.assertEqual(procedure.return_type, None)
        self.assertSequenceEqual(procedure.parameters, [Symbol("a", Type(Mode("bar")))])

    def testNoParameterIntReturnProcedure(self):
        s = '''
            foo: proc() returns(int); println("Hello, world!"); end;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        procedure = self.context.find_procedure("foo")
        self.assertIsNotNone(procedure)
        self.assertEqual(procedure.name, "foo")
        self.assertEqual(procedure.return_type, Type(INT_MODE))
        self.assertListEqual(procedure.parameters, list())

    def testOneRefModeParameterNoReturnProcedure(self):
        s = '''
            foo: proc(a ref bar); println(a); end;
        '''
        result = parser.parse(s)

        self.context.register_alias(Alias("bar", INT_MODE))

        self.visitor.visit(result)

        procedure = self.context.find_procedure("foo")
        self.assertIsNotNone(procedure)
        self.assertEqual(procedure.name, "foo")
        self.assertEqual(procedure.return_type, None)
        self.assertSequenceEqual(procedure.parameters, [Symbol("a", Type(INT_MODE, is_reference=True))])

if __name__ == "__main__":
    unittest.main()
