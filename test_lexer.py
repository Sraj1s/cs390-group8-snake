from lexer import Lexer


def print_tokens(source):
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        for token in tokens:
            print(token)

    except ValueError as error:
        print(error)


def test_variable():
    source = "var x = 10;"

    print("\nTest 1: Variable Declaration")
    print_tokens(source)


def test_arithmetic():
    source = "var total = 5 + 3 * 2;"

    print("\nTest 2: Arithmetic Expression")
    print_tokens(source)


def test_display():
    source = "display(total);"

    print("\nTest 3: Display Statement")
    print_tokens(source)


def test_control():
    source = "if x > 5 { display(x); }"

    print("\nTest 4: Control Structure")
    print_tokens(source)


def test_invalid():
    source = "var x = 10 @ 5;"

    print("\nTest 5: Invalid Input")
    print_tokens(source)


test_variable()
test_arithmetic()
test_display()
test_control()
test_invalid()