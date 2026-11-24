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
python -m src.jna examples/loops.jna
python -m src.jna examples/input.jna
python -m src.jna examples/stdlib.jna
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
| mandheg | Ngandegake baleni |
| terusna | Nerusake nang iterasi sabanjure |
| takon | Nampa input saka pengguna |
| ngaso | Ngaso sawetara wektu (detik) |
| wis | Nggakhiri program |

Elinga yen `takon` mesthi ngasilake teks (string); konversi tipe
bakal dadi bagean standard library nang fase sabanjure.

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

## Mandheg lan Terusna

Nang njero `baleni`, `mandheg` ngandegake ulangan lan `terusna`
mlumpat nang iterasi sabanjure. Kaduwe mung bisa ditulis nang njero
`baleni` lan ora bisa nembus wates fungsi.

```jna
angka = 0
baleni 5:
    angka = angka + 1
    nek angka == 3:
        terusna
    nek angka == 5:
        mandheg
    ngomong angka
```

Asile: `1`, `2`, `4`.

## Input lan Ngaso

`takon` maca sakbaris teks saka pengguna lan mesthi ngasilake string.
Bisa nganggo prompt sing ditampilake sakdurunge nunggu ketikan.

```jna
jeneng = takon "Siapa jenengmu?"
ngomong "Sugeng rawuh, " + jeneng + "!"
```

`ngaso` ngaso program sawetara detik. Durasi kudu angka sing ora
negatif, bisa bulat utawa koma.

```jna
ngomong "Nunggu sethik..."
ngaso 2
ngomong "Rampung"
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

## Standard Library

Fungsi-fungsi iki wis bisa diarani kaya fungsi biasa, dhisani
nganggo statement utawa nang njero ekspresi.

| Fungsi | Gunane |
| --- | --- |
| dadi_teks(nilai) | Ngonversi dadi teks |
| dadi_angka(nilai) | Ngonversi teks dadi angka |
| dadi_bulat(nilai) | Ngonversi dadi angka bulat (mbusak bagean desimal) |
| dadi_koma(nilai) | Ngonversi dadi angka koma |
| dawa(teks) | Ngetang dawa teks |
| potong(teks, wiwiti, pungkasan) | Njupuk bagean teks; pungkasan opsional |
| ganti(teks, wingi, anyar) | Ngganti kabeh teks sing wingi dadi anyar |
| goleki(teks, dicari) | Posisi kapisan; -1 yen ora ketemu |
| resiki(teks) | Mbuse spasi ing pinggir teks |
| mutlak(nilai) | Nilai absolut |
| pangkat(dasar, pangkat) | Dasar dipangkatke |
| bundele(nilai, cacah?) | Pondhokan ke angka paling cedhak; cacah desimal opsional |
| acak(wiwiti, pungkasan) | Angka acak bulat jegung kasebut |
| acak_koma() | Angka acak koma 0.0 nganti 1.0 |
| wektu() | Wektu saiki ing detik sejak 1970 |

```jna
ngomong dawa("Sugeng")
ngomong dadi_angka("42") + 8
ngomong pangkat(2, 10)
```

Argumen sing seler/type-e salah bakal metu error JNA sing jelas,
dhisani karo nomer baris.

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
2. Fase 4 wis lumayan: `takon`, `ngaso`, lan standard library pertama
   (konversi, teks, matematika) wis ana; fungsi list lan utilitas liyane
   isih ing antrean bareng fase list/dictionary.
3. Compiler durung ana; pangembangan dimulai sawise interpreter stabil,
   awit saka analisis kode saiki (pyproject lan skema paket uga isih
   kosong).
