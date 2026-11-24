import io
import unittest
from contextlib import redirect_stdout

from src.jna.lexer import tokenize
from src.jna.parser import parse
from src.jna.interpreter import Interpreter
from src.jna.runtime import RuntimeErrorJNA


class TestLists(unittest.TestCase):

    def execute(self, source):
        output = io.StringIO()

        with redirect_stdout(output):
            program = parse(tokenize(source))
            Interpreter().run(program)

        return output.getvalue().splitlines()

    def error(self, source):
        with self.assertRaises(RuntimeErrorJNA):
            self.execute(source)

    def test_list_literal_print(self):
        self.assertEqual(
            self.execute('woh = [1, 2, 3]\nngomong woh\n'),
            ["[1, 2, 3]"]
        )

    def test_empty_list(self):
        self.assertEqual(
            self.execute('dhasar = []\nngomong dhasar\nngomong dawa(dhasar)\n'),
            ["[]", "0"]
        )

    def test_nested_list_print(self):
        self.assertEqual(
            self.execute('ngomong [[1], bener, kosong]\n'),
            ["[[1], bener, kosong]"]
        )

    def test_index_read_list_and_text(self):
        self.assertEqual(
            self.execute(
                'woh = ["mangga", "pelem"]\n'
                'ngomong woh[1]\n'
                'ngomong "Ngapak"[0]\n'
            ),
            ["pelem", "N"]
        )

    def test_index_read_out_of_range(self):
        self.error('woh = [1]\nngomong woh[5]\n')

    def test_index_read_negative(self):
        self.error('woh = [1]\nngomong woh[-1]\n')

    def test_index_read_on_number(self):
        self.error('asil = 5\nngomong asil[0]\n')

    def test_index_assignment(self):
        self.assertEqual(
            self.execute('woh = [1, 2]\nwoh[1] = 9\nngomong woh\n'),
            ["[1, 9]"]
        )

    def test_index_assignment_out_of_range(self):
        self.error('woh = [1]\nwoh[1] = 9\n')

    def test_index_assignment_on_non_list(self):
        self.error('a = 5\na[0] = 1\n')

    def test_reference_semantics(self):
        self.assertEqual(
            self.execute(
                'a = [1]\n'
                'b = a\n'
                'tambahake(b, 3)\n'
                'ngomong dawa(a)\n'
            ),
            ["2"]
        )

    def test_kethoke_returns_removed(self):
        self.assertEqual(
            self.execute(
                'woh = ["mangga", "pelem"]\n'
                'ngomong kethoke(woh, 0)\n'
                'ngomong woh\n'
            ),
            ["mangga", "[pelem]"]
        )

    def test_sisipke(self):
        self.assertEqual(
            self.execute(
                'woh = ["a", "c"]\n'
                'sisipke(woh, 1, "b")\n'
                'ngomong woh\n'
            ),
            ["[a, b, c]"]
        )

    def test_urute_numbers_and_text(self):
        self.assertEqual(
            self.execute(
                'angka = [3, 1, 2]\n'
                'urute(angka)\n'
                'ngomong angka\n'
                'teks = ["c", "a"]\n'
                'urute(teks)\n'
                'ngomong teks\n'
            ),
            ["[1, 2, 3]", "[a, c]"]
        )

    def test_urute_mixed_rejected(self):
        self.error('urute(["a", 1])\n')

    def test_empty_list_falsy(self):
        self.assertEqual(
            self.execute(
                'kosongnane = []\n'
                'nek kosongnane:\n'
                '    ngomong "ana"\n'
                'liyane:\n'
                '    ngomong "ora ono"\n'
            ),
            ["ora ono"]
        )

    def test_list_mutation_across_function(self):
        self.assertEqual(
            self.execute(
                'woh = []\n'
                'gawe nambah():\n'
                '    tambahake(woh, 1)\n'
                'nambah()\n'
                'ngomong dawa(woh)\n'
            ),
            ["1"]
        )

    def test_index_in_condition(self):
        self.assertEqual(
            self.execute(
                'woh = [5, 9]\n'
                'nek woh[1] > 5:\n'
                '    ngomong "gedhe"\n'
            ),
            ["gedhe"]
        )


if __name__ == "__main__":
    unittest.main()
