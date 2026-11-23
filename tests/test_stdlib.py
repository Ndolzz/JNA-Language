import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestStdlib(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_dadi_teks(self):
        self.assertEqual(
            self.execute(
                'ngomong dadi_teks(3.5)\n'
                'ngomong dadi_teks(bener)\n'
                'ngomong dadi_teks(kosong)\n'
            ),
            ["3.5", "bener", "kosong"]
        )

    def test_dadi_angka_from_text(self):
        self.assertEqual(
            self.execute(
                'ngomong dadi_angka("12")\n'
                'ngomong dadi_angka("3.5")\n'
            ),
            ["12", "3.5"]
        )

    def test_dadi_angka_invalid(self):
        self.error('dadi_angka("pirang")\n')

    def test_dadi_angka_rejects_kosong(self):
        self.error('dadi_angka(kosong)\n')

    def test_dadi_bulat(self):
        self.assertEqual(
            self.execute(
                'ngomong dadi_bulat(3.7)\n'
                'ngomong dadi_bulat(-3.7)\n'
                'ngomong dadi_bulat("8")\n'
            ),
            ["3", "-3", "8"]
        )

    def test_dadi_koma(self):
        self.assertEqual(
            self.execute('ngomong dadi_koma("2.5")\n'),
            ["2.5"]
        )

    def test_dawa(self):
        self.assertEqual(
            self.execute('ngomong dawa("Sugeng")\n'),
            ["6"]
        )

    def test_dawa_requires_text(self):
        self.error('dawa(5)\n')

    def test_potong(self):
        self.assertEqual(
            self.execute(
                'ngomong potong("Ngapak", 0, 3)\n'
                'ngomong potong("Ngapak", 3)\n'
            ),
            ["Nga", "pak"]
        )

    def test_ganti(self):
        self.assertEqual(
            self.execute('ngomong ganti("satu satu", "satu", "loro")\n'),
            ["loro loro"]
        )

    def test_goleki(self):
        self.assertEqual(
            self.execute(
                'ngomong goleki("Ngapak", "pa")\n'
                'ngomong goleki("Ngapak", "xyz")\n'
            ),
            ["3", "-1"]
        )

    def test_resiki(self):
        self.assertEqual(
            self.execute('ngomong resiki("  JNA  ")\n'),
            ["JNA"]
        )

    def test_mutlak(self):
        self.assertEqual(
            self.execute('ngomong mutlak(-4)\nngomong mutlak(4)\n'),
            ["4", "4"]
        )

    def test_pangkat(self):
        self.assertEqual(
            self.execute(
                'ngomong pangkat(2, 3)\n'
                'ngomong pangkat(2, -1)\n'
            ),
            ["8", "0.5"]
        )

    def test_pangkat_zero_negative(self):
        self.error('pangkat(0, -2)\n')

    def test_bundele(self):
        self.assertEqual(
            self.execute(
                'ngomong bundele(2.5)\n'
                'ngomong bundele(-2.5)\n'
                'ngomong bundele(2.4)\n'
            ),
            ["3", "-3", "2"]
        )

    def test_wrong_arg_count(self):
        self.error('pangkat(2)\n')

    def test_call_non_function_unchanged(self):
        self.error('umur = 16\numur(2)\n')

    def test_user_function_shadows_builtin(self):
        self.assertEqual(
            self.execute(
                'gawe dawa(x):\n'
                '    balekna 99\n'
                'ngomong dawa("abanaban")\n'
            ),
            ["99"]
        )


if __name__ == "__main__":
    unittest.main()
