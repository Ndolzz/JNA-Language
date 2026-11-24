class RuntimeErrorJNA(Exception):
    pass


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        environment = self

        while environment is not None:
            if name in environment.variables:
                return environment.variables[name]
            environment = environment.parent

        raise RuntimeErrorJNA(
            f"Variabel '{name}' durung digawe"
        )


def stringify(value):
    if value is True:
        return "bener"
    if value is False:
        return "salah"
    if value is None:
        return "kosong"
    if isinstance(value, list):
        return "[" + ", ".join(stringify(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(key + ": " + stringify(item) for key, item in value.items()) + "}"
    return str(value)
