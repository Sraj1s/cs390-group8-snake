Snake Functions and Scope - Part 5

This part of the project contains the function runtime and function scope
support for the Snake programming language.

Files:

- interpreter.py - Executes functions, binds parameters, and handles return values.
- function_runtime.py - Stores function definitions and handles return signals.
- environment.py - Stores variables and links local scopes to enclosing scopes.
- expression_nodes.py - Includes the function call node.
- statement_nodes.py - Includes function definition, return, and expression statement nodes.
- part5_examples.py - Contains five function and scope examples built from AST nodes.
- demo_functions.py - Runs the five examples and prints their output.
- test_function_runtime.py - Contains 16 test cases for functions and scope.
- programs_part5 - Contains matching Snake examples and expected output.


How to Run:

1. Make sure Python 3.10 or newer is installed.
2. Keep these files in the same folder as the existing Part 4 project files.
3. Open a terminal in the project folder.
4. Run:

   py test_function_runtime.py

The tests check function calls, parameters, return values, local scope,
argument counts, and runtime errors.

To run the five examples, run:

   py demo_functions.py

The examples are:

1. Parameters and return - prints 30.
2. Local shadowing - prints 20, then 10.
3. New locals on every call - prints 5, then 10.
4. Return from a nested block - prints 1, then 0.
5. Definition scope instead of caller scope - prints 10.

If py is unavailable, use python or python3 instead.

Each function call creates a new local environment for its parameters and
local variables. Its parent is the environment where the function was defined.
This allows local variables to use the same names as global variables without
replacing them. Assignment updates the nearest existing variable.

Return statements exit the function, including from inside loops and blocks.
The interpreter restores the caller's environment after the function finishes
or encounters an error.

The current demo builds AST nodes directly. The matching Snake source examples
require function parser integration.

GitHub Link for Group 8: https://github.com/Sraj1s/cs390-group8-snake
