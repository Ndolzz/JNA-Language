import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestControlFlow(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def test_mandheg_stops_loop(self):
        source = (
            'baleni 5:\n'
            '    ngomong "JNA"\n'
            '    mandheg\n'
        )
        self.assertEqual(self.execute(source), ["JNA"])

    def test_terusna_skips_iteration(self):
        source = (
            'angka = 0\n'
            'baleni 5:\n'
            '    angka = angka + 1\n'
            '    nek angka == 3:\n'
            '        terusna\n'
            '    ngomong angka\n'
        )
        self.assertEqual(self.execute(source), ["1", "2", "4", "5"])

    def test_nested_loop_break_inner_only(self):
        source = (
            'baleni 2:\n'
            '    ngomong "Luar"\n'
            '    baleni 2:\n'
            '        ngomong "Jero"\n'
            '        mandheg\n'
        )
        self.assertEqual(
            self.execute(source),
            ["Luar", "Jero", "Luar", "Jero"]
        )

    def test_nested_loop_continue_inner_only(self):
        source = (
            'baleni 2:\n'
            '    ngomong "Luar"\n'
            '    baleni 1:\n'
            '        ngomong "Jero"\n'
            '        terusna\n'
        )
        self.assertEqual(
            self.execute(source),
            ["Luar", "Jero", "Luar", "Jero"]
        )

    def test_mandheg_outside_loop(self):
        source = 'mandheg\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_terusna_outside_loop(self):
        source = 'terusna\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_mandheg_cannot_cross_function_boundary(self):
        source = (
            'baleni 2:\n'
            '    gawe entek():\n'
            '        mandheg\n'
            '    entek()\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_terusna_cannot_cross_function_boundary(self):
        source = (
            'baleni 2:\n'
            '    gawe entek():\n'
            '        terusna\n'
            '    entek()\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)


if __name__ == "__main__":
    unittest.main()
