#!/usr/bin/env python3
import argparse

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser
from visualize_ast import VisualizeAST


def main():
    arg_parser = argparse.ArgumentParser(prog="y-interpreter")
    arg_parser.add_argument("file", help="要执行的y脚本文件")
    arg_parser.add_argument("--debug", action="store_true", help="开启调试")
    arg_parser.add_argument("--ast", action="store_true", help="生成AST")
    arg_parser.add_argument("--ast-file", help="生成AST文件名", default="astree.dot")
    args = arg_parser.parse_args()
    with open(args.file) as fp:
        program = fp.read()

    lexer = Lexer(program)
    tokens = lexer.run()
    if args.debug:
        print(tokens)

    parser = Parser(tokens)
    ast = parser.run()
    if args.ast:
        ast_visitor = VisualizeAST()
        ast_visitor.visit(ast)
        dot = ast_visitor.gendot()
        if args.debug:
            print(dot)
        with open(args.ast_file, "w") as f:
            f.write(dot)

    interpreter = Interpreter()
    interpreter.run(ast)


if __name__ == "__main__":
    main()
