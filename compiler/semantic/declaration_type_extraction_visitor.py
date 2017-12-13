from ..common.context import LyaContext, Type
from ..common.visitor import Visitor


class DeclarationTypeExtractionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

    def visit_discrete_mode(self, node):
        mode_name = node[2]

        mode = self.context.find_mode(mode_name)

        if mode is None:
            raise Exception("Mode {} has not been defined".format(mode_name))

        return Type(mode)

    def visit_mode_name(self, node):
        mode_name = node[2]

        mode = self.context.find_mode(mode_name)

        if mode is None:
            alias = self.context.find_alias(mode_name)

            if alias is None:
                raise Exception("Mode {} has not been defined".format(mode_name))

            mode = alias.mode

        return Type(mode)

    def visit_reference_mode(self, node):
        mode_node = node[1][0]

        mode_type = self.visit(mode_node)

        return Type(mode_type.mode, is_reference=True)

    def visit_parameter_spec_loc(self, node):
        mode_node = node[1][0]

        mode_type = self.visit(mode_node)

        return Type(mode_type.mode, is_reference=True)

    # TODO
    def visit_composite_mode(self, node):
        pass