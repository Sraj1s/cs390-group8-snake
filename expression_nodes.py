# node containing a number from the code
class NumberNode:
    def __init__(self, value):
        self.value = value

# node containing the name of a variable
class VariableNode:
    def __init__(self, name):
        self.name = name

# node containing an operator and the expressions on each side
class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

# node containing a true or false value from the code
class BooleanNode:
    def __init__(self, value):
        self.value = value

# node containing a function name and its arguments
class FunctionCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
