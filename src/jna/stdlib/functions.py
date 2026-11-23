import math

from ..runtime import RuntimeErrorJNA, stringify


def fail(message, line):
    if line:
        raise RuntimeErrorJNA(f"{message} pada baris {line}")

    raise RuntimeErrorJNA(message)


def require_text(name, value, line):
    if not isinstance(value, str):
        fail(f"'{name}' butuh teks", line)

    return value


def require_number(name, value, line):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"'{name}' butuh angka", line)

    return value


def require_integer(name, value, line):
    if isinstance(value, bool) or not isinstance(value, int):
        fail(f"'{name}' butuh angka bulat", line)

    return value


# KONVERSI

def dadi_teks(arguments, line):
    return stringify(arguments[0])


def dadi_angka(arguments, line):
    value = arguments[0]

    if isinstance(value, bool):
        fail("'dadi_angka' ora bisa ngubah boolean", line)

    if isinstance(value, (int, float)):
        return value

    if not isinstance(value, str):
        fail("'dadi_angka' ora bisa ngubah nilai iki", line)

    text = value.strip()

    try:
        return int(text)
    except ValueError:
        pass

    try:
        return float(text)
    except ValueError:
        fail(f"'{value}' ora bisa dadi angka", line)


def dadi_bulat(arguments, line):
    value = arguments[0]

    if isinstance(value, bool):
        fail("'dadi_bulat' ora bisa ngubah boolean", line)

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    if not isinstance(value, str):
        fail("'dadi_bulat' ora bisa ngubah nilai iki", line)

    text = value.strip()

    try:
        return int(text)
    except ValueError:
        pass

    try:
        return int(float(text))
    except ValueError:
        fail(f"'{value}' ora bisa dadi angka bulat", line)


def dadi_koma(arguments, line):
    value = arguments[0]

    if isinstance(value, bool):
        fail("'dadi_koma' ora bisa ngubah boolean", line)

    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        fail("'dadi_koma' ora bisa ngubah nilai iki", line)

    try:
        return float(value.strip())
    except ValueError:
        fail(f"'{value}' ora bisa dadi angka koma", line)


# TEKS

def dawa(arguments, line):
    value = arguments[0]

    if not isinstance(value, str):
        fail("'dawa' munggo ngukur teks", line)

    return len(value)


def potong(arguments, line):
    teks = require_text("potong", arguments[0], line)
    wiwiti = require_integer("potong", arguments[1], line)

    if len(arguments) == 2:
        return teks[wiwiti:]

    pungkasan = require_integer("potong", arguments[2], line)
    return teks[wiwiti:pungkasan]


def ganti(arguments, line):
    teks = require_text("ganti", arguments[0], line)
    wingi = require_text("ganti", arguments[1], line)
    anyar = require_text("ganti", arguments[2], line)

    return teks.replace(wingi, anyar)


def goleki(arguments, line):
    teks = require_text("goleki", arguments[0], line)
    dicari = require_text("goleki", arguments[1], line)

    return teks.find(dicari)


def resiki(arguments, line):
    teks = require_text("resiki", arguments[0], line)

    return teks.strip()


# MATEMATIKA

def mutlak(arguments, line):
    value = require_number("mutlak", arguments[0], line)

    return abs(value)


def pangkat(arguments, line):
    dasar = require_number("pangkat", arguments[0], line)
    pangkat = require_number("pangkat", arguments[1], line)

    if dasar == 0 and pangkat < 0:
        fail("Ora bisa 0 dipangkatke angka negatif", line)

    return dasar ** pangkat


def bundele(arguments, line):
    value = require_number("bundele", arguments[0], line)

    if value >= 0:
        return math.floor(value + 0.5)

    return math.ceil(value - 0.5)
