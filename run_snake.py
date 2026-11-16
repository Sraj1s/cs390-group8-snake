import sys

from lexer import Lexer
from parser import Parser
from expression_parser import ParseError
from interpreter import Interpreter
from runtime_errors import SnakeRuntimeError


def run_source(source):
    # source code -> tokens -> syntax tree -> execution
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    Interpreter().run(program.statements)


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_snake.py <program.snake>", file=sys.stderr)
        return 1

    try:
        with open(sys.argv[1], encoding="utf-8") as file:
            source = file.read()
    except OSError as error:
        print(f"Could not read file: {error}", file=sys.stderr)
        return 1

    try:
        run_source(source)
    except ValueError as error:
        message = f"Lexer error: {error}"
    except ParseError as error:
        message = f"Syntax error: {error}"
    except SnakeRuntimeError as error:
        message = f"Runtime error: {error}"
    else:
        return 0

    sys.stdout.flush()
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())