# Changelog

## 2026-11-24

### Ditambahake

- Kontrol alur: `mandheg` (break) lan `terusna` (continue) nang njero
  `baleni`, kalebu nested loop lan validasi penggunaan sing salah.
- Error sing jelas yen `mandheg`/`terusna` nang njaba `baleni` utawa
  nyoba nembus wates fungsi.
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
