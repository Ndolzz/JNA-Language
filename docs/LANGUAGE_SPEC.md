# JNA Language Specification

Dokumen ini menjelaskan perilaku bahasa JNA sebagaimana diimplementasikan
sekarang. Fitur yang belum tersedia tidak didokumentasikan di sini.

## 1. Filosofi

JNA (Jawa Ngapak Absurd) adalah bahasa pemrograman prosedural dengan
sintaks Jawa Ngapak. Prioritas utamanya: kebenaran sebelum kemudahan,
stabilitas sebelum banyaknya fitur, dan setiap kesalahan harus keluar
sebagai pesan yang jelas.

## 2. Struktur Program

- Program berupa kumpulan statement per baris.
- Komentar baris diawali `#` dan diabaikan.
- Blok ditandai tanda titik dua (`:`) dan indentasi spasi; tab dilarang.
- `wis` menghentikan program lebih awal; boleh tidak ditulis di akhir.
- Baris kosong diabaikan.

## 3. Leksikal

### 3.1 Kata kunci

| Kata kunci | Fungsi |
| --- | --- |
| ngomong | Menampilkan nilai |
| takon | Menerima input satu baris |
| nek | Kondisi if |
| liyane | Kondisi else |
| baleni | Ulangan dengan jumlah tetap |
| gawe | Mendefinisikan fungsi |
| balekna | Mengembalikan nilai fungsi |
| bener | Boolean true |
| salah | Boolean false |
| kosong | Null |
| mandheg | Break |
| terusna | Continue |
| ngaso | Tidur sejenak (detik) |
| wis | Mengakhiri program |

### 3.2 Pengenal

Pengenal diawali huruf atau `_`, lalu huruf, angka, atau `_`. Kata
kunci tidak dapat menjadi pengenal.

### 3.3 Angka

Bulat (`42`) dan koma (`3.5`). Tanda minus tunggal adalah operator unary.

### 3.4 String

- Ditulis dengan `'` atau `"`.
- Escape: `\n` (baris baru), `\t` (tab), `\r`, `\\`, dan kutip.
- Interpolasi: `{jeneng}` diganti nilai variabel. Hanya nama variabel
  yang sah; tidak ada ekspresi. `{{` dan `}}` menjadi kurung literal.
  Format salah (kurung tidak ditutup, penutup lepas, nama tidak sah)
  adalah `ParserError` dengan nomor baris. Variabel belum ada adalah
  error runtime.

### 3.5 Operator

| Operator | Fungsi |
| --- | --- |
| + - * / % | Aritmetika |
| == != < > <= >= | Komparasi |
| = | Penugasan |
| [ ] | Literal dhaptar dan akses indeks |
| { } | Literal dictionary |
| ( ) , : | Panggilan, parameter, blok |

## 4. Tipe Data

| Tipe | Contoh | Catatan |
| --- | --- | --- |
| Bulat | 42 | |
| Koma | 3.5 | |
| Teks | "Sugeng" | Tidak berubah (immutable) |
| Boolean | bener / salah | |
| Kosong | kosong | Null |
| Dhaptar | [1, 2, 3] | Nilai acuan |
| Dictionary | {"jeneng": "Nendi"} | Nilai acuan; kunci wajib teks; kunci dobel ditolak |

Dhaptar dan dictionary adalah nilai acuan: mutasi terlihat dari semua
variabel yang menunjuk objek yang sama.

### 4.1 Persamaan

`==` dan `!=` berlaku untuk semua tipe. `< > <= >=` membutuhkan dua
nilai yang dapat dibandingkan (angka-angka atau teks-teks).

### 4.2 Kebenaran

Palsu: `kosong`, `salah`, dhaptar kosong, dictionary kosong.
Bener: lainnya, termasuk angka 0 dan teks kosong.

### 4.3 Tampilan Nilai

`ngomong` dan interpolasi menampilkan: `bener`, `salah`, `kosong`,
dhaptar bergaya `[1, 2, 3]`, dictionary bergaya `{jeneng: Nendi, umur: 16}`,
secara rekursif untuk isi bersarang.

## 5. Ekspresi

Prioritas dari tinggi ke rendah:

1. Akses indeks postfix: `woh[0]`, `dhaftar[0][1]`; berlaku untuk
   dhaptar, teks, dan dictionary (kunci teks).
