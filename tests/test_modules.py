import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestModules(unittest.TestCase):

    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory()
        self.base = self._temporary.name

    def tearDown(self):
        self._temporary.cleanup()

    def write(self, filename, content):
        path = os.path.join(self.base, filename)

        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter(self.base).run(program)

        return output.getvalue().splitlines()

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_ngunduh_imports_function(self):
        self.write(
            "sapaan.jna",
            'gawe sapa(jeneng):\n    balekna "Sugeng, " + jeneng\n',
        )
        self.assertEqual(
            self.execute('ngunduh "sapaan"\nngomong sapa("Nendi")\n'),
            ["Sugeng, Nendi"]
        )

    def test_extension_appended(self):
        self.write("modul.jna", "umur = 16\n")
        self.assertEqual(
            self.execute('ngunduh "modul"\nngomong umur\n'),
            ["16"]
        )

    def test_full_name_with_extension(self):
        self.write("angka.jna", "nomer = 7\n")
        self.assertEqual(
            self.execute('ngunduh "angka.jna"\nngomong nomer\n'),
            ["7"]
        )

    def test_module_not_rerun(self):
        self.write("siji.jna", 'ngomong "modul jalan"\n')
        source = 'ngunduh "siji"\nngunduh "siji"\n'
        self.assertEqual(self.execute(source), ["modul jalan"])

    def test_module_wis_ends_module_only(self):
        self.write(
            "potongan.jna",
            'ngomong "awal"\nwis\nngomong "akhir"\n',
        )
        self.assertEqual(
            self.execute('ngunduh "potongan"\nngomong "lajeng"\n'),
            ["awal", "lajeng"]
        )

    def test_circular_import(self):
        self.write("a.jna", 'ngunduh "b"\n')
        self.write("b.jna", 'ngunduh "a"\n')
        self.error('ngunduh "a"\n')

    def test_missing_module(self):
        self.error('ngunduh "ora_ana"\n')

    def test_module_closure_keeps_module_variables(self):
        self.write(
            "rupane.jna",
            "dhasar = 10\ngawe tambah(n):\n    balekna dhasar + n\n",
        )
        self.assertEqual(
            self.execute('ngunduh "rupane"\nngomong tambah(5)\n'),
            ["15"]
        )

    def test_module_name_must_be_text(self):
        self.error("ngunduh 5\n")

    def test_import_inside_function_scope(self):
        self.write("kerdhes.jna", "penanda = 42\n")
        self.assertEqual(
            self.execute(
                'gawe mbekto():\n'
                '    ngunduh "kerdhes"\n'
                '    balekna penanda\n'
                'ngomong mbekto()\n'
            ),
            ["42"]
        )


if __name__ == "__main__":
    unittest.main()
