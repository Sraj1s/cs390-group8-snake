from environment import Environment
from expression_nodes import NumberNode, VariableNode, BinaryOpNode, BooleanNode, FunctionCallNode
from runtime_errors import SnakeRuntimeError
from function_runtime import SnakeFunction, ReturnSignal
from statement_nodes import (
    ProgramNode, AssignmentNode, PrintNode, BlockNode, IfNode, WhileNode,
    FunctionDefinitionNode, ReturnNode, ExpressionStatementNode
)


class Interpreter:
    def __init__(self, environment=None):
        # either start a new environment for this program or reuse an existing one
        self.environment = environment if environment is not None else Environment()
        self.call_depth = 0

    def evaluate(self, node):
        # evaluate an expression node and return its value
        if isinstance(node, NumberNode):
            self.check_number(node.value)
            return node.value

        if isinstance(node, BooleanNode):
            return node.value

        if isinstance(node, VariableNode):
            return self.environment.get(node.name)

        if isinstance(node, FunctionCallNode):
            return self.call_function(node)

        if isinstance(node, BinaryOpNode):
            # evaluate both sides first
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            # check that both values are numbers before performing the operation
            self.check_number(left)
            self.check_number(right)

            # perform the appropriate operation
            if node.operator == '+':
                return left + right
            if node.operator == '-':
                return left - right
            if node.operator == '*':
                return left * right
            if node.operator == '/':
                if right == 0:
                    raise SnakeRuntimeError('Division by zero')
                return left / right

            # comparisons return true or false so they can be used in conditions
            if node.operator == '==':
                return left == right
            if node.operator == '!=':
                return left != right
            if node.operator == '<':
                return left < right
            if node.operator == '>':
                return left > right
            if node.operator == '<=':
                return left <= right
            if node.operator == '>=':
                return left >= right

            raise SnakeRuntimeError(f"Invalid operator '{node.operator}'")

        raise SnakeRuntimeError(f'Invalid expression node: {type(node).__name__}')

    def check_number(self, value):
        # bool is a subclass of int, so use exact types to reject it
        if type(value) not in (int, float):
            raise SnakeRuntimeError('Operation requires numeric values')

    def check_condition(self, value):
        # if and while conditions must be true or false
        if type(value) is not bool:
            raise SnakeRuntimeError('Condition must be true or false')

    def format_value(self, value):
        # snake uses lowercase true and false
        if type(value) is bool:
            return 'true' if value else 'false'
        # print whole-number floats as 10 instead of 10.0
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def execute(self, node):
        if isinstance(node, FunctionDefinitionNode):
            if len(set(node.parameters)) != len(node.parameters):
                raise SnakeRuntimeError("Duplicate parameter name")
            self.environment.declare(node.name, SnakeFunction(node, self.environment))
            return

        if isinstance(node, ReturnNode):
            if self.call_depth == 0:
                raise SnakeRuntimeError("Return outside a function")
            value = None if node.expression is None else self.evaluate(node.expression)
            raise ReturnSignal(value)

        if isinstance(node, ExpressionStatementNode):
            self.evaluate(node.expression)
            return

        if isinstance(node, AssignmentNode):
            # evaluate expression first before assigning to a variable
            value = self.evaluate(node.expression)

            # if declare is true, create a new variable, otherwise reassign to an existing variable
            if node.declare:
                self.environment.declare(node.name, value)
            else:
                self.environment.assign(node.name, value)
            return

        if isinstance(node, PrintNode):
            value = self.evaluate(node.expression)
            print(self.format_value(value))
            return

        if isinstance(node, IfNode):
            condition = self.evaluate(node.condition)
            self.check_condition(condition)
            if condition:
                self.execute(node.then_block)
            elif node.else_block is not None:
                self.execute(node.else_block)
            return

        if isinstance(node, WhileNode):
            # the condition is checked again before every pass through the body
            while True:
                condition = self.evaluate(node.condition)
                self.check_condition(condition)
                if not condition:
                    break
                self.execute(node.body)
            return

        if isinstance(node, BlockNode):
            self.execute_scoped_block(node.statements)
            return

        if isinstance(node, ProgramNode):
            self.execute_block(node.statements)
            return

        raise SnakeRuntimeError(f'Invalid statement node: {type(node).__name__}')

    def execute_block(self, statements):
        # execute statements in order while keeping same environment
        for statement in statements:
            self.execute(statement)

    def execute_scoped_block(self, statements):
        # blocks get their own scope, which can see variables from outside
        outer = self.environment
        self.environment = Environment(outer)
        try:
            self.execute_block(statements)
        finally:
            # always go back to the outer scope, even if an error happens
            self.environment = outer

    def call_function(self, node):
        function = self.environment.get(node.name)
        if not isinstance(function, SnakeFunction):
            raise SnakeRuntimeError(f"'{node.name}' is not a function")
        definition = function.definition
        if len(node.arguments) != len(definition.parameters):
            raise SnakeRuntimeError(
                f"Function '{node.name}' expects {len(definition.parameters)} arguments, "
                f"got {len(node.arguments)}"
            )

        # arguments belong to the caller, evaluate them before changing scopes
        values = [self.evaluate(argument) for argument in node.arguments]
        local = Environment(function.closure)
        for name, value in zip(definition.parameters, values):
            local.declare(name, value)

        caller = self.environment
        self.environment = local
        self.call_depth += 1
        try:
            # parameters and top level function variables are in the same scope
            self.execute_block(definition.body.statements)
        except ReturnSignal as result:
            return result.value
        finally:
            self.environment = caller
            self.call_depth -= 1
        # functions that reach the end without a return statement return none
        return None

    def run(self, statements):
        self.execute_block(statements)