2. Panggilan fungsi: `tambah(a, b)`, boleh bersarang.
3. Minus unary: `-nilai`.
4. Perkalian, pembagian, modulo: `*`, `/`, `%`.
5. Tambahan dan kurang: `+`, `-`.
6. Komparasi: `== != < > <= >=`.

Aritmetika hanya untuk angka; `+` antara dua teks menyambung.
Pembagian/modulo nol, indeks di luar rentang, indeks negatif, atau
indeks bukan bulat keluar sebagai error runtime.

## 6. Statement

### 6.1 Penugasan

`jeneng = nilai`. Penugasan indeks: `woh[0] = x` (dhaptar) dan
`orang["umur"] = 17` (dictionary, sekaligus menambah kunci baru).

### 6.2 Output dan Input

- `ngomong nilai` menampilkan nilai lalu baris baru.
- `takon` atau `takon "prompt"` membaca satu baris; hasil selalu teks.
  Kehabisan input (EOF) atau interupsi keluar sebagai error JNA.

### 6.3 Kondisi

```jna
nek kondisi:
    ...
liyane:
    ...
```

`liyane` opsional.

### 6.4 Ulangan

```jna
baleni kaping:
    ...
```

`kaping` wajib bulat non-negatif. `mandheg` menghentikan ulangan,
`terusna` melompat ke iterasi berikutnya. Keduanya hanya boleh di dalam
`baleni` dan tidak menembus batas fungsi, hanya menyentuh ulangan
terdalam.

### 6.5 Fungsi

```jna
gawe tambah(a, b):
    balekna a + b
```

- Parameter posisional; jumlah argumen harus sama.
- `balekna` tanpa nilai menghasilkan `kosong`; tanpa `balekna` juga `kosong`.
- Setiap panggilan membuat lingkup baru; fungsi boleh nested dan rekursif.
- Kedalaman panggilan maksimal 100; rekursi tanpa henti keluar sebagai
  error JNA, bukan kerusakan stack.
- Panggilan bisa berupa ekspresi atau statement sendiri.

### 6.6 Ngaso

`ngaso detik` menunda eksekusi; durasi wajib angka non-negatif.

### 6.7 Wis

`wis` menghentikan program di posisi mana pun, termasuk di dalam blok.

## 7. Lingkup

- Lingkup global tunggal; setiap panggilan fungsi membuat lingkup baru
  yang terhubung ke lingkup tempat fungsi didefinisikan (klosur).
- Penugasan di dalam fungsi membuat variabel lokal.
- Pencarian variabel naik dari lokal ke global.

## 8. Standard Library

21 fungsi terpasang di lingkup global dan dapat dibayangi fungsi `gawe`.
Jumlah, tipe, dan nilai argumen divalidasi; kesalahan keluar sebagai
error JNA.

- Konversi: `dadi_teks`, `dadi_angka`, `dadi_bulat`, `dadi_koma`
- Teks: `dawa`, `potong`, `ganti`, `goleki`, `resiki`
- Matematika: `mutlak`, `pangkat`, `bundele`
- Utilitas: `acak`, `acak_koma`, `wektu`
- Dhaptar: `tambahake`, `kethoke`, `sisipke`, `urute`
- Dictionary: `ana`, `dibusake`

Perilaku khusus:

- `dadi_bulat` membuang bagian desimal ke arah nol.
- `bundele` membulatkan setengah menjauh dari nol: `bundele(2.5) == 3`,
  `bundele(-2.5) == -3`; argumen kedua opsional mengatur jumlah desimal.
- `urute` menuntut seluruh isi sejenis (semua angka atau semua teks).
- `kethoke` dan `dibusake` mengembalikan nilai yang dibuang.
- `goleki` mengembalikan `-1` bila tidak ditemukan.
- Acak mengandalkan modul `random` Python; tidak untuk kriptografi.

## 9. Kesalahan

| Kelas | Sumber | Contoh |
| --- | --- | --- |
| LexerError | Teks program | karakter tak dikenal, tab indentasi, string tak ditutup |
| ParserError | Tata bahasa | token yang tidak diharapkan, kurung tak ditutup, parameter dobel |
| RuntimeErrorJNA | Eksekusi | variabel belum ada, indeks di luar rentang, argumen salah, rekursi melebihi batas |

Ketiganya ditampilkan CLI dengan awalan `JNA Error:` pada alur penerangan
kesalahan (stderr).
