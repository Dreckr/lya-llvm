from compiler.common.context import LyaContext
from compiler.common.visitor import Visitor


class LLVMCodeGenVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
