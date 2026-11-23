import builtins
import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestInput(unittest.TestCase):

    def execute(self, source, input_lines=None):
        output = io.StringIO()
        lines = list(input_lines or [])
        state = {"index": 0}
        original_input = builtins.input

        def fake_input(prompt=""):
            if state["index"] >= len(lines):
                raise EOFError
            value = lines[state["index"]]
            state["index"] += 1
            output.write(prompt)
            return value

        builtins.input = fake_input

        try:
            with redirect_stdout(output):
                program = parse(tokenize(source))
                Interpreter().run(program)
        finally:
            builtins.input = original_input

        return output.getvalue()

    def test_takon_returns_string(self):
        result = self.execute(
            'jeneng = takon\nngomong jeneng\n',
            input_lines=["Nendi"],
        )
        self.assertEqual(result, "Nendi\n")

    def test_takon_with_prompt(self):
        result = self.execute(
            'jeneng = takon "Siapa jenengmu?"\nngomong jeneng\n',
            input_lines=["Nendi"],
        )
        self.assertEqual(result, "Siapa jenengmu?Nendi\n")

    def test_takon_value_is_string(self):
        result = self.execute(
            'umur = takon\nngomong umur + " taun"\n',
            input_lines=["16"],
        )
        self.assertEqual(result, "16 taun\n")

    def test_takon_at_end_of_input(self):
        source = 'jeneng = takon\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source, input_lines=[])

    def test_ngaso_zero_completes(self):
        result = self.execute(
            'ngomong "Mulai"\nngaso 0\nngomong "Rampung"\n'
        )
        self.assertEqual(result, "Mulai\nRampung\n")

    def test_ngaso_requires_number(self):
        source = 'ngaso "sethik"\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_ngaso_rejects_negative(self):
        source = 'ngaso -1\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_ngaso_rejects_boolean(self):
        source = 'ngaso bener\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)


if __name__ == "__main__":
    unittest.main()
