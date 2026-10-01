#!/usr/bin/env python3
"""Completa los resultados de material/TEORIA.md ejecutando sus consultas.

Los ejemplos de la teoría usan un club de barrio inventado (no la base de aerolíneas):
corren sobre una base vacía en memoria, así que acá no hay nada de la solución.

Uso (desde variante-a/):  python generar_teoria.py
"""
import os
import sqlite3
import sys

import solucion_util as su

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material", "TEORIA.md")


def main():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    texto = open(RUTA, encoding="utf-8").read()
    try:
        salida = su.completar(texto, con)
    except RuntimeError as e:
        sys.exit("ERROR: %s" % e)
    with open(RUTA, "w", encoding="utf-8", newline="\n") as f:
        f.write(salida)
    print("TEORIA.md actualizado: %d bloques ejecutados" % len(su.bloques(salida)))


if __name__ == "__main__":
    main()
