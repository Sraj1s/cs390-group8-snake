class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


class AssignmentNode:
    def __init__(self, name, expression, declare=False):
        self.name = name
        self.expression = expression
        self.declare = declare


class PrintNode:
    def __init__(self, expression):
        self.expression = expression


class BlockNode:
    def __init__(self, statements):
        self.statements = statements


class IfNode:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDefinitionNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body  # BlockNode


class ReturnNode:
    def __init__(self, expression=None):
        self.expression = expression


class ExpressionStatementNode:
    def __init__(self, expression):
        self.expression = expression
