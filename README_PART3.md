Snake Expression Parser - Part 3

This part of the project contains the expression parser and expression
AST nodes for the Snake programming language.

Files:
- expression_parser.py - Converts expression tokens into an AST.
- expression_nodes.py - Defines number, variable, and binary operator nodes.
- test_expression_parser.py - Contains the test cases for the expression parser.
- demo_expressions.py - Prints the ASTs for three example expressions.
- expression_ast_output.txt - Shows the AST output from the examples.
- EXPRESSION_GRAMMAR.ebnf - Contains the grammar rules for expressions.

How to Run:

1. Make sure Python 3.8 or newer is installed.
2. Place these files in the same folder as lexer.py and tokens.py from Part 2.
3. Open a terminal in the project folder.
4. Run:

   py test_expression_parser.py

The test file runs ten different test cases:
1. Operator precedence matching the assignment image
2. Parentheses overriding precedence
3. Variables and decimal numbers
4. Left-to-right subtraction
5. Left-to-right division
6. Missing operand
7. Missing closing parenthesis
8. Extra token after an expression
9. Leaving the semicolon for the statement parser
10. Missing expression before a semicolon

To show the three example ASTs, run:

   py demo_expressions.py

The examples are:
1. 2 + 3 * 4
2. (2 + 3) * 4
3. total + 2.5

To try another expression, run:

   py demo_expressions.py "8 / 2 + 5"

If py is unavailable, use python or python3 instead.

The parser recognizes numbers, variables, arithmetic expressions, and
parentheses. Multiplication and division have higher precedence than
addition and subtraction. Operators at the same precedence level are
grouped from left to right.

Invalid expressions produce an error showing the line and column where
the problem was found. The parser builds an AST but does not calculate
the result.

The grammar file covers the expression portion of Part 3. Assignments,
display statements, and multiple statements still need to be added.
The expression demo does not use semicolons.

GitHub Link for Group 8: https://github.com/Sraj1s/cs390-group8-snake
