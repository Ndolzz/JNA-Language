import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestDicts(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_dict_literal_print(self):
        self.assertEqual(
            self.execute(
                'orang = {"jeneng": "Nendi", "umur": 16}\n'
                'ngomong orang\n'
            ),
            ["{jeneng: Nendi, umur: 16}"]
        )

    def test_empty_dict(self):
        self.assertEqual(
            self.execute(
                'kosongnane = {}\n'
                'ngomong kosongnane\n'
                'ngomong dawa(kosongnane)\n'
            ),
            ["{}", "0"]
        )

    def test_dict_read(self):
        self.assertEqual(
            self.execute(
                'orang = {"jeneng": "Nendi"}\n'
                'ngomong orang["jeneng"]\n'
            ),
            ["Nendi"]
        )

    def test_dict_read_missing_key(self):
        self.error('orang = {"jeneng": "Nendi"}\nngomong orang["umur"]\n')

    def test_dict_non_text_key_rejected(self):
        self.error('a = {1: 2}\n')

    def test_dict_duplicate_key_rejected(self):
        self.error('a = {"x": 1, "x": 2}\n')

    def test_dict_assign_update_and_insert(self):
        self.assertEqual(
            self.execute(
                'orang = {"umur": 16}\n'
                'orang["umur"] = 17\n'
                'orang["kota"] = "Purwokerto"\n'
                'ngomong orang["umur"]\n'
                'ngomong orang["kota"]\n'
            ),
            ["17", "Purwokerto"]
        )

    def test_ana_on_dict(self):
        self.assertEqual(
            self.execute(
                'orang = {"umur": 16}\n'
                'ngomong ana(orang, "umur")\n'
                'ngomong ana(orang, "dhuwur")\n'
            ),
            ["bener", "salah"]
        )

    def test_ana_on_list(self):
        self.assertEqual(
            self.execute(
                'woh = ["mangga"]\n'
                'ngomong ana(woh, "mangga")\n'
                'ngomong ana(woh, "pelem")\n'
            ),
            ["bener", "salah"]
        )

    def test_ana_on_number_rejected(self):
        self.error('ana(5, 1)\n')

    def test_dawa_dict(self):
        self.assertEqual(
            self.execute(
                'orang = {"a": 1, "b": 2}\n'
                'ngomong dawa(orang)\n'
            ),
            ["2"]
        )

    def test_dibusake(self):
        self.assertEqual(
            self.execute(
                'orang = {"a": 1, "b": 2}\n'
                'ngomong dibusake(orang, "a")\n'
                'ngomong dawa(orang)\n'
            ),
            ["1", "1"]
        )

    def test_dibusake_missing_key(self):
        self.error('dibusake({"a": 1}, "z")\n')

    def test_empty_dict_falsy(self):
        self.assertEqual(
            self.execute(
                'kosongnane = {}\n'
                'nek kosongnane:\n'
                '    ngomong "ana"\n'
                'liyane:\n'
                '    ngomong "ora ono"\n'
            ),
            ["ora ono"]
        )

    def test_nested_print(self):
        self.assertEqual(
            self.execute('ngomong {"taun": [2024, 2025]}\n'),
            ["{taun: [2024, 2025]}"]
        )

    def test_dict_inside_list(self):
        self.assertEqual(
            self.execute(
                'dhaftar = [{"a": 1}]\n'
                'ngomong dhaftar[0]["a"]\n'
            ),
            ["1"]
        )

    def test_dict_mutation_across_function(self):
        self.assertEqual(
            self.execute(
                'gawe tambah_umur(orang):\n'
                '    orang["umur"] = orang["umur"] + 1\n'
                'orang = {"umur": 16}\n'
                'tambah_umur(orang)\n'
                'ngomong orang["umur"]\n'
            ),
            ["17"]
        )


if __name__ == "__main__":
    unittest.main()
