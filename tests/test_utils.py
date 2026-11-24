import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestUtils(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_acak_deterministic_bounds(self):
        self.assertEqual(
            self.execute(
                'ngomong acak(1, 1)\n'
                'ngomong acak(3, 3)\n'
            ),
            ["1", "3"]
        )

    def test_acak_within_range(self):
        source = (
            'cacah = 0\n'
            'baleni 50:\n'
            '    asil = acak(1, 6)\n'
            '    nek asil < 1:\n'
            '        ngomong "Ora sah"\n'
            '        mandheg\n'
            '    nek asil > 6:\n'
            '        ngomong "Ora sah"\n'
            '        mandheg\n'
            '    cacah = cacah + 1\n'
            'ngomong cacah\n'
        )
        self.assertEqual(self.execute(source), ["50"])

    def test_acak_rejects_reversed_range(self):
        self.error('acak(5, 1)\n')

    def test_acak_requires_integers(self):
        self.error('acak(1.5, 6)\n')

    def test_acak_koma_in_range(self):
        source = (
            'cacah = 0\n'
            'baleni 20:\n'
            '    asil = acak_koma()\n'
            '    nek asil < 0:\n'
            '        ngomong "Ora sah"\n'
            '        mandheg\n'
            '    nek asil >= 1:\n'
            '        ngomong "Ora sah"\n'
            '        mandheg\n'
            '    cacah = cacah + 1\n'
            'ngomong cacah\n'
        )
        self.assertEqual(self.execute(source), ["20"])

    def test_acak_koma_no_arguments(self):
        self.error('acak_koma(1)\n')

    def test_wektu_is_positive_number(self):
        source = (
            'nek wektu() > 0:\n'
            '    ngomong "bener"\n'
        )
        self.assertEqual(self.execute(source), ["bener"])

    def test_wektu_no_arguments(self):
        self.error('wektu(1)\n')

    def test_bundele_with_digits(self):
        self.assertEqual(
            self.execute(
                'ngomong bundele(3.14159, 2)\n'
                'ngomong bundele(0.125, 2)\n'
                'ngomong bundele(-2.103, 2)\n'
                'ngomong bundele(1.5, 0)\n'
            ),
            ["3.14", "0.13", "-2.1", "2"]
        )

    def test_bundele_digits_negative_rejected(self):
        self.error('bundele(3.14, -1)\n')


if __name__ == "__main__":
    unittest.main()
