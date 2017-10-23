class Visitor:

    def visit(self, node):
        method_name = "visit_{}".format(node[0].lower())
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            return self.visit_children(node)

    def visit_children(self, node):
        result = None
        for i in node[1]:
            result = self.visit(i)

        return result
