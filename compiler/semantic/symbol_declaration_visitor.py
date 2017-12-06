from ..common.context import LyaContext, Symbol
from ..common.visitor import Visitor
from .declaration_type_extraction_visitor import DeclarationTypeExtractionVisitor


class SymbolDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
        self.declaration_type_extractor = DeclarationTypeExtractionVisitor(self.context)

    def visit_declaration(self, node):
        mode_node = node[1][1]
        identifiers = node[1][0][1]

        type = self.declaration_type_extractor.visit(mode_node)

        for identifier in identifiers:
            self.context.register_symbol(Symbol(identifier[2], type))
