from runtime_errors import SnakeRuntimeError


class Environment:
    def __init__(self, parent=None):
        # symbol table for one scope, parent is the enclosing scope (None for global)
        self.variables = {}
        self.parent = parent

    def declare(self, name, value):
        if name in self.variables:
            raise SnakeRuntimeError(f"Variable '{name}' is already declared")
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise SnakeRuntimeError(f"Undefined variable '{name}'")

    def assign(self, name, value):
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
            return
        raise SnakeRuntimeError(f"Undefined variable '{name}'")