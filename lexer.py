from tokens import Token, TokenType


# list of keywords (the values will be the corresponding TokenType)
KEYWORDS = {
    "var": TokenType.VAR,
    "display": TokenType.DISPLAY,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "define": TokenType.DEFINE,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE
}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def current_char(self):
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def peek(self):
        if self.position + 1 >= len(self.source):
            return None

        return self.source[self.position + 1]

    def advance(self):
        char = self.current_char()

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    def read_identifier(self):
        start_column = self.column
        value = ""

        while self.current_char() is not None:
            char = self.current_char()

            if char.isalnum() or char == "_":
                value += char
                self.advance()
            else:
                break

        # if value is a keyword use that, otherwise it's an identifier
        token_type = KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            value,
            self.line,
            start_column
        )

    def read_number(self):
        start_column = self.column
        value = ""
        decimal_found = False

        while self.current_char() is not None:
            char = self.current_char()

            if char.isdigit():
                value += char
                self.advance()

            elif (
                char == "."
                and not decimal_found
                and self.peek() is not None
                and self.peek().isdigit()
            ):
                decimal_found = True
                value += char
                self.advance()

            else:
                break

        return Token(
            TokenType.NUMBER,
            value,
            self.line,
            start_column
        )

    def skip_whitespace(self):
        while (
            self.current_char() is not None
            and self.current_char().isspace()
        ):
            self.advance()

    def skip_comment(self):
        while (
            self.current_char() is not None
            and self.current_char() != "\n"
        ):
            self.advance()

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:
            char = self.current_char()

            # ignore whitespace
            if char.isspace():
                self.skip_whitespace()
                continue

            # ignore comments
            if char == "/" and self.peek() == "/":
                self.skip_comment()
                continue

            # keywords and identifiers
            if char.isalpha():
                tokens.append(
                    self.read_identifier()
                )
                continue

            # integer and decimal numbers
            if char.isdigit():
                tokens.append(
                    self.read_number()
                )
                continue

            # operators and delimiters
            single_tokens = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                ",": TokenType.COMMA,
                ";": TokenType.SEMICOLON
            }

            if char in single_tokens:
                tokens.append(
                    Token(single_tokens[char], char, self.line, self.column)
                )
                self.advance()
                continue

            # assignment and comparison operators
            if char == "=":
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(
                        Token(TokenType.EQUAL, "==", self.line, start_column)
                    )
                else:
                    self.advance()
                    tokens.append(
                        Token(TokenType.ASSIGN, "=", self.line, start_column)
                    )

                continue

            if char == "!":
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(
                        Token(TokenType.NOT_EQUAL, "!=", self.line, start_column)
                    )
                    continue

            if char == "<":
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(
                        Token(TokenType.LESS_EQUAL, "<=", self.line, start_column)
                    )
                else:
                    self.advance()
                    tokens.append(
                        Token(TokenType.LESS, "<", self.line, start_column)
                    )

                continue

            if char == ">":
                start_column = self.column

                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(
                        Token(TokenType.GREATER_EQUAL, ">=", self.line, start_column)
                    )
                else:
                    self.advance()
                    tokens.append(
                        Token(TokenType.GREATER, ">", self.line, start_column)
                    )

                continue

            raise ValueError(
                f"Unrecognized character '{char}' "
                f"at line {self.line}, column {self.column}"
            )
        # add token for end of file
        tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.line,
                self.column
            )
        )

        return tokens