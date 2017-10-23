import unittest

from compiler.syntatic.lexer import lexer


class LexerTest(unittest.TestCase):

    def setUp(self):
        self.lexer = lexer.clone()

    def test_tokenize_fibonacci(self):
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

        self.lexer.input(fibonacci)

        self.assertNextTokenEqual('IDENTIFIER', 'fibo', 4, 68)
        self.assertNextTokenEqual('COLON', ':', 4, 72)
        self.assertNextTokenEqual('PROC', 'proc', 4, 74)
        self.assertNextTokenEqual('LPARENS', '(', 4, 79)
        self.assertNextTokenEqual('IDENTIFIER', 'n', 4, 80)
        self.assertNextTokenEqual('INT', 'int', 4, 82)
        self.assertNextTokenEqual('COMMA', ',', 4, 85)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 4, 87)
        self.assertNextTokenEqual('INT', 'int', 4, 89)
        self.assertNextTokenEqual('LOC', 'loc', 4, 93)
        self.assertNextTokenEqual('RPARENS', ')', 4, 96)
        self.assertNextTokenEqual('SEMICOLON', ';', 4, 97)
        self.assertNextTokenEqual('DCL', 'dcl', 5, 113)
        self.assertNextTokenEqual('IDENTIFIER', 'h', 5, 117)
        self.assertNextTokenEqual('INT', 'int', 5, 119)
        self.assertNextTokenEqual('SEMICOLON', ';', 5, 122)
        self.assertNextTokenEqual('IF', 'if', 6, 138)
        self.assertNextTokenEqual('IDENTIFIER', 'n', 6, 141)
        self.assertNextTokenEqual('LT', '<', 6, 143)
        self.assertNextTokenEqual('NUMBERCONST', 0, 6, 145)
        self.assertNextTokenEqual('THEN', 'then', 6, 147)
        self.assertNextTokenEqual('PRINT', 'print', 7, 168)
        self.assertNextTokenEqual('LPARENS', '(', 7, 173)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 7, 174)
        self.assertNextTokenEqual('RPARENS', ')', 7, 175)
        self.assertNextTokenEqual('SEMICOLON', ';', 7, 176)
        self.assertNextTokenEqual('RETURN', 'return', 8, 194)
        self.assertNextTokenEqual('SEMICOLON', ';', 8, 200)
        self.assertNextTokenEqual('ELSE', 'else', 9, 216)
        self.assertNextTokenEqual('IDENTIFIER', 'h', 10, 237)
        self.assertNextTokenEqual('EQUALS', '=', 10, 239)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 10, 241)
        self.assertNextTokenEqual('SEMICOLON', ';', 10, 242)
        self.assertNextTokenEqual('IDENTIFIER', 'fibo', 10, 244)
        self.assertNextTokenEqual('LPARENS', '(', 10, 248)
        self.assertNextTokenEqual('IDENTIFIER', 'n', 10, 249)
        self.assertNextTokenEqual('MINUS', '-', 10, 250)
        self.assertNextTokenEqual('NUMBERCONST', 1, 10, 251)
        self.assertNextTokenEqual('COMMA', ',', 10, 252)
        self.assertNextTokenEqual('IDENTIFIER', 'h', 10, 254)
        self.assertNextTokenEqual('RPARENS', ')', 10, 255)
        self.assertNextTokenEqual('SEMICOLON', ';', 10, 256)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 11, 274)
        self.assertNextTokenEqual('EQUALS', '=', 11, 276)
        self.assertNextTokenEqual('IDENTIFIER', 'h', 11, 278)
        self.assertNextTokenEqual('SEMICOLON', ';', 11, 279)
        self.assertNextTokenEqual('IDENTIFIER', 'fibo', 11, 281)
        self.assertNextTokenEqual('LPARENS', '(', 11, 285)
        self.assertNextTokenEqual('IDENTIFIER', 'n', 11, 286)
        self.assertNextTokenEqual('MINUS', '-', 11, 287)
        self.assertNextTokenEqual('NUMBERCONST', 2, 11, 288)
        self.assertNextTokenEqual('COMMA', ',', 11, 289)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 11, 291)
        self.assertNextTokenEqual('RPARENS', ')', 11, 292)
        self.assertNextTokenEqual('SEMICOLON', ';', 11, 293)
        self.assertNextTokenEqual('FI', 'fi', 12, 309)
        self.assertNextTokenEqual('SEMICOLON', ';', 12, 311)
        self.assertNextTokenEqual('PRINT', 'print', 13, 327)
        self.assertNextTokenEqual('LPARENS', '(', 13, 332)
        self.assertNextTokenEqual('IDENTIFIER', 'n', 13, 333)
        self.assertNextTokenEqual('COMMA', ',', 13, 334)
        self.assertNextTokenEqual('IDENTIFIER', 'g', 13, 335)
        self.assertNextTokenEqual('RPARENS', ')', 13, 336)
        self.assertNextTokenEqual('SEMICOLON', ';', 13, 337)
        self.assertNextTokenEqual('END', 'end', 14, 351)
        self.assertNextTokenEqual('SEMICOLON', ';', 14, 354)
        self.assertNextTokenEqual('DCL', 'dcl', 16, 381)
        self.assertNextTokenEqual('IDENTIFIER', 'k', 16, 385)
        self.assertNextTokenEqual('INT', 'int', 16, 387)
        self.assertNextTokenEqual('EQUALS', '=', 16, 391)
        self.assertNextTokenEqual('NUMBERCONST', 0, 16, 393)
        self.assertNextTokenEqual('SEMICOLON', ';', 16, 394)
        self.assertNextTokenEqual('IDENTIFIER', 'fibo', 17, 408)
        self.assertNextTokenEqual('LPARENS', '(', 17, 412)
        self.assertNextTokenEqual('NUMBERCONST', 3, 17, 413)
        self.assertNextTokenEqual('COMMA', ',', 17, 414)
        self.assertNextTokenEqual('IDENTIFIER', 'k', 17, 415)
        self.assertNextTokenEqual('RPARENS', ')', 17, 416)
        self.assertNextTokenEqual('SEMICOLON', ';', 17, 417)
        self.assertNextTokenEqual('IDENTIFIER', 'fibo', 18, 431)
        self.assertNextTokenEqual('LPARENS', '(', 18, 435)
        self.assertNextTokenEqual('MINUS', '-', 18, 436)
        self.assertNextTokenEqual('NUMBERCONST', 1, 18, 437)
        self.assertNextTokenEqual('COMMA', ',', 18, 438)
        self.assertNextTokenEqual('IDENTIFIER', 'k', 18, 439)
        self.assertNextTokenEqual('RPARENS', ')', 18, 440)
        self.assertNextTokenEqual('SEMICOLON', ';', 18, 441)

    def assertNextTokenEqual(self, type, value, lineno, lexpos):
        next_token = self.lexer.next()
        self.assertEqual(next_token.type, type)
        self.assertEqual(next_token.value, value)
        self.assertEqual(next_token.lineno, lineno)
        self.assertEqual(next_token.lexpos, lexpos)


if __name__ == "__main__":
    unittest.main()
