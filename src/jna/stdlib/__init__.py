from ..functions import NativeFunction
from .functions import (
    dadi_teks, dadi_angka, dadi_bulat, dadi_koma,
    dawa, potong, ganti, goleki, resiki,
    mutlak, pangkat, bundele,
)


BUILTINS = (
    NativeFunction("dadi_teks", 1, 1, dadi_teks),
    NativeFunction("dadi_angka", 1, 1, dadi_angka),
    NativeFunction("dadi_bulat", 1, 1, dadi_bulat),
    NativeFunction("dadi_koma", 1, 1, dadi_koma),
    NativeFunction("dawa", 1, 1, dawa),
    NativeFunction("potong", 2, 3, potong),
    NativeFunction("ganti", 3, 3, ganti),
    NativeFunction("goleki", 2, 2, goleki),
    NativeFunction("resiki", 1, 1, resiki),
    NativeFunction("mutlak", 1, 1, mutlak),
    NativeFunction("pangkat", 2, 2, pangkat),
    NativeFunction("bundele", 1, 1, bundele),
)


def install_builtins(environment):
    for function in BUILTINS:
        environment.define(function.name, function)
