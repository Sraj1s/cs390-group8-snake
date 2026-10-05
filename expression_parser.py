from tokens import TokenType
from expression_nodes import NumberNode, VariableNode, BinaryOpNode


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
        # parse a complete expression
        node = self.parse_expression()
        self.expect(TokenType.EOF, "expected end of expression")
        return node

    def parse_expression(self):
        # addition and subtraction have lower precedence
        node = self.parse_term()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token().value
            self.advance()
            right = self.parse_term()
            # keep the previous node on the left to group operators left to right
            node = BinaryOpNode(node, operator, right)
        return node

    def parse_term(self):
        # multiplication and division have higher precedence
        node = self.parse_factor()
        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token().value
            self.advance()
            right = self.parse_factor()
            # keep the previous node on the left to group operators left to right
            node = BinaryOpNode(node, operator, right)
        return node

    def parse_factor(self):
        # a factor is either a number, variable or a parenthesized expression
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            if "." in token.value:
                # if the token has a decimal, make a float
                value = float(token.value)
            else:
                # otherwise make an int
                value = int(token.value)
            return NumberNode(value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return VariableNode(token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.expect(TokenType.RPAREN, "expected ')' to close expression")
            return node

        raise self.error("expected a number, variable, or '('")
