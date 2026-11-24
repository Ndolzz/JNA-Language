import math
import random
import time

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

    if isinstance(value, (str, list)):
        return len(value)

    fail("'dawa' munggo ngukur teks lan dhaptar", line)


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

    if len(arguments) == 1:
        return round_half_away(value, 1)

    cacah = require_integer("bundele", arguments[1], line)

    if cacah < 0:
        fail("'bundele' butuh cacah desimal ora negatif", line)

    if cacah == 0:
        return round_half_away(value, 1)

    return round_half_away(value, 10 ** cacah) / (10 ** cacah)


def round_half_away(value, skala):
    if value >= 0:
        return math.floor(value * skala + 0.5)

    return math.ceil(value * skala - 0.5)


# UTILITAS

def acak(arguments, line):
    wiwiti = require_integer("acak", arguments[0], line)
    pungkasan = require_integer("acak", arguments[1], line)

    if wiwiti > pungkasan:
        fail("'acak' butuh wiwiti ora luwih gedhe tinimbang pungkasan", line)

    return random.randint(wiwiti, pungkasan)


def acak_koma(arguments, line):
    return random.random()


def wektu(arguments, line):
    return time.time()


# DHAPTAR

def require_list(name, value, line):
    if not isinstance(value, list):
        fail(f"'{name}' butuh dhaptar", line)

    return value


def tambahake(arguments, line):
    dhaptar = require_list("tambahake", arguments[0], line)
    dhaptar.append(arguments[1])


def kethoke(arguments, line):
    dhaptar = require_list("kethoke", arguments[0], line)
    indeks = require_integer("kethoke", arguments[1], line)

    if indeks < 0 or indeks >= len(dhaptar):
        fail(f"Indeks {indeks} ngluwihi dawa dhaptar sing {len(dhaptar)}", line)

    return dhaptar.pop(indeks)


def sisipke(arguments, line):
    dhaptar = require_list("sisipke", arguments[0], line)
    indeks = require_integer("sisipke", arguments[1], line)
    value = arguments[2]

    if indeks < 0 or indeks > len(dhaptar):
        fail(f"Indeks {indeks} ora sah kanggo dhaptar sing dawa {len(dhaptar)}", line)

    dhaptar.insert(indeks, value)


def urute(arguments, line):
    dhaptar = require_list("urute", arguments[0], line)

    if not dhaptar:
        return dhaptar

    kabeh_angka = all(
        not isinstance(item, bool) and isinstance(item, (int, float))
        for item in dhaptar
    )
    kabeh_teks = all(isinstance(item, str) for item in dhaptar)

    if not kabeh_angka and not kabeh_teks:
        fail("'urute' butuh kabeh isine sejenis angka utawa teks", line)

    dhaptar.sort()

    return dhaptar
