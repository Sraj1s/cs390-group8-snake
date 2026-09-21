from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    # keywords
    VAR = "VAR"
    DISPLAY = "DISPLAY"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    DEFINE = "DEFINE"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"

    # values
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    # operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"

    # comparisons
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"

    # assignment
    ASSIGN = "ASSIGN"

    # delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"

    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __str__(self):
        if self.value:
            return f"{self.type.value}({self.value})"

        return self.type.value