from lexer import Lexer

def main():
    program = None
    with open("hello.y") as fp:
        program = fp.read()

    lexer = Lexer(program)
    tokens = lexer.run()
    print(tokens)

if __name__ == "__main__":
    main()
