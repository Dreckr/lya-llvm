from ..common.context import LyaContext
from ..common.visitor import Visitor

# TODO
class SymbolDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

    def visit_newmode_statement(self, node):
        print(node)
