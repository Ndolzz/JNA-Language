# JNA Architecture

Alur eksekusi: sumber `.jna` diliwati empat tahapan berurutan di CLI.

```
source (teks)
  -> lexer.py      # tokenize: kata kunci, angka, string, operator, indentasi
  -> parser.py     # parse: AST node + validasi tata bahasa
  -> interpreter.py# eksekusi AST
  -> output
```

## Modul

| Modul | Tanggung jawab |
| --- | --- |
| cli.py | Titik masuk; menangani error dan kode keluar |
| lexer.py | Pembuatan token, aturan indentasi, escape, kata kunci |
| parser.py | Node AST (dataclass) dan pembentukannya; interpolasi string dibentuk di sini |
| interpreter.py | Evaluasi AST, kontrol alur, batas kedalaman |
| runtime.py | Environment (rantai lingkup), error runtime, aturan tampilan nilai |
| functions.py | JNAFunction (fungsi user) dan NativeFunction (built-in) |
| stdlib/ | Implementasi 21 fungsi built-in dan registrynya |

## Keputusan Desain

1. Lingkup memakai rantai Environment (lokal menunjuk parent); fungsi
   menyimpan lingkup penutupnya (klosur), sehingga rekursi dan nested
   function bekerja tanpa aturan khusus.
2. Fungsi user (JNAFunction) dan built-in (NativeFunction) dipanggil
   melalui jalur yang sama di evaluator; built-in dipasang di lingkup
   global sehingga statement penugasan biasa bisa membayanginya.
3. Kontrol alur (mandheg/terusna/balekna) memakai sinyal exception
   internal; batas lingkaran dijaga oleh penghitung di interpreter dan
   sinyal liar dikonversi menjadi error JNA yang jelas.
4. Interpolasi string dibentuk di parser (bukan lexer) agar aturan
   escape `{{`/`}}` dan validasi pengenal terjadi satu kali.
5. Aritmetika dan perbandingan diperiksa tipe-nya secara eksplisit;
   error Python tidak dibiarkan bocor ke pengguna.

## Ke Arah Compiler

Interpreter saat ini langsung mengeksekusi AST. Struktur node yang
terpisah dari runtime adalah dasar untuk tahap kompilasi (IR, bytecode,
VM) kelak. Belum ada IR, bytecode, maupun VM; dan belum ada klaim
bahwa JNA bisa dikompilasi.
