import io
import unittest
from contextlib import redirect_stdin, redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestInput(unittest.TestCase):

    def execute(self, source, stdin_text=None):
        output = io.StringIO()
        stdin_source = io.StringIO(stdin_text) if stdin_text is not None else io.StringIO()

        with redirect_stdout(output), redirect_stdin(stdin_source):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue()

    def test_takon_returns_string(self):
        result = self.execute(
            'jeneng = takon\nngomong jeneng\n',
            stdin_text="Nendi\n",
        )
        self.assertEqual(result, "Nendi\n")

    def test_takon_with_prompt(self):
        result = self.execute(
            'jeneng = takon "Siapa jenengmu?"\nngomong jeneng\n',
            stdin_text="Nendi\n",
        )
        self.assertEqual(result, "Siapa jenengmu?Nendi\n")

    def test_takon_value_is_string(self):
        result = self.execute(
            'umur = takon\nngomong umur + " taun"\n',
            stdin_text="16\n",
        )
        self.assertEqual(result, "16 taun\n")

    def test_takon_at_end_of_input(self):
        source = 'jeneng = takon\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source, stdin_text="")

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
