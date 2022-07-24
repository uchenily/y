class NodeVisitor():
    def visit(self, node):
        fn_name = "visit_" + node.__class__.__name__
        fn = getattr(self, fn_name, self.visit_Unknown)
        return fn(node)
