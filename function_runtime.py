# keep the environment from where the function was defined for lexical scope
class SnakeFunction:
    def __init__(self, definition, closure):
        self.definition = definition
        self.closure = closure

# make sure the return statement exits from inner loops and blocks
class ReturnSignal(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

