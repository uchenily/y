from typing import Union
from enum import Enum

from util import Stack
from visitor import NodeVisitor
from exception import InterpreterError


class Function:
    def __init__(self, f_name, f_params, f_block):
        self.name = f_name
        self.params = f_params
        self.block = f_block


class String:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __bool__(self):
        return len(self.value) == 0


class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return self.value == 0


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "true" if self.left and self.right else "false"

    def __bool__(self):
        return self.left and self.right


class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "true" if self.left or self.right else "false"

    def __bool__(self):
        return self.left or self.right


class Break:
    pass


class Continue:
    pass


class Return:
    def __init__(self, value):
        self.value = value


class _True:
    def __str__(self):
        return "true"


true = _True()


class _False:
    def __str__(self):
        return "false"

    def __bool__(self):
        return False


false = _False()


class Nil:
    def __str__(self):
        return "nil"

    def __bool__(self):
        return False


nil = Nil()


def native_print(args):
    for arg in args:
        print(arg, end=" ")
    print()
    return Nil


builtin_functions = {
    "print": native_print,
    # "len": native_len,
}


class Environment:
    def __init__(self, outer_space: "ActivationRecord"):
        self.kvs = dict()
        self.outer_space = outer_space

    def __getitem__(self, key):
        if key in self.kvs:
            return self.kvs.get(key)
        if self.outer_space:
            return self.outer_space.environ.__getitem__(key)

    def __setitem__(self, key, value):
        self.kvs[key] = value


class ActivationRecord(object):
    def __init__(self, name, type, nesting_level, outer_space=None):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.environ = Environment(outer_space)

    def __getitem__(self, key):
        return self.environ[key]

    def __setitem__(self, key, value):
        self.environ[key] = value

    def get(self, key):
        return self.environ[key]

    def __str__(self):
        lines = ["%d: %s %s" % (self.nesting_level, self.type.value, self.name)]
        for k, v in self.environ.kvs.items():
            lines.append(f"    {k:<16}: {v}")
        s = "\n".join(lines)
        return s


class ARType(Enum):
    PROGRAM = "program"
    FUNCTION = "function"


class Interpreter(NodeVisitor):
    def __init__(self):
        self.current_frame = None
        self.call_stack = Stack()

    def run(self, ast_tree):
        self.visit(ast_tree)

    def visit_Unknown(self, node):
        print("Unknown %s" % type(node))

    def visit_Program(self, node):
        main_frame = ActivationRecord("main", ARType.PROGRAM, nesting_level=1)
        self.call_stack.push(main_frame)
        self.current_frame = main_frame

        for declaration in node.declarations:
            self.visit(declaration)

        self.call_stack.pop()

    def visit_VarDecl(self, node):
        if node.expr_node:
            value = self.visit(node.expr_node)
        else:
            value = nil
        self.current_frame[node.var.token.value] = value

    def visit_FuncDecl(self, node):
        f_name = node.func.token.value
        f_params = [p.value for p in node.params]
        f_block = node.block
        f_obj = Function(f_name, f_params, f_block)
        self.current_frame[f_name] = f_obj

    def visit_String(self, node):
        return String(node.token.value)

    def visit_FunctionCall(self, node):
        f_name = str(node.func.token.value)
        if f_name in builtin_functions:
            args = []
            for arg in node.arguments:
                args.append(self.visit(arg))
            return builtin_functions[f_name](args)

        new_frame = ActivationRecord(
            f_name,
            ARType.FUNCTION,
            self.current_frame.nesting_level + 1,
            self.current_frame,
        )
        f_obj = self.current_frame.get(f_name)
        if f_obj is None:
            while self.call_stack.peek():
                print("-" * 20)
                print(self.call_stack.pop())

            raise InterpreterError("Function %s is not defined" % f_name)
        # 将形参 - 实参对存入ActivationRecord中
        for param, arg in zip(f_obj.params, node.arguments):
            new_frame[param] = self.visit(arg)

        self.call_stack.push(new_frame)
        self.current_frame = new_frame

        # print(self.current_frame)

        # 执行函数
        retval = self.visit(f_obj.block)
        assert isinstance(retval, Return)

        self.call_stack.pop()
        self.current_frame = self.call_stack.peek()

        return retval.value

    def visit_Block(self, node) -> Union[Return, Break, Continue]:
        for declaration in node.declarations:
            retval = self.visit(declaration)
            if isinstance(retval, Return):
                return retval

            """
            当执行到break/continue语句的时候, 应该传递给上层(比如for-block, while-block)
            var a = 1
            while true:                 | block1
                a = a + 1               |
                if a == 10:    | block2 |
                    break      |        |
            """
            if retval is Break:
                return retval

            if retval is Continue:
                return retval

        return Return(nil)

    def visit_Number(self, node):
        return Number(node.token.value)

    def visit_Identifier(self, node):
        retval = self.current_frame.get(node.token.value)
        if retval is None:
            raise InterpreterError("Identifier %s is not defined" % node.token.value)
        return retval

    def visit_Add(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Number(left.value + right.value)

    def visit_Sub(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Number(left.value - right.value)

    def visit_Mul(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Number(left.value * right.value)

    def visit_Div(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Number(left.value / right.value)

    def visit_Mod(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Number(left.value % right.value)

    def visit_If(self, node):
        # if
        if self.visit(node.if_part.condition):
            return self.visit(node.if_part.block)
        # elifs
        for part in node.elif_parts:
            if self.visit(part.condition):
                return self.visit(part.block)
        # else
        if node.else_part:
            return self.visit(node.else_part.block)

    def visit_Expr(self, node):
        return self.visit(node.expr_node)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op_type
        if op_type == "<":
            return left.value < right.value
        elif op_type == "<=":
            return left.value <= right.value
        elif op_type == ">":
            return left.value > right.value
        elif op_type == ">=":
            return left.value >= right.value
        elif op_type == "==":
            return left.value == right.value
        elif op_type == "!=":
            return left.value != right.value
        else:
            raise InterpreterError("Unknown Compare op_type %s" % op_type)

    def visit_Return(self, node):
        if self.current_frame.type != ARType.FUNCTION:
            raise InterpreterError("'return' outside function")
        return Return(self.visit(node.expr_node))

    def visit_Assign(self, node):
        left_name = node.left.token.value
        expr = self.visit(node.expr)
        self.current_frame[left_name] = expr

    def visit_And(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return And(left, right)

    def visit_Or(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Or(left, right)

    def visit__True(self, node):
        return true

    def visit__False(self, node):
        return false

    def visit_Nil(self, node):
        return nil

    def visit_Break(self, node):
        return Break

    def visit_Continue(self, node):
        return Continue

    def visit_While(self, node):
        while self.visit(node.condition):
            retval = self.visit(node.block)
            if isinstance(retval, Return):
                return retval.value
            if retval is Break:
                break
            if retval is Continue:
                continue

    def visit_For(self, node):
        pass
