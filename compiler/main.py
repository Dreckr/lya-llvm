from compiler.common.visitor import Visitor
from compiler.semantic.alias_definition_visitor import AliasDefinitionVisitor
from compiler.syntatic.parser import parser, lexer


class ProgramVisitor(Visitor):

    def visit_integer_literal(self, node):
        print(node)


def print_visit(node, depth=list(), final=True):

    if len(depth) > 0:
        for i, is_final in enumerate(depth):
            if i < len(depth):
                if not is_final:
                    print(' |  ', end='')
                else:
                    print('    ', end='')

        print(' |  ')

        for i, is_final in enumerate(depth):
            if i < len(depth):
                if not is_final:
                    print(' |  ', end='')
                else:
                    print('    ', end='')

        if final:
            print(' └─ ', end='')
        else:
            print(' ├─ ', end='')

    if len(node) == 2:
        print('{0}'.format(node[0]))
    else:
        print('{0} ({1})'.format(node[0], node[2]))

    depth.append(final)

    for i, child in enumerate(node[1]):
        print_visit(
            child,
            depth,
            i == len(node[1]) - 1)

    depth.pop()

if __name__ == '__main__':
    s = '''
            /* Compute the Fibonacci of an integer */

            foo: proc() returns(int); foo(); end;
            foo(10);
    '''

    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input

        print(tok)

    result = parser.parse(s)

    print_visit(result)

    visitor = AliasDefinitionVisitor()
    visitor.visit(result)

