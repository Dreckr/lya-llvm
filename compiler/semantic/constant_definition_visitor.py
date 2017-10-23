from .expression_type_extraction_visitor import ExpressionTypeExtractionVisitor
from .constant_literal_evaluation_visitor import ConstantLiteralEvaluationVisitor
from ..common.context import LyaContext, Constant, Symbol
from ..common.visitor import Visitor

# TODO
class ConstantDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
        self.evaluator = ConstantLiteralEvaluationVisitor(context)
        self.expression_type_extractor = ExpressionTypeExtractionVisitor(context)

    def visit_synonym_definition(self, node):
        identifiers = node[1][0]
        mode = None


        if len(node[1]) == 3:
            expression = node[1][2]

            value = expression # integer literal
        else:
            expression = node[1][1]

        expression_type = self.expression_type_extractor.visit(expression)
        value = self.evaluator.visit(expression)

        for identifier in identifiers[1]:
            self.context.register_constant(Constant(Symbol(identifier[2], expression_type), value))



