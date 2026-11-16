from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

source = "display(2 + 3 * 4);"
print("Source")
print(source)

tokens = Lexer(source).tokenize()
print("\nTokens")
for token in tokens:
    print(token)

program = Parser(tokens).parse()
statement = program.statements[0]
addition = statement.expression
multiplication = addition.right

print("\nAST")
print(type(program).__name__)
print(f"  {type(statement).__name__}")
print(f"    {type(addition).__name__}({addition.operator})")
print(f"      left:  {type(addition.left).__name__}({addition.left.value})")
print(f"      right: {type(multiplication).__name__}({multiplication.operator})")
print(f"        left:  {type(multiplication.left).__name__}({multiplication.left.value})")
print(f"        right: {type(multiplication.right).__name__}({multiplication.right.value})")

print("\nOutput")
Interpreter().run(program.statements)
