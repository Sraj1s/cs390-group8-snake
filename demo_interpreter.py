from expression_parser import ExpressionParser
from interpreter import Interpreter
from lexer import Lexer
from runtime_errors import SnakeRuntimeError
from statement_nodes import AssignmentNode, PrintNode


def expression(source):
    return ExpressionParser(Lexer(source).tokenize()).parse()


def main():
    # create statement nodes directly for now since the statement parser is not ready yet
    interpreter = Interpreter()

    interpreter.run([
        AssignmentNode('x', expression('10'), declare=True),
        AssignmentNode('y', expression('x + 5'), declare=True),
        PrintNode(expression('y')),
        AssignmentNode('x', expression('x + 1')),
        PrintNode(expression('x')),
        PrintNode(expression('2 + 3 * 4')),
        PrintNode(expression('(2 + 3) * 4')),
        PrintNode(expression('9 / 2')),
    ])

    for source in ['x == 11', 'x != 11', 'x < y', 'x > y',
                   'x <= 11', 'x >= 12']:
        print(source, '->', interpreter.evaluate(expression(source)))

    for source in ['missing + 1', '10 / 0', '(1 < 2) + 3']:
        try:
            interpreter.evaluate(expression(source))
        except SnakeRuntimeError as error:
            print('Runtime error:', error)


if __name__ == '__main__':
    main()