# JNA Roadmap

## Fase 1 - Core Language

Selesai: lexer, token system, parser, AST, interpreter, runtime,
environment, error handling. Sisa kecil: sebagian error runtime belum
menyertakan nomor baris.

## Fase 2 - Function System

Selesai: deklarasi `gawe`, panggilan, parameter posisional, `balekna`,
lingkup lokal/global, fungsi nested, rekursi dengan batas kedalaman,
validasi argumen.

## Fase 3 - Control Flow

Selesai: if/else, repeat, `mandheg`, `terusna`, ulangan nested, dan
validasi alurnya.

## Fase 4 - Input dan Standard Library

Selesai: `takon`, konversi tipe, manipulasi teks, matematika, fungsi
dhaptar (bersama Fase 5), utilitas, `ngaso`, penanganan error standard
library.

## Fase 5 - Advanced Language Features

Selesai: dhaptar, dictionary, string interpolation, built-in functions.
Belum: module dan import, operasi berkas, penanganan exception, class,
type system statis.

## Fase 6 - Compiler Development

Belum dimulai: riset IR, bytecode, VM, compiler frontend/backend,
optimasi, dan distribusi executable. Dimulai setelah interpreter stabil
sepenuhnya.
