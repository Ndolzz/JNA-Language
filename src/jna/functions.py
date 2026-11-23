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


class NativeFunction:
    def __init__(self, name, min_args, max_args, handler):
        self.name = name
        self.min_args = min_args
        self.max_args = max_args
        self.handler = handler

    def call(self, arguments, line=None):
        count = len(arguments)

        if count < self.min_args or count > self.max_args:
            expected = (
                str(self.min_args)
                if self.min_args == self.max_args
                else f"{self.min_args} nganti {self.max_args}"
            )
            location = f" pada baris {line}" if line else ""
            raise RuntimeErrorJNA(
                f"Fungsi '{self.name}' butuh {expected} "
                f"argumen, neng {count}{location}"
            )

        return self.handler(arguments, line)
