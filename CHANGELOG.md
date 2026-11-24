# Changelog

## 2026-11-24

### Ditambahake

- Dhaptar (list): literal `[...]`, indeks, penugasan indeks, nilai
  acuan, list kosong palsu; fungsi `tambahake`, `kethoke`, `sisipke`,
  `urute`; `dawa` saiki ngukur dhaptar uga.
- Contoh examples/lists.jna lan pengujian tests/test_lists.py.
- Dictionary: literal `{...}` mung kunci teks, akses/penugasan indeks,
  kunci dobel ditolak, dictionary kosong palsu; fungsi `ana` lan
  `dibusake`; `dawa` ngukur dictionary uga.
- Contoh examples/dicts.jna lan pengujian tests/test_dicts.py.
- String interpolation: `{jeneng}` nang string disilikake karo nilai
  variabel; `{{`/`}}` dadi kurung literal; kesalahan format metu error
  parser sing jelas.
- Contoh examples/interpolation.jna lan pengujian tests/test_interpolation.py.
- Fungsi utilitas: `acak` (acak bulat jegung kasebut), `acak_koma`
  (0.0 nganti 1.0), `wektu` (detik sejak 1970); `bundele` saiki suport
  jumlah desimal opsional.
- Kontrol alur: `mandheg` (break) lan `terusna` (continue) nang njero
  `baleni`, kalebu nested loop lan validasi penggunaan sing salah.
- Error sing jelas yen `mandheg`/`terusna` nang njaba `baleni` utawa
  nyoba nembus wates fungsi.
- Input lan wektu: `takon` (maca input, karo prompt opsional, asile
  tansah string) lan `ngaso` (ngaso program, durasi kudu angka
  non-negatif).
- Contoh examples/input.jna lan pengujian tests/test_input.py.
- Standard library pertama (12 fungsi built-in):
  `dadi_teks`, `dadi_angka`, `dadi_bulat`, `dadi_koma`, `dawa`,
  `potong`, `ganti`, `goleki`, `resiki`, `mutlak`, `pangkat`, `bundele`,
  dipasang nang environment global lan bisa dibayangi user.
- Modul anyar: src/jna/stdlib/ (functions.py, __init__.py) lan kelas
  NativeFunction nang src/jna/functions.py.
- Contoh examples/stdlib.jna lan pengujian tests/test_stdlib.py.
- Contoh examples/loops.jna lan pengujian tests/test_control_flow.py.

## 2026-11-23

### Ditambahake

- Sistem fungsi: deklarasi `gawe`, return `balekna`, pemanggilan fungsi
  dadi ekspresi lan statement, parametere posisi, validasi jumlah argumen.
- Lingkup lokal nang fungsi karo pangenalan global (parent chain).
- Fungsi nested lan rekursif karo watesan panggilan 100 tingkat,
  supaya tetep aman nang batas rekursi Python (khususe Termux/ARMv7).
- Node AST anyar: FunctionDef, Return, Call, ExpressionStatement.
- Pengujian fungsi nang tests/test_functions.py.
- Contoh examples/functions.jna, README.md, CHANGELOG.md.
