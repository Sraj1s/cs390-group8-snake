import json
import sys

from expression_nodes import NumberNode, VariableNode, BinaryOpNode
from expression_parser import ExpressionParser, ParseError
from lexer import Lexer


def node_to_dict(node):
    # turns expression nodes into dicts so they can be printed
    if isinstance(node, NumberNode):
        return {"type": "NumberNode", "value": node.value}

    if isinstance(node, VariableNode):
        return {"type": "VariableNode", "name": node.name}

    if isinstance(node, BinaryOpNode):
        return {
            "type": "BinaryOpNode",
            "left": node_to_dict(node.left),
            "operator": node.operator,
            "right": node_to_dict(node.right)
        }

    raise ValueError("unknown expression node")


def main():
    # if expressions specified on command line then use those
    # otherwise use the examples
    if len(sys.argv) > 1:
        expressions = sys.argv[1:]
    else:
        expressions = ["2 + 3 * 4", "(2 + 3) * 4", "total + 2.5"]

    for expression in expressions:
        print(f"Expression: {expression}")

        try:
            lexer = Lexer(expression)
            tokens = lexer.tokenize()
            parser = ExpressionParser(tokens)
            parsed_tree = parser.parse()
        except (ParseError, ValueError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

        # indentation to make tree easier to read
        tree_output = node_to_dict(parsed_tree)
        print(json.dumps(tree_output, indent=2))
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
