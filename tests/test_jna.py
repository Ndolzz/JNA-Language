import unittest

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestJNA(unittest.TestCase):

    def execute(self, source):
        import io
        from contextlib import redirect_stdout

        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def test_print(self):
        self.assertEqual(
            self.execute('ngomong "Halo"\n'),
            ["Halo"]
        )

    def test_variable(self):
        self.assertEqual(
            self.execute(
                'jeneng = "Nendi"\nngomong jeneng\n'
            ),
            ["Nendi"]
        )

    def test_math(self):
        self.assertEqual(
            self.execute(
                'asil = 10 + 5\nngomong asil\n'
            ),
            ["15"]
        )

    def test_condition(self):
        self.assertEqual(
            self.execute(
                'nek 10 > 5:\n'
                '    ngomong "Bener"\n'
                'liyane:\n'
                '    ngomong "Salah"\n'
            ),
            ["Bener"]
        )

    def test_repeat(self):
        self.assertEqual(
            self.execute(
                'baleni 3:\n'
                '    ngomong "JNA"\n'
            ),
            ["JNA", "JNA", "JNA"]
        )

    def test_boolean(self):
        self.assertEqual(
            self.execute(
                'ngomong bener\nngomong salah\n'
            ),
            ["bener", "salah"]
        )

    def test_end(self):
        self.assertEqual(
            self.execute(
                'ngomong "Mulai"\n'
                'wis\n'
                'ngomong "Akhir"\n'
            ),
            ["Mulai"]
        )

    def test_mixed_type_comparison_rejected(self):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute('ngomong 1 < "x"\n')


if __name__ == "__main__":
    unittest.main()
