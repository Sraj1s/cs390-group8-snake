import unittest

from lexer import Lexer
from parser import Parser
from expression_parser import ParseError
from expression_nodes import NumberNode, VariableNode, BinaryOpNode
from statement_nodes import ProgramNode, AssignmentNode, PrintNode


def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


class ParserTests(unittest.TestCase):

    def test_variable_declaration(self):
        tree = parse("var x = 5;")

        self.assertIsInstance(tree, ProgramNode)
        self.assertEqual(len(tree.statements), 1)

        statement = tree.statements[0]
        self.assertIsInstance(statement, AssignmentNode)
        self.assertEqual(statement.name, "x")
        self.assertIsInstance(statement.expression, NumberNode)
        self.assertEqual(statement.expression.value, 5)

    def test_assignment(self):
        tree = parse("x = 10;")

        statement = tree.statements[0]
        self.assertIsInstance(statement, AssignmentNode)
        self.assertEqual(statement.name, "x")
        self.assertEqual(statement.expression.value, 10)

    def test_display_statement(self):
        tree = parse("display(x);")

        statement = tree.statements[0]
        self.assertIsInstance(statement, PrintNode)
        self.assertIsInstance(statement.expression, VariableNode)
        self.assertEqual(statement.expression.name, "x")

    def test_multiple_statements(self):
        tree = parse(
            "var x = 5; "
            "x = x + 2; "
            "display(x);"
        )

        self.assertIsInstance(tree, ProgramNode)
        self.assertEqual(len(tree.statements), 3)

        self.assertIsInstance(tree.statements[0], AssignmentNode)
        self.assertIsInstance(tree.statements[1], AssignmentNode)
        self.assertIsInstance(tree.statements[2], PrintNode)

    def test_expression_in_assignment(self):
        tree = parse("var result = 2 + 3 * 4;")

        statement = tree.statements[0]
        self.assertIsInstance(statement.expression, BinaryOpNode)
        self.assertEqual(statement.expression.operator, "+")
        self.assertIsInstance(statement.expression.right, BinaryOpNode)
        self.assertEqual(statement.expression.right.operator, "*")

    def test_invalid_assignment(self):
        with self.assertRaises(ParseError):
            parse("var x = ;")


if __name__ == "__main__":
    unittest.main(verbosity=2)


