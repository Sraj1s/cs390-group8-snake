from runtime_errors import SnakeRuntimeError


class Environment:
    def __init__(self):
        # shared symbol table for the entire program
        self.variables = {}

    def declare(self, name, value):
        if name in self.variables:
            raise SnakeRuntimeError(f"Variable '{name}' is already declared")
        self.variables[name] = value

    def get(self, name):
        if name not in self.variables:
            raise SnakeRuntimeError(f"Undefined variable '{name}'")
        return self.variables[name]

    def assign(self, name, value):
        if name not in self.variables:
            raise SnakeRuntimeError(f"Undefined variable '{name}'")
        self.variables[name] = value
