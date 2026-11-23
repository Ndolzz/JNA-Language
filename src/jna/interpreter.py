from .parser import (
    Program, Number, String, Boolean, Null,
    Variable, Binary, Unary, Assignment,
    Print, If, Repeat, End
)
from .runtime import Environment, RuntimeErrorJNA


class StopProgram(Exception):
    pass


class Interpreter:
    def __init__(self):
        self.environment = Environment()

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

            for _ in range(count):
                self.execute_block(node.body)

        elif isinstance(node, End):
            raise StopProgram()

        else:
            raise RuntimeErrorJNA(
                f"Instruksi durung didukung: {type(node).__name__}"
            )

    def execute_block(self, statements):
        for statement in statements:
            self.execute(statement)

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
        if value is True:
            return "bener"
        if value is False:
            return "salah"
        if value is None:
            return "kosong"
        return str(value)


def interpret(program):
    Interpreter().run(program)
