from util import Queue
from enum import Enum
import exception

class TokenType(Enum):
    ID = "identifier"
    NUMBER = "number"
    STRING = "string"
    COMMENT = "comment"
    INDENT = "indent"

    L_PAREN = "("
    R_PAREN = ")"
    L_SQUARE = "["
    R_SQUARE = "]"
    L_CURLY = "{"
    R_CURLY = "}"
    COMMA = ","
    COLON = ":"

    LESS = "<"
    GREATER = ">"
    NOT = "!"
    ASSIGN = "="
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "=="
    NOT_EQUAL = "!="

    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"

    # keywords
    VAR = "var"
    FUNCTION = "func"
    IF = "if"
    ELSE = "else"
    ELSEIF = "elif"
    WHILTE = "while"
    RETURN = "return"
    FOR = "for"
    CONTINUE = "continue"
    BREAK = "break"
    AND = "and"
    OR = "or"
    TRUE = "true"
    FALSE = "false"
    NIL = "nil"

    EOF = "EOF"

    def __str__(self):
        return self.name

def _build_keywords():
    token_list = list(TokenType)
    start = token_list.index(TokenType.VAR)
    end = token_list.index(TokenType.EOF)
    res = {}
    for i in range(start, end):
        res[token_list[i].value] = token_list[i]

    return res


keyword_dict = _build_keywords()


class Token(object):
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return (f"Token(type={self.type}, value='{self.value}')")


class Lexer():
    """Lexical analyzer"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.token_queue = Queue()

    @property
    def current_char(self):
        return self.text[self.pos]

    def peek(self, pos=1):
        peek_pos = self.pos + pos
        if peek_pos < 0 or peek_pos >= len(self.text):
            return None

        return self.text[peek_pos]

    def advance(self, step=1):
        self.pos += step

    def get_indent(self):
        chars = [' ']
        while self.pos < len(self.text) and self.current_char == ' ':
            chars.append(' ')
            self.advance()

        res = ''.join(chars)
        return res

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.current_char.isspace():
            self.advance()

    def get_string(self):
        chars = ['"']
        self.advance()
        while self.pos < len(self.text) and self.current_char != '"':
            chars.append(self.current_char)
            self.advance()

        chars.append('"')
        self.advance()

        self.advance()
        res = ''.join(chars)
        return res

    def get_number(self):
        chars = []
        while self.pos < len(self.text) and self.current_char.isdigit():
            chars.append(self.current_char)
            self.advance()

        if self.current_char == ".":
            chars.append(".")
            self.advance()

            while self.pos < len(self.text) and self.current_char.isdigit():
                chars.append(self.current_char)
                self.advance()

            self.advance()
            res = float("".join(chars))
            return res

        self.advance()
        res = int("".join(chars))
        return res

    def get_id(self):
        chars = []
        while self.pos < len(self.text) and (
            self.current_char.isalnum() or self.current_char == '_'):
            chars.append(self.current_char)
            self.advance()

        self.advance()
        res = "".join(chars)
        return res

    def get_comment(self):
        line = []
        while self.pos < len(self.text) and self.current_char != '\n':
            line.append(self.current_char)
            self.advance()

        self.advance()
        res = "".join(line)
        return res

    def raise_error(self):
        raise exception.LexerError(f"Lexer error. '{self.current_char}'")

    def run(self):
        """执行结束返回token列表"""
        while self.pos < len(self.text):
            # indent
            if self.current_char == ' ' and self.peek(-1) == '\n' \
                and self.peek(-2) == ':':
                value = self.get_indent()
                token = Token(TokenType.INDENT, value)

            # skip whitespace
            elif self.current_char.isspace():
                self.skip_whitespace()

            # comment
            elif self.current_char == '#':
                value = self.get_comment()
                token = Token(TokenType.COMMENT, value)
                self.token_queue.put(token)

            # string
            elif self.current_char == '"':
                value = self.get_string()
                token = Token(TokenType.STRING, value)
                self.token_queue.put(token)

            # number
            elif self.current_char.isdigit():
                value = self.get_number()
                token = Token(TokenType.NUMBER, value)
                self.token_queue.put(token)

            # two-character tokens
            elif self.current_char == '<' and self.peek() == '=':
                token = Token(TokenType.LESS_EQUAL, "<=")
                self.token_queue.put(token)
                self.advance(2)

            elif self.current_char == '>' and self.peek() == '=':
                token = Token(TokenType.GREATER_EQUAL, ">=")
                self.token_queue.put(token)
                self.advance(2)

            elif self.current_char == '!' and self.peek() == '=':
                token = Token(TokenType.NOT_EQUAL, "!=")
                self.token_queue.put(token)
                self.advance(2)

            elif self.current_char == '=' and self.peek() == '=':
                token = Token(TokenType.EQUAL, "==")
                self.token_queue.put(token)
                self.advance(2)

            # single character tokens
            elif self.current_char == '+':
                token = Token(TokenType.PLUS, '+')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '-':
                token = Token(TokenType.MINUS, '-')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '*':
                token = Token(TokenType.MUL, '*')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '/':
                token = Token(TokenType.DIV, '/')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '%':
                token = Token(TokenType.MOD, '%')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '(':
                token = Token(TokenType.L_PAREN, '(')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == ')':
                token = Token(TokenType.R_PAREN, ')')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '[':
                token = Token(TokenType.L_SQUARE, '[')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == ']':
                token = Token(TokenType.R_SQUARE, ']')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '{':
                token = Token(TokenType.L_CURLY, '{')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '}':
                token = Token(TokenType.R_CURLY, '}')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '<':
                token = Token(TokenType.LESS, '<')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '>':
                token = Token(TokenType.GREATER, '>')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '=':
                token = Token(TokenType.ASSIGN, '=')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == '!':
                token = Token(TokenType.NOT, '!')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == ',':
                token = Token(TokenType.COMMA, ',')
                self.token_queue.put(token)
                self.advance()

            elif self.current_char == ':':
                token = Token(TokenType.COLON, ':')
                self.token_queue.put(token)
                self.advance()

            # identifier
            elif self.current_char.isalpha() or self.current_char == '_':
                id = self.get_id()
                if id in keyword_dict:
                    token = Token(keyword_dict[id], id)
                else:
                    token = Token(TokenType.ID, id)

                self.token_queue.put(token)

            else:
                self.raise_error()

        token = Token(TokenType.EOF, "EOF")
        self.token_queue.put(token)

        return self.token_queue
