# JNA Language

JNA (Jawa Ngapak Absurd) yaiku basa pemrograman independen karo sintaks khas
Jawa Ngapak. Implementasi saiki ditulis nang Python (sethike 3.8) lan mung
nggunakake pustaka standar, dadi bisa mlaku nang Termux / ARMv7.

Dokumen iki mung njlentrehake fitur sing wis ana lan wis diimplementasikan.

## Instalasi

```bash
git clone https://github.com/Ndolzz/JNA-Language.git
cd JNA-Language
```

## Cara nglakokake

```bash
python -m src.jna examples/hello.jna
python -m src.jna examples/functions.jna
```

Ora ana dependensi eksternal; mung butuh Python 3 (nang Termux cukup
`pkg install python`).

## Kata kunci sing wis ana

| Kata kunci | Gunane |
| --- | --- |
| ngomong | Nampilake output |
| nek | Kondisi if |
| liyane | Kondisi else |
| baleni | Ulangan kaping tetep |
| gawe | Ngertinake fungsi |
| balekna | Ngembalikan nilai saka fungsi |
| bener | Boolean bener |
| salah | Boolean salah |
| kosong | Nilai kosong (null) |
| wis | Nggakhiri program |

Kata kunci `takon`, `mandheg`, `terusna`, lan `ngaso` wis ana nang lexer
nanging durung diimplementasikake nang parser lan interpreter.

## Tipe data

- Angka bulat lan koma, contone `10`, `3.5`
- Teks, contone `"Sugeng"`
- Boolean: `bener` lan `salah`
- Null: `kosong`

## Operator

- Aritmetika: `+`, `-`, `*`, `/`, `%`
- Komparasi: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Komentar baris nganggo `#`

## Variabel

```jna
jeneng = "Nendi"
umur = 16
```

## Kondisi

```jna
nek umur >= 17:
    ngomong "Wis dewasa"
liyane:
    ngomong "Durung dewasa"
```

## Perulangan

```jna
baleni 5:
    ngomong "JNA"
```

## Fungsi

```jna
gawe tambah(a, b):
    balekna a + b

asil = tambah(10, 5)
ngomong asil

gawe sapa(jeneng):
    ngomong "Sugeng rawuh, " + jeneng + "!"

sapa("Nendi")
```

Fungsi rekursif uga didukung:

```jna
gawe faktorial(n):
    nek n <= 1:
        balekna 1
    liyane:
        balekna n * faktorial(n - 1)
```

Aturan fungsi:

1. Jumlah argumen kudu cocog karo penataan parameter.
2. `balekna` mung bisa ana nang njero fungsi; tanpa nilai, asile `kosong`.
3. Variabel segera nang fungsi kapisah saka lingkup global.
4. Panggilan fungsi bisa dadi ekspresi utawa statement dhewe.
5. Rekursi diwatesi nganti 100 tingkat panggilan supaya metu error sing
   jelas, ora nglakokake stack Python.

## Pengujian

```bash
python -m unittest discover -s tests -v
```

## Struktur kode

```
src/jna/
  cli.py          # Titik masuk CLI
  lexer.py        # Tokenizer lan keyword
  parser.py       # Parser lan node AST
  interpreter.py  # Evaluasi program
  runtime.py      # Environment lan error runtime
  functions.py    # Representasi fungsi JNA
```

## Roadmap

1. Fase 1 (bahasa inti) umume wis ana; error runtime durung kabeh
   nduweni nomer baris.
2. Fase 2 (sistem fungsi) wis berjalan; standard library, `takon`,
   `mandheg`, `terusna`, lan `ngaso` isih ing antrean.
3. Compiler durung ana; pangembangan dimulai sawise interpreter stabil,
   awit saka analisis kode saiki (pyproject lan skema paket uga isih
   kosong).
