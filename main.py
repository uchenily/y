#!/usr/bin/env python3
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from visualize_ast import VisualizeAST

debug = False
gen_ast = True


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
    if debug:
        print(tokens)
    parser = Parser(tokens)
    ast = parser.run()
    if gen_ast:
        ast_visitor = VisualizeAST()
        ast_visitor.visit(ast)
        dot = ast_visitor.gendot()
        if debug:
            print(dot)
        with open("astree.dot", "w") as f:
            f.write(dot)

    interpreter = Interpreter()
    interpreter.run(ast)


if __name__ == "__main__":
    main()
