from tokens import TokenType
from expression_parser import ExpressionParser, ParseError
from statement_nodes import (
    ProgramNode, AssignmentNode, PrintNode, BlockNode, IfNode, WhileNode
)


class Parser(ExpressionParser):
    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []

        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())

        return ProgramNode(statements)

    def parse_statement(self):
        token = self.current_token()

        if token.type == TokenType.VAR:
            return self.parse_variable_declaration()

        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()

        if token.type == TokenType.DISPLAY:
            return self.parse_display()

        if token.type == TokenType.IF:
            return self.parse_if()

        if token.type == TokenType.WHILE:
            return self.parse_while()

        raise self.error("expected a statement")

    def parse_variable_declaration(self):
        self.expect(TokenType.VAR, "expected 'var'")

        name_token = self.expect(
            TokenType.IDENTIFIER,
            "expected variable name"
        )

        self.expect(
            TokenType.ASSIGN,
            "expected '=' after variable name"
        )

        value = self.parse_expression()

        self.expect(
            TokenType.SEMICOLON,
            "expected ';' after variable declaration"
        )

        return AssignmentNode(name_token.value, value, declare=True)

    def parse_assignment(self):
        name_token = self.expect(
            TokenType.IDENTIFIER,
            "expected variable name"
        )

        self.expect(
            TokenType.ASSIGN,
            "expected '=' after variable name"
        )

        value = self.parse_expression()

        self.expect(
            TokenType.SEMICOLON,
            "expected ';' after assignment"
        )

        return AssignmentNode(name_token.value, value)

    def parse_display(self):
        self.expect(
            TokenType.DISPLAY,
            "expected 'display'"
        )

        self.expect(
            TokenType.LPAREN,
            "expected '(' after 'display'"
        )

        expression = self.parse_expression()

        self.expect(
            TokenType.RPAREN,
            "expected ')' after display expression"
        )

        self.expect(
            TokenType.SEMICOLON,
            "expected ';' after display statement"
        )

        return PrintNode(expression)

    def parse_if(self):
        self.expect(TokenType.IF, "expected 'if'")

        # the condition can be written with or without parentheses
        condition = self.parse_expression()
        then_block = self.parse_block()

        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            else_block = self.parse_block()

        return IfNode(condition, then_block, else_block)

    def parse_while(self):
        self.expect(TokenType.WHILE, "expected 'while'")

        condition = self.parse_expression()
        body = self.parse_block()

        return WhileNode(condition, body)

    def parse_block(self):
        self.expect(TokenType.LBRACE, "expected '{' to start block")

        statements = []

        while self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.EOF:
                raise self.error("expected '}' to close block")
            statements.append(self.parse_statement())

        self.expect(TokenType.RBRACE, "expected '}' to close block")

        return BlockNode(statements)