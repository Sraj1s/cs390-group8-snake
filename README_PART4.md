Snake Interpreter - Part 4

Files:

- interpreter.py - Performs assignment, printing, comparisons,
  and arithmetic evaluation
- environment.py - Stores, retrieves, and updates variable values
- statement_nodes.py - Defines nodes for print and assignment statements
- runtime_errors.py - Runtime error for use by interpreter
- expression_parser.py - Modified to support comparisons between
  arithmetic expressions
- EXPRESSION_GRAMMAR.ebnf - Grammar for expressions with support
  for comparisons between arithmetic expressions
- demo_interpreter.py - A demo of the interpreter that uses
  statement nodes

Running:

1. Make sure Python 3.8 or later is installed.
2. Put these files in the same directory as the previous
   parts' lexer.py, tokens.py, and expression_nodes.py
3. Replace the previous expression_parser.py and EXPRESSION_GRAMMAR.ebnf
   with these new ones. Keep the other files from the previous parts.
4. Open a terminal in the project directory.
5. Run:

   py demo_interpreter.py

This will demonstrate variable declaration and assignment,
printing, arithmetic, all six comparisons, and runtime errors.
Statement nodes are constructed directly in the demo since the
full statement parser is not yet implemented.

Expected output from the demo:

```text
15
11
14
20
4.5
x == 11 -> True
x != 11 -> False
x < y -> True
x > y -> False
x <= 11 -> True
x >= 12 -> False
Runtime error: Undefined variable 'missing'
Runtime error: Division by zero
Runtime error: Operation requires numeric values
```

The demo was run while the code was being implemented and produced
the expected output. 

The expression parser tests can be run with:

py test_expression_parser.py

The expression parser supports parentheses and operator precedence
for arithmetic operations. Comparisons are evaluated with lower
precedence than arithmetic. Comparisons supported by the interpreter
are: ==, !=, <, >, <=, and >=. All comparisons use numeric
values and return either True or False. Chained comparisons
(like 1 < 2 < 3) are not supported. Boolean return values can
be printed or assigned to variables but cannot be used in arithmetic.
Division can result in a decimal. Integer results are printed
without a decimal.

The environment uses a Python dictionary to store variable names
and their values. For example, declaring variable x to be 10
will store the variable name x with a value of 10. When x is
read from the environment its stored value is returned. When
a new value is assigned to x it will be updated. All blocks
share the same environment.

AssignmentNode(name, expression, declare=True) creates a
new variable with the given name and value (from expression).
AssignmentNode(name, expression) assigns a new value to an
existing variable given its name and value (from expression).
PrintNode(expression) prints the value of the given expression.
Interpreter.run(statements) runs a list of statement nodes
in order.

Accessing an undefined variable, dividing by zero, performing an
invalid operation, or declaring the same variable more than once
will result in a SnakeRuntimeError.

GitHub Link for Group 8: https://github.com/Sraj1s/cs390-group8-snake
