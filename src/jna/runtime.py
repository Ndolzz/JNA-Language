class RuntimeErrorJNA(Exception):
    pass


class Environment:
    def __init__(self):
        self.variables = {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name not in self.variables:
            raise RuntimeErrorJNA(
                f"Variabel '{name}' durung digawe"
            )
        return self.variables[name]
