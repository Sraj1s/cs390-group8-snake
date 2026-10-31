from tokens import TokenType
from expression_nodes import NumberNode, VariableNode, BinaryOpNode, BooleanNode


class ParseError(SyntaxError):
    pass


class ExpressionParser:
    def __init__(self, tokens):
        # we expect the lexer to supply an eof token
        if not tokens or tokens[-1].type != TokenType.EOF:
            raise ValueError("token list must end with EOF")
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.position += 1
        return token

    def error(self, message):
        token = self.current_token()
        if token.type == TokenType.EOF:
            found = "end of input"
        else:
            found = repr(token.value)
        return ParseError(f"{message}; found {found} at line {token.line}, column {token.column}")

    def expect(self, token_type, message):
        if self.current_token().type != token_type:
            raise self.error(message)
        return self.advance()

    def parse(self):
        node = self.parse_expression()
        self.expect(TokenType.EOF, "expected end of expression")
        return node

    def parse_expression(self):
        node = self.parse_arithmetic()
        comparison_types = (
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.GREATER,
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL,
        )
        if self.current_token().type in comparison_types:
            operator = self.advance().value
            right = self.parse_arithmetic()
            node = BinaryOpNode(node, operator, right)
            if self.current_token().type in comparison_types:
                raise self.error("chained comparisons are not supported")
        return node

    def parse_arithmetic(self):
        node = self.parse_term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().value
            self.advance()
            right = self.parse_term()
            node = BinaryOpNode(node, operator, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token().value
            self.advance()
            right = self.parse_factor()
            node = BinaryOpNode(node, operator, right)
        return node

    def parse_factor(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            if "." in token.value:
                value = float(token.value)
            else:
                value = int(token.value)
            return NumberNode(value)

        if token.type == TokenType.TRUE:
            self.advance()
            return BooleanNode(True)

        if token.type == TokenType.FALSE:
            self.advance()
            return BooleanNode(False)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return VariableNode(token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.expect(TokenType.RPAREN, "expected ')' to close expression")
            return node

        raise self.error("expected a number, variable, true/false, or '('")