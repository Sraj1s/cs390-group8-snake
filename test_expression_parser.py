import unittest

from expression_nodes import NumberNode, VariableNode, BinaryOpNode
from expression_parser import ExpressionParser, ParseError
from lexer import Lexer
from tokens import TokenType


def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = ExpressionParser(tokens)
    return parser.parse()


class ExpressionParserTests(unittest.TestCase):
    def test_assignment_image_precedence(self):
        tree = parse("2 + 3 * 4")
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "+")
        self.assertIsInstance(tree.left, NumberNode)
        self.assertEqual(tree.left.value, 2)
        self.assertIsInstance(tree.right, BinaryOpNode)
        self.assertEqual(tree.right.operator, "*")
        self.assertIsInstance(tree.right.left, NumberNode)
        self.assertEqual(tree.right.left.value, 3)
        self.assertIsInstance(tree.right.right, NumberNode)
        self.assertEqual(tree.right.right.value, 4)

    def test_parentheses_override_precedence(self):
        tree = parse("(2 + 3) * 4")
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "*")
        self.assertIsInstance(tree.left, BinaryOpNode)
        self.assertEqual(tree.left.operator, "+")
        self.assertIsInstance(tree.left.left, NumberNode)
        self.assertEqual(tree.left.left.value, 2)
        self.assertIsInstance(tree.left.right, NumberNode)
        self.assertEqual(tree.left.right.value, 3)
        self.assertIsInstance(tree.right, NumberNode)
        self.assertEqual(tree.right.value, 4)

    def test_variable_and_decimal(self):
        tree = parse("total + 2.5")
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "+")
        self.assertIsInstance(tree.left, VariableNode)
        self.assertEqual(tree.left.name, "total")
        self.assertIsInstance(tree.right, NumberNode)
        self.assertEqual(tree.right.value, 2.5)

    def test_left_associative_subtraction(self):
        tree = parse("10 - 3 - 2")
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "-")
        self.assertIsInstance(tree.left, BinaryOpNode)
        self.assertEqual(tree.left.operator, "-")
        self.assertIsInstance(tree.left.left, NumberNode)
        self.assertEqual(tree.left.left.value, 10)
        self.assertIsInstance(tree.left.right, NumberNode)
        self.assertEqual(tree.left.right.value, 3)
        self.assertIsInstance(tree.right, NumberNode)
        self.assertEqual(tree.right.value, 2)

    def test_left_associative_division(self):
        tree = parse("20 / 5 / 2")
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "/")
        self.assertIsInstance(tree.left, BinaryOpNode)
        self.assertEqual(tree.left.operator, "/")
        self.assertIsInstance(tree.left.left, NumberNode)
        self.assertEqual(tree.left.left.value, 20)
        self.assertIsInstance(tree.left.right, NumberNode)
        self.assertEqual(tree.left.right.value, 5)
        self.assertIsInstance(tree.right, NumberNode)
        self.assertEqual(tree.right.value, 2)

    def test_missing_operand(self):
        with self.assertRaises(ParseError) as result:
            parse("2 +")
        self.assertIn("end of input at line 1, column 4", str(result.exception))

    def test_missing_closing_parenthesis(self):
        with self.assertRaises(ParseError) as result:
            parse("(2 + 3")
        self.assertIn("expected ')' to close expression", str(result.exception))

    def test_rejects_extra_token(self):
        with self.assertRaises(ParseError) as result:
            parse("2 3")
        self.assertIn("expected end of expression", str(result.exception))

    def test_expression_leaves_statement_delimiter(self):
        tokens = Lexer("2 + 3;").tokenize()
        parser = ExpressionParser(tokens)
        tree = parser.parse_expression()
        self.assertIsInstance(tree, BinaryOpNode)
        self.assertEqual(tree.operator, "+")
        self.assertIsInstance(tree.left, NumberNode)
        self.assertEqual(tree.left.value, 2)
        self.assertIsInstance(tree.right, NumberNode)
        self.assertEqual(tree.right.value, 3)
        self.assertEqual(parser.current_token().type, TokenType.SEMICOLON)

    def test_empty_expression_at_semicolon(self):
        tokens = Lexer(";").tokenize()
        parser = ExpressionParser(tokens)
        with self.assertRaises(ParseError) as result:
            parser.parse_expression()
        self.assertIn("found ';' at line 1, column 1", str(result.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
