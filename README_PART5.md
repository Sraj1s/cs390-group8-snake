# Snake Programming Language — Part 5

## 1. Project Overview

Snake is a small programming language built for our CS 390 final project. It uses a lexer to turn source code into tokens, a parser to build an abstract syntax tree (AST), and an interpreter to execute the program. Part 5 adds functions and local scope, along with `for` loops, `break`, and `continue`.

## 2. Supported Features

- Variable declarations with `var` and assignments to existing variables
- Integer and decimal numbers, arithmetic (`+`, `-`, `*`, `/`), and comparisons (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- Boolean values `true` and `false`
- Output using `display(expression);`
- `if`/`else` statements and `while` loops
- Functions defined with `define`, including parameters, calls, local variables, and `return`
- Global, function-local, and block scope
- Part 5 extension: `for` loops with `break;` and `continue;`
- Single-line comments starting with `//`

## 3. How to Run

Use Python 3. No third-party packages are required for the source files shown in this project.

Open a terminal in the folder containing `run_snake.py` and run:

```cmd
py run_snake.py test_programs_part5\01_parameters_return.snake
```

To run another program, replace the filename with the path to that `.snake` file. On systems where Python is invoked with `python3`, use `python3` instead of `py`.

## 4. Functions and Scope

Functions use the `define` keyword. They can accept parameters and return values. Variables declared inside a function are local to that function. A local variable can have the same name as a global variable without changing the global variable.

```text
var x = 10;

define test() {
    var x = 20;
    display(x);
}

test();
display(x);
```

Expected output:

```text
20
10
```

The interpreter represents scope using `Environment` objects. A new environment can refer to an enclosing environment to look up variables. A function also keeps the environment where it was defined (its closure), which supports lexical scope. Blocks create their own scopes, while function parameters and top-level function-body variables share the function's local environment.

## 5. Part 5 Extension: `for`, `break`, and `continue`

A `for` loop contains an initializer, a condition, an update, and a block. The initializer ends with a semicolon, and the condition ends with another semicolon. There is no semicolon between the update and the opening `{`.

```text
for var i = 0; i < 5; i = i + 1 {
    if i == 2 { continue; }
    if i == 4 { break; }
    display(i);
}
```

Expected output:

```text
0
1
3
```

`break;` exits the current loop. `continue;` skips the rest of the current iteration. In a `for` loop, the update still runs after `continue;`. These statements also work inside `while` loops. A variable declared by a `for` initializer belongs to that loop's scope and is not available after the loop finishes.

## 6. Part 5 Test Programs

The `test_programs_part5` folder contains the following test programs:

| File | What it demonstrates | Expected output |
| --- | --- | --- |
| `01_parameters_return.snake` | Function parameters and return values | `30` |
| `02_local_shadowing.snake` | Local variable shadows a global variable | `20`, then `10` |
| `03_new_locals.snake` | Local variables within functions | `5`, then `10` |
| `04_nested_return.snake` | Return behavior within nested statements | `1`, then `0` |
| `05_lexical_scope.snake` | Lexical scope | `10` |
| `06_for_loop.snake` | `for` loop with `continue` and `break` | `0`, `1`, `3` |
| `07_for_scope.snake` | Loop-local variable cannot be accessed afterward | `0`, `1`, `2`, then `Runtime error: Undefined variable 'i'` |

The runtime error in Test 07 is intentional: it confirms that the loop variable does not leak into the surrounding scope. Each program can be run using the command shown in Section 3 with its own filename.

## 7. Main Project Files

| File | Purpose |
| --- | --- |
| `tokens.py` | Defines token types and the token structure |
| `lexer.py` | Converts Snake source code into tokens |
| `expression_nodes.py` | Defines AST nodes for expressions |
| `statement_nodes.py` | Defines AST nodes for statements, functions, and loops |
| `expression_parser.py` | Parses expressions and function calls |
| `parser.py` | Parses statements and builds the program AST |
| `environment.py` | Stores variables and manages nested scopes |
| `function_runtime.py` | Stores function closures and control-flow signals |
| `interpreter.py` | Evaluates expressions and executes statements |
| `runtime_errors.py` | Defines the Snake runtime error type |
| `run_snake.py` | Runs a Snake source file through the language implementation |
| `PART5_GRAMMAR.ebnf` | Documents the Part 5 language grammar |
| `test_programs_part5/` | Contains the Part 5 test programs |

## GitHub

Group 8 Repository:

https://github.com/Sraj1s/cs390-group8-snake