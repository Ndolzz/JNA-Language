import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse, ParserError
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestInterpolation(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def parse_error(self, source):
        with self.assertRaises(ParserError):
            self.execute(source)

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_basic_interpolation(self):
        self.assertEqual(
            self.execute(
                'jeneng = "Nendi"\n'
                'ngomong "Sugeng, {jeneng}!"\n'
            ),
            ["Sugeng, Nendi!"]
        )

    def test_number_interpolation(self):
        self.assertEqual(
            self.execute(
                'umur = 16\n'
                'ngomong "Umure {umur} taun"\n'
            ),
            ["Umure 16 taun"]
        )

    def test_boolean_and_kosong_interpolation(self):
        self.assertEqual(
            self.execute(
                'tandha = bener\n'
                'wujud = kosong\n'
                'ngomong "{tandha}"\n'
                'ngomong "{wujud}"\n'
            ),
            ["bener", "kosong"]
        )

    def test_escaped_braces(self):
        self.assertEqual(
            self.execute('ngomong "Nilai: {{utuh}}"\n'),
            ["Nilai: {utuh}"]
        )

    def test_expression_in_braces_rejected(self):
        self.parse_error('a = 1\nb = 2\nngomong "{a+b}"\n')

    def test_unclosed_brace_rejected(self):
        self.parse_error('ngomong "{jeneng"\n')

    def test_stray_closing_brace_rejected(self):
        self.parse_error('ngomong "pasangan } salah"\n')

    def test_invalid_identifier_rejected(self):
        self.parse_error('ngomong "{jeneng umur}"\n')

    def test_unknown_variable_runtime_error(self):
        self.error('ngomong "{durung_ana}"\n')

    def test_interpolation_assigned_to_variable(self):
        self.assertEqual(
            self.execute(
                'pang = "Banyu"\n'
                'nulis = "{pang}mila"\n'
                'ngomong nulis\n'
            ),
            ["Banyumila"]
        )

    def test_interpolation_in_function(self):
        self.assertEqual(
            self.execute(
                'gawe sapa(jeneng):\n'
                '    balekna "Sugeng, {jeneng}!"\n'
                'ngomong sapa("Banyumila")\n'
            ),
            ["Sugeng, Banyumila!"]
        )

    def test_plain_strings_unchanged(self):
        self.assertEqual(
            self.execute('ngomong "Halo"\nngomong "tanpa kurung"\n'),
            ["Halo", "tanpa kurung"]
        )

    def test_stray_brace_pair_still_rejected(self):
        self.parse_error('ngomong "a} b{ c"\n')


if __name__ == "__main__":
    unittest.main()
