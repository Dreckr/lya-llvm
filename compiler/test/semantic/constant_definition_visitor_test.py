import unittest

from compiler.syntatic.parser import parser
from compiler.semantic.constant_definition_visitor import ConstantDefinitionVisitor


class ConstantDefinitionVisitorTest(unittest.TestCase):

    def setUp(self):
        self.visitor = ConstantDefinitionVisitor()

    def testIntegerConstantExtraction(self):
        s = '''
            syn a int = 10;
        '''
        result = parser.parse(s)
        self.visitor.visit(result)

        print(self.visitor)


if __name__ == "__main__":
    unittest.main()
