import io
import unittest
from contextlib import redirect_stdout

from interpreter import Interpreter
from runtime_errors import SnakeRuntimeError
from expression_nodes import NumberNode, VariableNode, BinaryOpNode, FunctionCallNode
from statement_nodes import (
    AssignmentNode, BlockNode, WhileNode, FunctionDefinitionNode,
    ReturnNode, ExpressionStatementNode,
)
from part5_examples import examples


class FunctionRuntimeTests(unittest.TestCase):
    def setUp(self):
        # start each test with a new interpreter
        self.interpreter = Interpreter()

    def define(self, name, parameters, statements):
        # helper to define functions without using the parser
        self.interpreter.execute(FunctionDefinitionNode(name, parameters, BlockNode(statements)))

    def call(self, name, arguments=None):
        # helper to call a function (uses no arguments by default)
        return self.interpreter.evaluate(FunctionCallNode(name, arguments or []))

    def test_five_example_programs(self):
        for title, statements, expected in examples():
            # report each example separately if it fails
            with self.subTest(program=title):
                # capture printed output so it can be compared to the expected output
                output = io.StringIO()
                with redirect_stdout(output):
                    Interpreter().run(statements)
                self.assertEqual(output.getvalue(), expected)

    def test_wrong_argument_count(self):
        # reject calls with not enough or too many arguments
        self.define("one", ["n"], [ReturnNode(VariableNode("n"))])
        for arguments in ([], [NumberNode(1), NumberNode(2)]):
            with self.subTest(arguments=len(arguments)):
                with self.assertRaisesRegex(SnakeRuntimeError, "expects 1 arguments"):
                    self.call("one", arguments)

    def test_undefined_function(self):
        # make calling a function that does not exist raise an error
        with self.assertRaisesRegex(SnakeRuntimeError, "Undefined variable 'missing'"):
            self.call("missing")

    def test_nonfunction_call(self):
        # prevent a regular number from being called as a function
        self.interpreter.environment.declare("x", 4)
        with self.assertRaisesRegex(SnakeRuntimeError, "is not a function"):
            self.call("x")

    def test_duplicate_parameters(self):
        # make sure that two parameters can't have the same name
        with self.assertRaisesRegex(SnakeRuntimeError, "Duplicate parameter"):
            self.define("bad", ["x", "x"], [])

    def test_return_outside_function(self):
        # only allow return while a function is running
        with self.assertRaisesRegex(SnakeRuntimeError, "Return outside"):
            self.interpreter.execute(ReturnNode(NumberNode(1)))

    def test_locals_do_not_leak(self):
        # prevent a function's local variables from being available globally
        self.define("local", [], [AssignmentNode("secret", NumberNode(7), True)])
        self.call("local")
        with self.assertRaisesRegex(SnakeRuntimeError, "Undefined variable 'secret'"):
            self.interpreter.environment.get("secret")

    def test_arguments_are_evaluated_in_caller(self):
        # look up argument values before switching to the function's scope
        self.interpreter.environment.declare("x", 6)
        self.define("identity", ["x"], [ReturnNode(VariableNode("x"))])
        self.assertEqual(self.call("identity", [VariableNode("x")]), 6)

    def test_global_assignment_from_function(self):
        # make assignment update the global variable if no local variable has that name
        self.interpreter.environment.declare("x", 1)
        self.define("change", [], [AssignmentNode("x", NumberNode(8))])
        self.call("change")
        self.assertEqual(self.interpreter.environment.get("x"), 8)

    def test_parameter_assignment_does_not_change_global(self):
        # make sure the global variable stays unchanged when changing a parameter
        self.interpreter.environment.declare("x", 1)
        self.define("change", ["x"], [AssignmentNode("x", NumberNode(8)), ReturnNode(VariableNode("x"))])
        self.assertEqual(self.call("change", [VariableNode("x")]), 8)
        self.assertEqual(self.interpreter.environment.get("x"), 1)

    def test_caller_local_is_not_visible(self):
        # make sure read cannot access secret because read was defined outside caller's scope
        self.define("read", [], [ReturnNode(VariableNode("secret"))])
        self.define("caller", [], [
            AssignmentNode("secret", NumberNode(9), True),
            ReturnNode(FunctionCallNode("read", [])),
        ])
        with self.assertRaisesRegex(SnakeRuntimeError, "Undefined variable 'secret'"):
            self.call("caller")

    def test_error_restores_environment_and_call_depth(self):
        # make sure a runtime error still restores the caller's environment
        original = self.interpreter.environment
        self.define("bad", [], [ReturnNode(BinaryOpNode(NumberNode(1), "/", NumberNode(0)))])
        with self.assertRaisesRegex(SnakeRuntimeError, "Division by zero"):
            self.call("bad")
        self.assertIs(self.interpreter.environment, original)
        self.assertEqual(self.interpreter.call_depth, 0)

        # make sure the interpreter no longer considers itself inside a function
        with self.assertRaisesRegex(SnakeRuntimeError, "Return outside"):
            self.interpreter.execute(ReturnNode())

    def test_bare_return_and_fallthrough(self):
        # give none for either an empty body or a return without a value
        self.define("empty", [], [])
        self.define("bare", [], [ReturnNode(), ReturnNode(NumberNode(999))])
        self.assertIsNone(self.call("empty"))
        self.assertIsNone(self.call("bare"))

    def test_return_leaves_loop(self):
        # make sure return exits the function, even from inside an infinite loop
        from expression_nodes import BooleanNode
        self.define("loop", [], [WhileNode(BooleanNode(True), BlockNode([ReturnNode(NumberNode(5))]))])
        self.assertEqual(self.call("loop"), 5)

    def test_nested_call_returns_to_caller(self):
        # make sure outer still has access to its parameter after inner finishes
        self.define("inner", [], [ReturnNode(NumberNode(3))])
        self.define("outer", ["x"], [
            ExpressionStatementNode(FunctionCallNode("inner", [])),
            ReturnNode(VariableNode("x")),
        ])
        self.assertEqual(self.call("outer", [NumberNode(7)]), 7)
        self.assertEqual(self.interpreter.call_depth, 0)

    def test_parameter_cannot_be_redeclared_in_function_body(self):
        # make sure parameters and top level function locals share the same scope
        self.define("bad", ["x"], [AssignmentNode("x", NumberNode(2), True)])
        with self.assertRaisesRegex(SnakeRuntimeError, "already declared"):
            self.call("bad", [NumberNode(1)])


if __name__ == "__main__":
    # run the tests and show the names and results of each one
    unittest.main(verbosity=2)