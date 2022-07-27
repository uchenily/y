from typing import Union
from typing import Optional
from enum import Enum
import codecs

from util import Stack
from visitor import NodeVisitor
from exception import InterpreterError

debug = False


class Function:
    def __init__(self, f_name, f_params, f_block):
        self.name = f_name
        self.params = f_params
        self.block = f_block


class Array:
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return "[" + ",".join([str(e) for e in self.elements]) + "]"

    def __bool__(self):
        return len(self.elements) == 0


class String:
    def __init__(self, value):
        self.value = value[1:-1]

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
        """
        NOTE:
        >>> 1 and 2
        2
        >>> 2 and 1
        1
        >>> True and 3
        3

        return self.left and self.right ==> unexpected result
        """
        return bool(self.left) and bool(self.right)


class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "true" if self.left or self.right else "false"

    def __bool__(self):
        return bool(self.left) or bool(self.right)


class Not:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "false" if self.value else "true"

    def __bool__(self):
        return not self.value


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
        # 将原始字符串转为普通字符串(支持转义)
        if isinstance(arg, String):
            arg = codecs.decode(arg.value, "unicode_escape")
        print(arg, end=" ")
    print()
    return nil


def native_range(args):
    left, right = args[0].value, args[1].value
    return [Number(i) for i in range(left, right)]


builtin_functions = {
    "print": native_print,
    "range": native_range,
    # "len": native_len,
}


class Environment:
    def __init__(self, outer_space: Optional["ActivationRecord"]):
        self.kvs = dict()
        self.outer_space = outer_space

    def __getitem__(self, key):
        if key in self.kvs:
            return self.kvs.get(key)
        if self.outer_space:
            return self.outer_space.environ.__getitem__(key)

    def __setitem__(self, key, value):
        self.kvs[key] = value

    def set(self, key, value):
        if key in self.kvs:
            self.kvs[key] = value
        if self.outer_space:
            self.outer_space.environ.set(key, value)

    def __delitem__(self, key):
        del self.kvs[key]


class ActivationRecord:
    def __init__(self, name, type, nesting_level, outer_space=None):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.environ = Environment(outer_space)

    def __getitem__(self, key):
        return self.environ[key]

    def __setitem__(self, key, value):
        self.environ[key] = value

    def __delitem__(self, key):
        del self.environ[key]

    def get(self, key):
        return self.__getitem__(key)

    def set(self, key, value):
        """
        NOTE: 这里 set 和 __setitem__ 语义并不等同.
        __setitem__: 只会向当前活动记录添加kv对;
        set: 如果当前活动记录不存在key, set会递归查找上层;
        """
        self.environ.set(key, value)

    def __str__(self):
        lines = ["%d: %s %s" % (self.nesting_level, self.type.value, self.name)]
        for k, v in self.environ.kvs.items():
            lines.append(f"    {k:<16}: {v}")
        s = "\n".join(lines)
        return s

    def upper(self):
        return self.environ.outer_space


class ARType(Enum):
    PROGRAM = "program"
    FUNCTION = "function"
    BLOCK = "block"


class Interpreter(NodeVisitor):
    def __init__(self):
        self.current_frame: ActivationRecord
        self.call_stack = Stack()

    def run(self, ast_tree):
        self.visit(ast_tree)

    def visit_Unknown(self, node):
        print("Unknown `%s`" % type(node))

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

            raise InterpreterError("Function `%s` is not defined" % f_name)
        # 将形参 - 实参对存入ActivationRecord中
        for param, arg in zip(f_obj.params, node.arguments):
            new_frame[param] = self.visit(arg)

        self.call_stack.push(new_frame)
        self.current_frame = new_frame

        # 执行函数
        retval = self.visit(f_obj.block)
        assert retval is nil or isinstance(retval, Return)

        if debug:
            print(self.current_frame)

        self.call_stack.pop()
        self.current_frame = self.call_stack.peek()

        if isinstance(retval, Return):
            return retval.value
        return retval

    def visit_Block(self, node) -> Union[Return, Break, Continue, Nil]:
        new_frame = ActivationRecord(
            "<block>",
            ARType.BLOCK,
            self.current_frame.nesting_level + 1,
            self.current_frame,
        )
        self.call_stack.push(new_frame)
        self.current_frame = new_frame
        try:
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

            # block执行结束, 没有遇到return/break/continue
            return nil
        finally:
            self.call_stack.pop()
            self.current_frame = self.call_stack.peek()

    def visit_Number(self, node):
        return Number(node.token.value)

    def visit_Identifier(self, node):
        retval = self.current_frame.get(node.token.value)
        if retval is None:
            raise InterpreterError("Identifier `%s` is not defined" % node.token.value)
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
            raise InterpreterError("Unknown Compare op_type `%s`" % op_type)

    def visit_Return(self, node):
        frame = self.current_frame
        while frame.type != ARType.PROGRAM:
            if frame.type == ARType.FUNCTION:
                return Return(self.visit(node.expr_node))
            frame = frame.upper()

        raise InterpreterError("`return` outside function")

    def visit_Assign(self, node):
        expr = self.visit(node.expr)
        if type(node.left).__name__ == "ArrayAccess":
            arr_name = node.left.node.token.value
            arr_index = self.visit(node.left.index)
            array = self.current_frame[arr_name]
            assert isinstance(array, Array)
            assert isinstance(arr_index, Number)
            assert arr_index.value < len(array.elements)
            array.elements[arr_index.value] = expr
            return

        left_name = node.left.token.value
        if self.current_frame.get(left_name) is None:
            raise InterpreterError("Assign to an unknown variable `%s`" % left_name)
        self.current_frame.set(left_name, expr)

    def visit_And(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return And(left, right)

    def visit_Or(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return Or(left, right)

    def visit_Not(self, node):
        value = self.visit(node.node)
        return Not(value)

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
        var_name = node.var.token.value
        iterable = self.visit(node.iterable)
        for value in iterable:
            try:
                self.current_frame[var_name] = value
                retval = self.visit(node.block)
                if isinstance(retval, Return):
                    return retval.value
                if retval is Break:
                    break
                if retval is Continue:
                    continue
            finally:
                del self.current_frame[var_name]

    def visit_Array(self, node):
        elements = []
        for elem in node.elements:
            elements.append(self.visit(elem))
        return Array(elements)

    def visit_ArrayAccess(self, node):
        arr_name = self.visit(node.node)
        arr_index = self.visit(node.index)
        assert isinstance(arr_index, Number)
        if isinstance(arr_name, Array):
            assert arr_index.value < len(arr_name.elements)
            return arr_name.elements[arr_index.value]

        arr_name = node.node.token.value
        array = self.current_frame[arr_name]
        assert isinstance(array, Array)
        assert arr_index.value < len(array.elements)
        return array.elements[arr_index.value]
