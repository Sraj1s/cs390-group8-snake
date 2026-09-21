Snake Lexer - Part 2

This project contains the lexer for the Snake programming language.

Files:
- lexer.py - Reads Snake source code and converts it into tokens.
- tokens.py - Defines the different token types used by the lexer.
- test_lexer.py - Contains the test cases for the lexer.
- lexer_output.txt - Shows the output from the test cases.

How to Run:

1. Make sure Python 3 is installed.
2. Place all project files in the same folder.
3. Open a terminal in the project folder.
4. Run:

   python test_lexer.py

The test file runs five different test cases:
1. Variable declaration
2. Arithmetic expression
3. Display statement
4. Control structure
5. Invalid input

The lexer recognizes Snake keywords, identifiers, numbers, arithmetic
operators, comparison operators, assignment, parentheses, braces,
commas, semicolons, whitespace, and comments.

Invalid characters produce an error showing the line and column where
the character was found.

The grammar from Part 1 was not changed for this part of the project.
GitHub Link for Group 8: https://github.com/Sraj1s/cs390-group8-snake
