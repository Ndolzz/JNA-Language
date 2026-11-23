import time

from .parser import (
    Program, Number, String, Boolean, Null,
    Variable, Binary, Unary, Assignment,
    Print, If, Repeat, End,
    FunctionDef, Return, Call, ExpressionStatement,
    Break, Continue, Takon, Ngaso
)
from .runtime import Environment, RuntimeErrorJNA, stringify
from .functions import JNAFunction, NativeFunction
from .stdlib import install_builtins

MAX_CALL_DEPTH = 100


class StopProgram(Exception):
    pass


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        install_builtins(self.globals)
        self.environment = self.globals
        self.function_depth = 0
        self.loop_depth = 0

    def run(self, program):
        try:
            self.execute(program)
        except StopProgram:
            pass

    def execute(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.execute(statement)

        elif isinstance(node, Assignment):
            value = self.evaluate(node.value)
            self.environment.define(node.name, value)

        elif isinstance(node, ExpressionStatement):
            self.evaluate(node.expression)

        elif isinstance(node, Print):
            value = self.evaluate(node.value)
            print(self.stringify(value))

        elif isinstance(node, If):
            condition = self.evaluate(node.condition)

            if self.is_truthy(condition):
                self.execute_block(node.body)
            else:
                self.execute_block(node.otherwise)

        elif isinstance(node, Repeat):
            count = self.evaluate(node.count)

            if isinstance(count, bool) or not isinstance(count, int):
                raise RuntimeErrorJNA(
                    "Jumlah baleni kudu angka bulat"
                )

            if count < 0:
                raise RuntimeErrorJNA(
                    "Jumlah baleni ora kena negatif"
                )

            self.loop_depth += 1

            try:
                for _ in range(count):
                    try:
                        self.execute_block(node.body)
                    except ContinueSignal:
                        continue
            except BreakSignal:
                pass
            finally:
                self.loop_depth -= 1

        elif isinstance(node, FunctionDef):
            function = JNAFunction(
                node.name,
                node.params,
                node.body,
                self.environment
            )
            self.environment.define(node.name, function)

        elif isinstance(node, Return):
            if self.function_depth == 0:
                raise RuntimeErrorJNA(
                    "balekna mung bisa nang njero gawe"
                )

            value = None

            if node.value is not None:
                value = self.evaluate(node.value)

            raise ReturnSignal(value)

        elif isinstance(node, Break):
            if self.loop_depth == 0:
                raise RuntimeErrorJNA(
                    "mandheg mung bisa nang njero baleni"
                )
            raise BreakSignal()

        elif isinstance(node, Continue):
            if self.loop_depth == 0:
                raise RuntimeErrorJNA(
                    "terusna mung bisa nang njero baleni"
                )
            raise ContinueSignal()

        elif isinstance(node, Ngaso):
            duration = self.evaluate(node.duration)

            if isinstance(duration, bool) or not isinstance(duration, (int, float)):
                raise RuntimeErrorJNA(
                    "Durasi ngaso kudu angka"
                )

            if duration < 0:
                raise RuntimeErrorJNA(
                    "Durasi ngaso ora kena negatif"
                )

            time.sleep(duration)

        elif isinstance(node, End):
            raise StopProgram()

        else:
            raise RuntimeErrorJNA(
                f"Instruksi durung didukung: {type(node).__name__}"
            )

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

    def call_function(self, function, arguments, line):
        if self.function_depth >= MAX_CALL_DEPTH:
            raise RuntimeErrorJNA(
                f"Telpun njero fungsi kepaten "
                f"(lewih saka {MAX_CALL_DEPTH}); "
                "ana rekursi sing ora mandheg?"
            )

        call_environment = function.bind(arguments, line)

        previous_environment = self.environment
        self.environment = call_environment

        self.function_depth += 1

        try:
            self.execute_block(function.body)
        except BreakSignal:
            raise RuntimeErrorJNA(
                "mandheg mung bisa nang njero baleni"
            )
        except ContinueSignal:
            raise RuntimeErrorJNA(
                "terusna mung bisa nang njero baleni"
            )
        except ReturnSignal as signal:
            result = signal.value
        else:
            result = None
        finally:
            self.function_depth -= 1
            self.environment = previous_environment

        return result

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, String):
            return node.value

        if isinstance(node, Boolean):
            return node.value

        if isinstance(node, Null):
            return None

        if isinstance(node, Variable):
            return self.environment.get(node.name)

        if isinstance(node, Takon):
            try:
                if node.prompt is not None:
                    prompt = self.stringify(self.evaluate(node.prompt))
                    return input(prompt)

                return input()
            except EOFError:
                raise RuntimeErrorJNA(
                    "Input entek durung ana nilaine"
                )
            except KeyboardInterrupt:
                raise RuntimeErrorJNA(
                    "Input dipeksa mandheg"
                )

        if isinstance(node, Call):
            called = self.environment.get(node.name)

            arguments = [
                self.evaluate(argument)
                for argument in node.arguments
            ]

            if isinstance(called, JNAFunction):
                return self.call_function(called, arguments, node.line)

            if isinstance(called, NativeFunction):
                return called.call(arguments, node.line)

            raise RuntimeErrorJNA(
                f"'{node.name}' bukan fungsi JNA"
            )

        if isinstance(node, Unary):
            value = self.evaluate(node.operand)

            if node.operator == "MINUS":
                self.require_number(value)
                return -value

        if isinstance(node, Binary):
            return self.evaluate_binary(node)

        raise RuntimeErrorJNA(
            f"Ekspresi durung didukung: {type(node).__name__}"
        )

    def evaluate_binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.operator

        if op == "PLUS":
            if isinstance(left, str) and isinstance(right, str):
                return left + right

            self.require_number(left)
            self.require_number(right)
            return left + right

        if op == "MINUS":
            self.require_number(left)
            self.require_number(right)
            return left - right

        if op == "STAR":
            self.require_number(left)
            self.require_number(right)
            return left * right

        if op == "SLASH":
            self.require_number(left)
            self.require_number(right)

            if right == 0:
                raise RuntimeErrorJNA("Ora bisa dibagi nol")

            return left / right

        if op == "PERCENT":
            self.require_number(left)
            self.require_number(right)

            if right == 0:
                raise RuntimeErrorJNA("Ora bisa modulo nol")

            return left % right

        if op == "EQUAL_EQUAL":
            return left == right

        if op == "NOT_EQUAL":
            return left != right

        if op == "GREATER":
            return left > right

        if op == "LESS":
            return left < right

        if op == "GREATER_EQUAL":
            return left >= right

        if op == "LESS_EQUAL":
            return left <= right

        raise RuntimeErrorJNA(f"Operator ora dikenal: {op}")

    @staticmethod
    def require_number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise RuntimeErrorJNA("Operasi iki mbutuhake angka")

    @staticmethod
    def is_truthy(value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    @staticmethod
    def stringify(value):
        return stringify(value)


def interpret(program):
    Interpreter().run(program)
