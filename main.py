from lexer import Lexer
from parser import Parser
from visualize_ast import VisualizeAST

def main():
    program = None
    with open("hello.y") as fp:
        program = fp.read()

    lexer = Lexer(program)
    tokens = lexer.run()
    print(tokens)
    parser = Parser(tokens)
    ast = parser.run()
    ast_visitor = VisualizeAST()
    ast_visitor.visit(ast)
    dot = ast_visitor.gendot()
    print(dot)
    with open('astree.dot', 'w') as f:
        f.write(dot)


if __name__ == "__main__":
    main()
