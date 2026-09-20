from lexer import Lexer

def print_tokens(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)

def test_keywords_and_identifier():
    source = "var score"

    print("\nTest 1:")
    print_tokens(source)

def test_numbers():
    source = "25 10.5 100"

    print("\nTest 2:")
    print_tokens(source)

test_keywords_and_identifier()
test_numbers()
