'''
Lexer module for the Lya language
'''
import ply.lex as lex

class LyaLexer:
    'Lexer for the Lya language'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, s):
        self.lexer.input(s)

    def token(self):
        return self.lexer.token()

    # // Reserved words
    reserved = {
        'array': 'ARRAY',
        'by': 'BY',
        'chars': 'CHARS',
        'dcl': 'DCL',
        'do': 'DO',
        'down': 'DOWN',
        'else': 'ELSE',
        'elseif': 'ELSIF',
        'end': 'END',
        'exit': 'EXIT',
        'fi': 'FI',
        'for': 'FOR',
        'if': 'IF',
        'in': 'IN',
        'loc': 'LOC',
        'type': 'TYPE',
        'od': 'OD',
        'proc': 'PROC',
        'ref': 'REF',
        'result': 'RESULT',
        'return': 'RETURN',
        'returns': 'RETURNS',
        'syn': 'SYN',
        'then': 'THEN',
        'to': 'TO',
        'while': 'WHILE',
        'bool': 'BOOL',
        'char': 'CHAR',
        'false': 'FALSE',
        'int': 'INT',
        'length': 'LENGTH',
        'lower': 'LOWER',
        'null': 'NULL',
        'num': 'NUM',
        'pred': 'PRED',
        'print': 'PRINT',
        'read': 'READ',
        'succ': 'SUCC',
        'true': 'TRUE',
        'upper': 'UPPER',
        'assert': 'ASSERT',
        'new': 'NEW',
        'free': 'FREE',
    }

    tokens = [
        'NUMBERCONST',
        'CHARCONST',
        'STRINGCONST',
        'COMMA',
        'COLON',
        'SEMICOLON',
        'UNDERSCORE',
        'EQUALS',
        'LPARENS',
        'RPARENS',
        'LBRACKET',
        'RBRACKET',
        'ARROW',
        'STRINGCONCAT',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULO',
        'AND',
        'OR',
        'NOT',
        'EQ',
        'NEQ',
        'LT',
        'LE',
        'GT',
        'GE',
        'IDENTIFIER'
    ] + list(reserved.values())

    def t_NUMBERCONST(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CHARCONST(self, t):
        r'\'.\''
        t.value = t.value[1:-1]
        return t

    def t_STRINGCONST(self, t):
        r'".+"'
        t.value = t.value[1:-1]
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    t_COMMA = r','
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_UNDERSCORE = r'_'
    t_EQUALS = r'='
    t_LPARENS = r'\('
    t_RPARENS = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'

    t_ARROW = r'->'
    t_STRINGCONCAT = r'&'

    # // Arithmetic operators
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'

    # // Relational operators
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    t_ignore_COMMENT = r'(/\*[^\n]*\*/)|(//[^\n]*)'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
