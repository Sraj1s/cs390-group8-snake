# Snake Interpreter - Part 4

Part 4 makes Snake executable. The interpreter walks the syntax tree built by
the parser and runs the program.

## Files

New in Part 4:

- `interpreter.py` - Executes statements and evaluates expressions.
- `environment.py` - Symbol table that stores, retrieves, and updates variables.
- `runtime_errors.py` - `SnakeRuntimeError`, raised for errors while a program runs.
- `run_snake.py` - Runs a Snake program file from the command line.
- `demo_interpreter.py` - Small demo that builds statement nodes directly.
- `programs/` - Test programs (`.snake`) and their expected output (`.expected.txt`).
- `PART4_GRAMMAR.ebnf` - Updated grammar. It replaces `PART3_GRAMMAR.ebnf` and `EXPRESSION_GRAMMAR.ebnf`.

Updated from Part 3:

- `expression_nodes.py` - Added `BooleanNode`.
- `expression_parser.py` - Added comparisons and `true`/`false`.
- `statement_nodes.py` - Added `BlockNode`, `IfNode`, `WhileNode`. `AssignmentNode` now has a `declare` flag and its value field is named `expression` (it was `value`).
- `parser.py` - Added `if`/`else`, `while`, and blocks. `var` now builds a declaration node.
- `test_parser.py` - Updated for the renamed `AssignmentNode` field.

Unchanged from earlier parts: `tokens.py`, `lexer.py`, `test_lexer.py`, `test_expression_parser.py`, `demo_expressions.py`, `expression_ast_output.txt`.

## How to Run

Requires Python 3.10 or newer. (Older versions have a built-in module named
`parser` that can conflict with our `parser.py`.) Keep all files in one folder.

Run a Snake program:

```text
py run_snake.py programs/01_arithmetic.snake
```

Run the earlier tests:

```text
py test_lexer.py
py test_expression_parser.py
py test_parser.py
```

Run the demo:

```text
py demo_interpreter.py
```

If `py` is unavailable, use `python` or `python3`.

## Language Features

- Variables: `var x = 10;` declares, `x = x + 1;` updates.
- Arithmetic: `+ - * /` with normal precedence and parentheses. Division can give a decimal.
- Comparisons: `== != < > <= >=`. They give `true` or `false`.
- `true` and `false` values.
- Output: `display(x);` prints numbers and `true`/`false`. Whole-number decimals print without `.0` (so `10 / 2` prints `5`).
- If/else: the condition works with or without parentheses.
- While loops.
- Comments start with `//`.

Example:

```text
var x = 1;
while (x <= 5) {
    display(x);
    x = x + 1;
}
```

Not included yet: `define`, `return`, function calls, and negative numbers written like `-5`.

## Environment / Symbol Table

`Environment` holds a Python dictionary that maps each variable name to its
current value, plus a link to the enclosing environment (`parent`).

- `declare(name, value)` adds a new variable to the current scope. It is an error if the name already exists in that scope.
- `get(name)` returns the value. It looks in the current scope first, then each enclosing scope. It is an error if the name is not found anywhere.
- `assign(name, value)` updates the variable in the nearest scope that has it. It is an error if the name is not found.

The program starts with one global environment. Every `{ }` block (an `if`,
`else`, or `while` body) runs in a new child environment. So:

- Code inside a block can read and update variables declared outside it.
- A variable declared inside a block disappears when the block ends.
- A `var` inside a loop body works on every pass, because each pass gets a fresh scope.

## Runtime Errors

All runtime errors raise `SnakeRuntimeError` and `run_snake.py` prints them as
`Runtime error: <message>`.

| Error | Message |
|---|---|
| Undefined variable (read or update) | `Undefined variable 'x'` |
| Declaring a name twice in one scope | `Variable 'x' is already declared` |
| Division by zero | `Division by zero` |
| Arithmetic or comparison on a true/false value | `Operation requires numeric values` |
| `if` or `while` condition that is not true/false | `Condition must be true or false` |

Syntax errors are reported as `Syntax error: ...` with the line and column.
Comparisons only work on numbers, and chained comparisons like `1 < 2 < 3` are
a syntax error.

## Test Programs

Each program in `programs/` has a matching `.expected.txt` with the expected
output. Each program was run with `py run_snake.py programs/<name>.snake` and the
actual output was identical to the expected output (error messages included).

| Program | What it shows | Expected / actual output |
|---|---|---|
| `01_arithmetic.snake` | Variables, update, precedence, parentheses, decimal division | 15, 11, 14, 20, 4.5, 3 |
| `02_comparisons.snake` | All six comparisons and a comparison stored in a variable | false, true, true, false, true, false, true |
| `03_if_else.snake` | If/else, with and without parentheses, a true/false variable as the condition | 8, 0, 1 |
| `04_while_loop.snake` | While loops, counting and summing | 1, 2, 3, 4, 5, 55 |
| `05_nested_scope.snake` | An `if` inside a `while`, with a `var` declared in the loop body | 1, 4, 9, 77 |
| `06_error_undefined.snake` | Undefined variable | 1, then `Runtime error: Undefined variable 'missing'` |
| `07_error_division.snake` | Division by zero | 5, then `Runtime error: Division by zero` |
| `08_error_invalid.snake` | Arithmetic on a true/false value | true, then `Runtime error: Operation requires numeric values` |
| `09_error_condition.snake` | Non-boolean condition | `Runtime error: Condition must be true or false` |

A program stops at the first runtime error, so any lines after the error do not run.

## How the Pieces Fit Together

`run_snake.py` reads the file, `Lexer` turns the text into tokens, `Parser`
builds the syntax tree (`ProgramNode` and the statement and expression nodes),
and `Interpreter` executes it.

## GitHub

Group 8 Repository:

https://github.com/Sraj1s/cs390-group8-snake