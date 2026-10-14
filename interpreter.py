from environment import Environment
from expression_nodes import NumberNode, VariableNode, BinaryOpNode
from runtime_errors import SnakeRuntimeError
from statement_nodes import AssignmentNode, PrintNode


class Interpreter:
    def __init__(self, environment=None):
        # either start a new environment for this program or reuse an existing one
        self.environment = environment if environment is not None else Environment()

    def evaluate(self, node):
        # evaluate an expression node and return its value
        if isinstance(node, NumberNode):
            self.check_number(node.value)
            return node.value

        if isinstance(node, VariableNode):
            return self.environment.get(node.name)

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

    def execute(self, node):
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
            # print whole-number floats as 10 instead of 10.0
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            print(value)
            return

        raise SnakeRuntimeError(f'Invalid statement node: {type(node).__name__}')

    def execute_block(self, statements):
        # execute statements in order while keeping same environment
        for statement in statements:
            self.execute(statement)

    def run(self, statements):
        self.execute_block(statements)
