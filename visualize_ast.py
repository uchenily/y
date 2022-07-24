import textwrap

from parser import ArrayAccess, Identifier, Parser
from visitor import NodeVisitor


class VisualizeAST(NodeVisitor):
    def __init__(self):
        self.count = 0
        self.dot_header = [
            textwrap.dedent(
                """digraph astgraph {
          node [fontsize=12, fontname="Courier", height=.1];
          # ranksep=.3;
          # edge [arrowsize=.5]

        """
            )
        ]
        self.dot_body = []
        self.dot_footer = ["}"]

    def gendot(self):
        return "".join(self.dot_header + self.dot_body + self.dot_footer)

    def visit_Program(self, node):
        s = '  node%d [label="%s"]\n' % (self.count, type(node).__name__)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for decl in node.declarations:
            self.visit(decl)
            s = "  node%d -> node%d\n" % (node._num, decl._num)
            self.dot_body.append(s)

    def visit_FuncDecl(self, node):
        s = '  node%d [label="Func %s"]\n' % (self.count, node.func.token.value)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        param_count = self.count
        self.count += 1
        s = '  node%d [label="Params\n%s"]\n' % (
            param_count,
            ",".join([v.value for v in node.params]),
        )
        self.dot_body.append(s)
        s = "  node%d -> node%d\n" % (node._num, param_count)
        self.dot_body.append(s)

        # for child in (node.params, node.block):
        for child in (node.block,):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Block(self, node):
        s = '  node%d [label="Block"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for decl in node.declarations:
            self.visit(decl)
            s = "  node%d -> node%d\n" % (node._num, decl._num)
            self.dot_body.append(s)

    def visit_FunctionCall(self, node):
        if isinstance(node.func, Identifier):
            fname = node.func.token.value
        else:
            assert isinstance(node.func, ArrayAccess)
            fname = (
                node.func.node.token.value
                + "["
                + str(node.func.index.token.value)
                + "]"
            )
        args = []
        for arg in node.arguments:
            if isinstance(arg, ArrayAccess):
                args.append(
                    str(arg.node.token.value)
                    + "["
                    + str(arg.index.token.value)
                    + "]"
                )
            else:
                args.append(str(arg.token.value).replace('"', ""))

        args = ",".join(args)
        s = '  node%d [label="%s(%s)"]\n' % (self.count, fname, args)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        # for arg in node.arguments:
        #    self.visit(arg)
        #    s = '  node%d -> node%d\n' % (node._num, arg._num)
        #    self.dot_body.append(s)

    def visit_VarDecl(self, node):
        s = '  node%d [label="Var %s"]\n' % (self.count, node.var.token.value)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        self.visit(node.expr_node)
        s = "  node%d -> node%d\n" % (node._num, node.expr_node._num)
        self.dot_body.append(s)

    def visit_Add(self, node):
        s = '  node%d [label="+"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.left, node.right):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Sub(self, node):
        s = '  node%d [label="-"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.left, node.right):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Comment(self, node):
        limit = node.token.value.replace('"', "")
        if len(limit) > 12:
            limit = limit[:12] + "..."
        s = '  node%d [label="Comment\n%s"]\n' % (self.count, limit)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_Return(self, node):
        s = '  node%d [label="Return"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        self.visit(node.expr_node)
        s = "  node%d -> node%d\n" % (node._num, node.expr_node._num)
        self.dot_body.append(s)

    def visit_Expr(self, node):
        s = '  node%d [label="%s"]\n' % (self.count, node)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        # self.visit(node.left)
        # self.visit(node.expr)

        for child in (node.expr_node,):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Number(self, node):
        s = '  node%d [label="%s"]\n' % (self.count, node.token.value)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_Identifier(self, node):
        s = '  node%d [label="%s"]\n' % (self.count, node.token.value)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_String(self, node):
        s = '  node%d [label="String\n%s"]\n' % (
            self.count,
            node.token.value.replace('"', ""),
        )
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_Array(self, node):
        s = '  node%d [label="Array\n%s"]\n' % (
            self.count,
            [str(v.token.value).replace('"', "") for v in node.elements],
        )
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_ArrayAccess(self, node):
        if isinstance(node.node, Identifier):
            s = '  node%d [label="ArrayAccess\n%s[%d]"]\n' % (
                self.count,
                node.node.token.value,
                node.index.token.value,
            )
        else:
            s = '  node%d [label="ArrayAccess\n%s()[%d]"]\n' % (
                self.count,
                type(node.node).__name__,
                node.index.token.value,
            )
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_Assign(self, node):
        if isinstance(node.left, ArrayAccess):
            s = '  node%d [label="Assign\n%s[%s]"]\n' % (
                self.count,
                node.left.node.token.value,
                node.left.index.token.value,
            )
        else:
            s = '  node%d [label="Assign\n%s"]\n' % (
                self.count,
                node.left.token.value,
            )
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        self.visit(node.expr)
        s = "  node%d -> node%d\n" % (node._num, node.expr._num)
        self.dot_body.append(s)

    def visit__True(self, node):
        s = '  node%d [label="True"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit__False(self, node):
        s = '  node%d [label="False"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_And(self, node):
        s = '  node%d [label="And"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.left, node.right):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Or(self, node):
        s = '  node%d [label="Or"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.left, node.right):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Not(self, node):
        s = '  node%d [label="Not"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        self.visit(node.node)
        print("node._num", node._num, " -> ", node.node._num)
        s = "  node%d -> node%d\n" % (node._num, node.node._num)
        self.dot_body.append(s)

    def visit_Conditional(self, node):
        s = '  node%d [label="Cond"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.condition, node.block):
            if child is None:
                continue

            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_If(self, node):
        s = '  node%d [label="If"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.if_part, node.elif_parts, node.else_part):
            if not child:
                continue

            if isinstance(child, list):
                elif_blocks_count = self.count
                self.count += 1
                s = '  node%d [label="[else if]"]\n' % elif_blocks_count
                self.dot_body.append(s)
                s = "  node%d -> node%d\n" % (node._num, elif_blocks_count)
                self.dot_body.append(s)

                for elif_block in child:
                    self.visit(elif_block)
                    s = "  node%d -> node%d\n" % (
                        elif_blocks_count,
                        elif_block._num,
                    )
                    self.dot_body.append(s)
            else:
                self.visit(child)
                s = "  node%d -> node%d\n" % (node._num, child._num)
                self.dot_body.append(s)

    def visit_Compare(self, node):
        s = '  node%d [label="Compare\n%s"]\n' % (self.count, node.op_type)
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.left, node.right):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_While(self, node):
        s = '  node%d [label="While"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.condition, node.block):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Break(self, node):
        s = '  node%d [label="Break"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_Continue(self, node):
        s = '  node%d [label="Continue"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

    def visit_For(self, node):
        s = '  node%d [label="For"]\n' % self.count
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1

        for child in (node.var, node.iterable, node.block):
            self.visit(child)
            s = "  node%d -> node%d\n" % (node._num, child._num)
            self.dot_body.append(s)

    def visit_Unknown(self, node):
        s = '  node%d [label="Unknown %s"]\n' % (self.count, type(node))
        self.dot_body.append(s)
        node._num = self.count
        self.count += 1
