import unittest

from compiler.syntatic.parser import parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = parser
        self.parser.errorok = False

    def test_parse_fibonacci(self):
        fibonacci = """
            /* Compute the Fibonacci of an integer */

            fibo: proc (n int, g int loc);
              dcl h int;
              if n < 0 then
                print(g);
                return;
              else
                h = g; fibo(n-1, h);
                g = h; fibo(n-2, g);
              fi;
              print(n,g);
            end;

            dcl k int = 0;
            fibo(3,k);
            fibo(-1,k);
        """

        ast = self.parser.parse(fibonacci)
        print(ast)

        self.assertEqual(self.parser.errorok, True)
        self.assertEqual(ast, ('PROGRAM', [('STATEMENT', [('DECLARATION_STATEMENT', [('DECLARATION_LIST', [('DECLARATION', [('IDENTIFIER_LIST', [('IDENTIFIER', [], 'k')]), ('MODE', [('DISCRETE_MODE', [], 'int')]), ('INITIALIZATION', [('EXPRESSION', [('INTEGER_LITERAL', [], 0)])])])])])]), ('STATEMENT', [('ACTION_STATEMENT', [('ACTION', [('CALL_ACTION', [('PROCEDURE_CALL', [('PROCEDURE_NAME', [], 'fibo'), ('PARAMETER_LIST', [('PARAMETER', [('EXPRESSION', [('INTEGER_LITERAL', [], 3)])]), ('PARAMETER', [('EXPRESSION', [('LOCATION', [('LOCATION_NAME', [], 'k')])])])])])])])])]), ('STATEMENT', [('ACTION_STATEMENT', [('ACTION', [('CALL_ACTION', [('PROCEDURE_CALL', [('PROCEDURE_NAME', [], 'fibo'), ('PARAMETER_LIST', [('PARAMETER', [('EXPRESSION', [('MINUS_OPERATOR', [('INTEGER_LITERAL', [], 1)])])]), ('PARAMETER', [('EXPRESSION', [('LOCATION', [('LOCATION_NAME', [], 'k')])])])])])])])])])]))


if __name__ == "__main__":
    unittest.main()
