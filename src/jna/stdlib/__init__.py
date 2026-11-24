from ..functions import NativeFunction
from .functions import (
    dadi_teks, dadi_angka, dadi_bulat, dadi_koma,
    dawa, potong, ganti, goleki, resiki,
    mutlak, pangkat, bundele,
    acak, acak_koma, wektu,
    tambahake, kethoke, sisipke, urute,
    ana, dibusake,
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
    NativeFunction("bundele", 1, 2, bundele),
    NativeFunction("acak", 2, 2, acak),
    NativeFunction("acak_koma", 0, 0, acak_koma),
    NativeFunction("wektu", 0, 0, wektu),
    NativeFunction("tambahake", 2, 2, tambahake),
    NativeFunction("kethoke", 2, 2, kethoke),
    NativeFunction("sisipke", 3, 3, sisipke),
    NativeFunction("urute", 1, 1, urute),
    NativeFunction("ana", 2, 2, ana),
    NativeFunction("dibusake", 2, 2, dibusake),
)


def install_builtins(environment):
    for function in BUILTINS:
        environment.define(function.name, function)
