from .declaration_type_extraction_visitor import DeclarationTypeExtractionVisitor
from ..common.context import LyaContext, Symbol, Scope, Procedure
from ..common.visitor import Visitor


class ProcedureDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context
        self.type_extraction_visitor = DeclarationTypeExtractionVisitor(context)

    def visit_procedure_statement(self, node):
        procedure_name = node[1][0][2]
        procedure_definition = node[1][1]

        procedure_scope = Scope("procedure_{}".format(procedure_name), self.context.current_scope)
        self.context.register_scope(procedure_scope)

        self.context.enter_scope(procedure_scope.name)

        parameter_list = procedure_definition[1][0]
        parameters = list()

        for i in parameter_list[1]:
            parameter_type = self.type_extraction_visitor.visit(i[1][1])

            for j in i[1][0][1]:
                parameter = Symbol(j[2], parameter_type)

                self.context.register_symbol(parameter)
                parameters.append(parameter)

        return_type = None
        if len(procedure_definition[1]) == 3:
            result_spec = procedure_definition[1][1]

            return_type = self.type_extraction_visitor.visit(result_spec)

        self.context.enter_scope(procedure_scope.parent.name)

        self.context.register_procedure(Procedure(procedure_name, parameters, return_type))
