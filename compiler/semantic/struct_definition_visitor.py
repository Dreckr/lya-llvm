from ..common.context import LyaContext
from ..common.visitor import Visitor

# TODO
class StructDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
