#!/usr/bin/env python3

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from visualize_ast import VisualizeAST


def main():
    program = None
    import sys

    file = "fibonacci.y"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    with open(file) as fp:
        program = fp.read()

    lexer = Lexer(program)
    tokens = lexer.run()
    # print(tokens)
    parser = Parser(tokens)
    ast = parser.run()
    # ast_visitor = VisualizeAST()
    # ast_visitor.visit(ast)
    # dot = ast_visitor.gendot()
    ## print(dot)
    # with open('astree.dot', 'w') as f:
    #    f.write(dot)

    interpreter = Interpreter()
    interpreter.run(ast)


if __name__ == "__main__":
    main()
