class AssignmentNode:
    # declare=true is for var/let declarations, false is for variable updates
    def __init__(self, name, expression, declare=False):
        self.name = name
        self.expression = expression
        self.declare = declare


class PrintNode:
    def __init__(self, expression):
        self.expression = expression
