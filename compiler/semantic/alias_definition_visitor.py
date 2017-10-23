from ..common.context import LyaContext, Alias
from ..common.visitor import Visitor


class AliasDefinitionVisitor(Visitor):

    def __init__(self, context=LyaContext()):
        self.context = context

    def visit_mode_definition(self, node):
        identifiers = list(map(lambda identifier_node: identifier_node[2], node[1][0][1]))
        mode_name = node[1][1][2]

        mode = self.context.find_mode(mode_name)

        if mode is None:
            alias = self.context.find_alias(mode_name)

            if alias is None:
                raise Exception("Mode {} has not been registered yet".format(mode_name))
            else:
                mode = alias.mode

        for identifier in identifiers:
            if self.context.find_alias(identifier) is None and self.context.find_mode(identifier) is None:
                self.context.register_alias(Alias(identifier, mode))
            else:
                raise Exception("Mode {} already registered".format(identifier))
