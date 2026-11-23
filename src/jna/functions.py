from .runtime import Environment, RuntimeErrorJNA


class JNAFunction:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def bind(self, arguments, line=None):
        if len(arguments) != len(self.params):
            location = f" pada baris {line}" if line else ""
            raise RuntimeErrorJNA(
                f"Fungsi '{self.name}' butuh {len(self.params)} "
                f"argumen, neng {len(arguments)}{location}"
            )

        environment = Environment(parent=self.closure)

        for param, argument in zip(self.params, arguments):
            environment.define(param, argument)

        return environment
