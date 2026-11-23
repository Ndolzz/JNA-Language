import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestFunctions(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def test_function_call_and_return(self):
        source = (
            'gawe tambah(a, b):\n'
            '    balekna a + b\n'
            'asil = tambah(10, 5)\n'
            'ngomong asil\n'
        )
        self.assertEqual(self.execute(source), ["15"])

    def test_function_without_return_gives_kosong(self):
        source = (
            'gawe sapa(jeneng):\n'
            '    ngomong "Sugeng, " + jeneng\n'
            'asil = sapa("Nendi")\n'
            'ngomong asil\n'
        )
        self.assertEqual(
            self.execute(source),
            ["Sugeng, Nendi", "kosong"]
        )

    def test_call_statement(self):
        source = (
            'gawe sapa(jeneng):\n'
            '    ngomong "Sugeng, " + jeneng\n'
            'sapa("Nendi")\n'
        )
        self.assertEqual(self.execute(source), ["Sugeng, Nendi"])

    def test_wrong_argument_count(self):
        source = (
            'gawe tambah(a, b):\n'
            '    balekna a + b\n'
            'tambah(1)\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_call_non_function(self):
        source = (
            'umur = 16\n'
            'umur(2)\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_local_scope_does_not_leak(self):
        source = (
            'gawe durung_digawe():\n'
            '    lokal = 99\n'
            '    balekna lokal\n'
            'asil = durung_digawe()\n'
            'ngomong asil\n'
            'ngomong lokal\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_global_variable_visible_in_function(self):
        source = (
            'umur = 16\n'
            'gawe deleng_umur():\n'
            '    balekna umur\n'
            'ngomong deleng_umur()\n'
        )
        self.assertEqual(self.execute(source), ["16"])

    def test_recursion(self):
        source = (
            'gawe faktorial(n):\n'
            '    nek n <= 1:\n'
            '        balekna 1\n'
            '    liyane:\n'
            '        balekna n * faktorial(n - 1)\n'
            'ngomong faktorial(5)\n'
        )
        self.assertEqual(self.execute(source), ["120"])

    def test_nested_functions(self):
        source = (
            'gawe luar(n):\n'
            '    gawe njero(n):\n'
            '        balekna n * 2\n'
            '    balekna njero(n) + 1\n'
            'ngomong luar(10)\n'
        )
        self.assertEqual(self.execute(source), ["21"])

    def test_balekna_outside_function(self):
        source = 'balekna 1\n'
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_balekna_without_value(self):
        source = (
            'gawe apa_bae(n):\n'
            '    nek n > 0:\n'
            '        balekna\n'
            'ngomong apa_bae(5)\n'
        )
        self.assertEqual(self.execute(source), ["kosong"])

    def test_deep_recursion_reports_error(self):
        source = (
            'gawe durung_entek(n):\n'
            '    balekna durung_entek(n + 1)\n'
            'durung_entek(1)\n'
        )
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)


if __name__ == "__main__":
    unittest.main()
