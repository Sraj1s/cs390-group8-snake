from tokens import TokenType
from expression_parser import ExpressionParser, ParseError
from expression_nodes import FunctionCallNode
from statement_nodes import (
    ProgramNode, AssignmentNode, PrintNode, BlockNode, IfNode, WhileNode,
    FunctionDefinitionNode, ReturnNode, ExpressionStatementNode,
    ForNode, BreakNode, ContinueNode
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

        if token.type == TokenType.DEFINE:
            return self.parse_function()

        if token.type == TokenType.RETURN:
            return self.parse_return()

        if token.type == TokenType.IDENTIFIER:
            # "x = 5;" is an assignment, "test();" is a call statement
            if self.peek_token().type == TokenType.ASSIGN:
                return self.parse_assignment()
            return self.parse_expression_statement()

        if token.type == TokenType.DISPLAY:
            return self.parse_display()

        if token.type == TokenType.IF:
            return self.parse_if()

        if token.type == TokenType.WHILE:
            return self.parse_while()
        # part 5 extension: for loops, break, and continue
        if token.type == TokenType.FOR:
            return self.parse_for()

        if token.type == TokenType.BREAK:
            return self.parse_break()

        if token.type == TokenType.CONTINUE:
            return self.parse_continue()

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
    
    def peek_token(self):
        # look one token ahead without consuming anything
        index = self.position + 1
        if index < len(self.tokens):
            return self.tokens[index]
        return self.tokens[-1]  # EOF

    def parse_function(self):
        # parse define name(a, b) { ... }
        self.expect(TokenType.DEFINE, "expected 'define'")
        name_token = self.expect(
            TokenType.IDENTIFIER, "expected function name after 'define'"
        )
        self.expect(TokenType.LPAREN, "expected '(' after function name")

        parameters = []
        # a function can have no parameters
        if self.current_token().type != TokenType.RPAREN:
            parameters.append(
                self.expect(TokenType.IDENTIFIER, "expected parameter name").value
            )
            # more parameters are separated by commas
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                parameters.append(
                    self.expect(TokenType.IDENTIFIER, "expected parameter name").value
                )

        self.expect(TokenType.RPAREN, "expected ')' after parameters")
        body = self.parse_block()
        return FunctionDefinitionNode(name_token.value, parameters, body)

    def parse_return(self):
        # parse return expr; or just return;
        self.expect(TokenType.RETURN, "expected 'return'")

        expression = None
        if self.current_token().type != TokenType.SEMICOLON:
            expression = self.parse_expression()

        self.expect(TokenType.SEMICOLON, "expected ';' after return")
        return ReturnNode(expression)

    def parse_expression_statement(self):
        # parse a call used as a statement, like test();
        expression = self.parse_expression()

        # only calls make sense as standalone statements
        if not isinstance(expression, FunctionCallNode):
            raise self.error("expected a statement")

        self.expect(TokenType.SEMICOLON, "expected ';' after function call")
        return ExpressionStatementNode(expression)

    def parse_for(self):
        # parse for var i = 0; i < 5; i = i + 1 { ... }
        self.expect(TokenType.FOR, "expected 'for'")

        # the initializer is a var declaration or an assignment, both end with ';'
        if self.current_token().type == TokenType.VAR:
            initializer = self.parse_variable_declaration()
        else:
            initializer = self.parse_assignment()

        condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON, "expected ';' after for condition")

        # the update is an assignment with no ';' before the block
        name_token = self.expect(TokenType.IDENTIFIER, "expected variable name in for update")
        self.expect(TokenType.ASSIGN, "expected '=' in for update")
        update = AssignmentNode(name_token.value, self.parse_expression())

        body = self.parse_block()
        return ForNode(initializer, condition, update, body)

    def parse_break(self):
        # parse break;
        self.expect(TokenType.BREAK, "expected 'break'")
        self.expect(TokenType.SEMICOLON, "expected ';' after break")
        return BreakNode()

    def parse_continue(self):
        # parse continue;
        self.expect(TokenType.CONTINUE, "expected 'continue'")
        self.expect(TokenType.SEMICOLON, "expected ';' after continue")
        return ContinueNode()