from typing import List
from typing import Union

import exception
from lexer import Token
from lexer import TokenType


class Node:
    pass


class Identifier(Node):
    def __init__(self, token):
        self.token = token


class Comment(Node):
    def __init__(self, token):
        self.token = token


class Return(Node):
    def __init__(self, expr_node):
        self.expr_node = expr_node


class Expr(Node):
    def __init__(self, expr_node):
        self.expr_node = expr_node


class Conditional(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class If(Node):
    def __init__(self, if_part, elif_parts, else_part):
        self.if_part = if_part
        self.elif_parts = elif_parts
        self.else_part = else_part


class While(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class RangeFor(Node):
    def __init__(self, var: Identifier, iterable, block):
        self.var = var
        self.iterable = iterable
        self.block = block


class For(Node):
    def __init__(self, init, cond, incr, block):
        self.init = init
        self.cond = cond
        self.incr = incr
        self.block = block


class Continue(Node):
    pass


class Break(Node):
    pass


class Assign(Node):
    def __init__(self, left, expr):
        self.left = left
        self.expr = expr


class Program(Node):
    def __init__(self, declarations: List[Node]):
        self.declarations = declarations


class Block(Node):
    def __init__(self, declarations: List[Node]):
        self.declarations = declarations


class VarDecl(Node):
    def __init__(self, var: Identifier, expr_node):
        self.var = var
        self.expr_node = expr_node


class FuncDecl(Node):
    def __init__(self, func: Identifier, params: List[Token], block: Block):
        self.func = func
        self.params = params
        self.block = block


class Or(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Compare(Node):
    def __init__(self, left, right, op_type: str):
        self.left = left
        self.right = right
        self.op_type = op_type


class Add(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Sub(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Mul(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Div(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Mod(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Not(Node):
    def __init__(self, node):
        self.node = node


class Negative(Node):
    def __init__(self, node):
        self.node = node


class ArrayAccess(Node):
    def __init__(self, node: Node, index: Node):
        self.node = node
        self.index = index


class FunctionCall(Node):
    def __init__(self, node, arguments):
        self.func = node
        self.arguments = arguments


class _True(Node):
    pass


class _False(Node):
    pass


class Nil(Node):
    pass


class Number(Node):
    def __init__(self, token):
        self.token = token


class String(Node):
    def __init__(self, token):
        self.token = token


class Array(Node):
    def __init__(self, args):
        self.elements = args


class Parser:
    def __init__(self, token_queue):
        self.token_queue = token_queue
        self.current_token = self.token_queue.get()

    def peek_token(self):
        return self.token_queue.peek()

    def raise_error(self):
        raise exception.ParserError(f"Parser error. token={self.current_token}")

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.token_queue.get()
        else:
            self.raise_error()

    def arguments(self):
        args = [self.expression()]
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            args.append(self.expression())

        return args

    def atom(self):
        if self.current_token.type == TokenType.ID:
            node = Identifier(self.current_token)
            self.eat(TokenType.ID)
            return node
        elif self.current_token.type == TokenType.TRUE:
            node = _True()
            self.eat(TokenType.TRUE)
            return node

        elif self.current_token.type == TokenType.FALSE:
            node = _False()
            self.eat(TokenType.FALSE)
            return node

        elif self.current_token.type == TokenType.NIL:
            node = Nil()
            self.eat(TokenType.NIL)
            return node

        elif self.current_token.type == TokenType.NUMBER:
            node = Number(self.current_token)
            self.eat(TokenType.NUMBER)
            return node

        elif self.current_token.type == TokenType.STRING:
            node = String(self.current_token)
            self.eat(TokenType.STRING)
            return node

    def primary(self):
        if self.current_token.type in (TokenType.L_PAREN, TokenType.L_SQUARE):
            if self.current_token.type == TokenType.L_PAREN:
                self.eat(TokenType.L_PAREN)
                expr = self.expression()
                self.eat(TokenType.R_PAREN)
                return Expr(expr)
            else:
                self.eat(TokenType.L_SQUARE)
                args = self.arguments()
                self.eat(TokenType.R_SQUARE)
                return Array(args)

        node = self.atom()
        while self.current_token.type in (
            TokenType.L_PAREN,
            TokenType.L_SQUARE,
        ):
            if self.current_token.type == TokenType.L_PAREN:
                self.eat(TokenType.L_PAREN)
                args = []
                if self.current_token.type != TokenType.R_PAREN:
                    args = self.arguments()
                self.eat(TokenType.R_PAREN)
                node = FunctionCall(node, args)
            else:
                self.eat(TokenType.L_SQUARE)
                expr = self.expression()
                self.eat(TokenType.R_SQUARE)
                node = ArrayAccess(node, expr)

        return node

    def unary(self):
        node = None
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = Not(self.unary())
        elif self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = Negative(self.unary())
        else:
            node = self.primary()

        return node

    def factor(self):
        left = self.unary()
        while self.current_token.type in (
            TokenType.MUL,
            TokenType.DIV,
            TokenType.MOD,
        ):
            op_type = self.current_token.type
            self.eat(op_type)
            right = self.unary()

            if op_type == TokenType.MUL:
                left = Mul(left, right)
            elif op_type == TokenType.DIV:
                left = Div(left, right)
            else:
                left = Mod(left, right)

        return left

    def term(self):
        left = self.factor()
        while self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            op_type = self.current_token.type
            self.eat(op_type)
            right = self.factor()

            if op_type == TokenType.PLUS:
                left = Add(left, right)
            else:
                left = Sub(left, right)

        return left

    def comparison(self):
        left = self.term()
        while self.current_token.type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op_type = self.current_token.type
            self.eat(op_type)
            right = self.term()

            left = Compare(left, right, op_type.value)

        return left

    def equality(self):
        left = self.comparison()
        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op_type = self.current_token.type
            self.eat(op_type)
            right = self.comparison()

            left = Compare(left, right, op_type.value)

        return left

    def logic_and(self):
        left = self.equality()
        while self.current_token.type == TokenType.AND:
            self.eat(TokenType.AND)
            right = self.equality()
            left = And(left, right)

        return left

    def logic_or(self):
        left = self.logic_and()
        while self.current_token.type == TokenType.OR:
            self.eat(TokenType.OR)
            right = self.logic_and()
            left = Or(left, right)

        return left

    def array_list(self):
        self.eat(TokenType.L_SQUARE)
        args = []
        if self.current_token.type != TokenType.R_SQUARE:
            args = self.arguments()
        self.eat(TokenType.R_SQUARE)

        return Array(args)

    def expression(self):
        if self.current_token.type == TokenType.L_SQUARE:
            return self.array_list()

        left = self.logic_or()
        if self.current_token.type == TokenType.ASSIGN:
            assert isinstance(left, Identifier) or isinstance(left, ArrayAccess)
            self.eat(TokenType.ASSIGN)
            expr = self.expression()
            left = Assign(left, expr)

        return left

    def var_decl(self):
        self.eat(TokenType.VAR)
        id = Identifier(self.current_token)
        self.eat(TokenType.ID)

        expr_node = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            expr_node = self.expression()

        return VarDecl(id, expr_node)

    def parameters(self):
        params = [self.current_token]
        self.eat(TokenType.ID)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            params.append(self.current_token)
            self.eat(TokenType.ID)

        return params

    def block(self):
        declarations = []
        self.eat(TokenType.INDENT)
        while self.current_token.type != TokenType.DEDENT:
            declarations.append(self.declaration())
        self.eat(TokenType.DEDENT)

        return Block(declarations)

    def func_decl(self):
        self.eat(TokenType.FUNCTION)
        func = Identifier(self.current_token)
        self.eat(TokenType.ID)
        self.eat(TokenType.L_PAREN)

        params = []
        if self.current_token.type != TokenType.R_PAREN:
            params = self.parameters()

        self.eat(TokenType.R_PAREN)
        self.eat(TokenType.COLON)
        block_node = self.block()

        return FuncDecl(func, params, block_node)

    def comment(self):
        comment = Comment(self.current_token)
        self.eat(TokenType.COMMENT)
        return comment

    def assign_statement(self):
        id = Identifier(self.current_token)
        self.eat(TokenType.ID)
        if self.current_token.type == TokenType.L_SQUARE:
            self.eat(TokenType.L_SQUARE)
            expr = self.expression()
            self.eat(TokenType.R_SQUARE)
            id = ArrayAccess(id, expr)

        self.eat(TokenType.ASSIGN)
        expr_node = self.expression()
        return Assign(id, expr_node)

    def expr_statement(self):
        expr_stmt = self.expression()
        return expr_stmt

    def return_statement(self):
        self.eat(TokenType.RETURN)
        expr = self.expression()
        if expr is None:
            expr = Nil()

        return Return(expr)

    def if_statement(self):
        self.eat(TokenType.IF)
        if_cond = self.expression()
        self.eat(TokenType.COLON)
        if_block = self.block()

        if_part = Conditional(if_cond, if_block)

        elif_parts = []
        while self.current_token.type == TokenType.ELSEIF:
            self.eat(TokenType.ELSEIF)
            elif_cond = self.expression()
            self.eat(TokenType.COLON)
            elif_block = self.block()

            elif_part = Conditional(elif_cond, elif_block)
            elif_parts.append(elif_part)

        else_part = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)
            else_block = self.block()

            else_part = Conditional(None, else_block)

        return If(if_part, elif_parts, else_part)

    def for_statement(self) -> Union[For, RangeFor]:
        # 类型1: for-range
        # for id in range(expr):
        #     block

        # 类型2:
        # for (init; cond; incr):
        #     block
        self.eat(TokenType.FOR)

        if self.current_token.type == TokenType.ID:
            var = Identifier(self.current_token)
            self.eat(TokenType.ID)
            self.eat(TokenType.IN)
            iterable = self.expression()
            self.eat(TokenType.COLON)
            block = self.block()
            return RangeFor(var, iterable, block)
        else:
            assert self.current_token.type == TokenType.L_PAREN
            self.eat(TokenType.L_PAREN)
            init_decl = self.declaration()
            self.eat(TokenType.SEMICOLON)
            cond_expr = self.expression()
            self.eat(TokenType.SEMICOLON)
            incr_expr = self.expression()
            self.eat(TokenType.R_PAREN)
            self.eat(TokenType.COLON)
            block = self.block()
            return For(init_decl, cond_expr, incr_expr, block)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        cond = self.expression()
        self.eat(TokenType.COLON)
        stmt = self.block()

        return While(cond, stmt)

    def continue_statement(self):
        self.eat(TokenType.CONTINUE)
        return Continue()

    def break_statement(self):
        self.eat(TokenType.BREAK)
        return Break()

    def statement(self):
        if self.current_token.type == TokenType.COMMENT:
            return self.comment()
        elif self.current_token.type == TokenType.ID:
            return self.expr_statement()

        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.for_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            return self.continue_statement()
        elif self.current_token.type == TokenType.BREAK:
            return self.break_statement()
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()

    def declaration(self):
        if self.current_token.type == TokenType.VAR:
            return self.var_decl()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.func_decl()
        else:
            return self.statement()

    def program(self):
        declarations = []
        while self.current_token.type != TokenType.EOF:
            declarations.append(self.declaration())

        return Program(declarations)

    def run(self):
        return self.program()
