# JNA Syntax Guide

Panduan singkat sintaks JNA yang sudah tersedia. Rincian semantik ada
nang LANGUAGE_SPEC.md.

## Output dan Variabel

```jna
jeneng = "Nendi"
umur = 16

ngomong "Halo, " + jeneng
ngomong umur
```

## Kondisi

```jna
nek umur >= 17:
    ngomong "Wis dewasa"
liyane:
    ngomong "Durung dewasa"
```

## Ulangan

```jna
baleni 5:
ngomong "JNA"
```

dengan mandheg lan terusna:

```jna
baleni 5:
    mandheg
```

## Fungsi

```jna
gawe tambah(a, b):
    balekna a + b

asil = tambah(10, 5)
ngomong asil
```

## Interpolasi

```jna
ngomong "Sugeng rawuh, {jeneng}!"
```

## Dhaptar dan Dictionary

```jna
woh = ["mangga", "pelem"]
orang = {"jeneng": "Nendi", "umur": 16}

tambahake(woh, "jambu")
ngomong woh[0]
ngomong orang["jeneng"]
```

## Input lan Ngaso

```jna
jeneng = takon "Siapa jenengmu?"
ngaso 2
```

## Mengakhiri

```jna
ngomong "Mulai"
wis
ngomong "Durung kacapake"
```
