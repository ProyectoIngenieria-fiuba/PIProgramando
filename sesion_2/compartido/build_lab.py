#!/usr/bin/env python3
"""Inyecta una base SQLite en el template del SQL Lab.

Uso:
    python build_lab.py <variante> <ruta_db> "<Título>"
Ejemplo:
    python build_lab.py a-aerolineas ../variante-a/aerolineas.db "Torre de control · Aerolíneas"

Escribe ../dist/<variante>/lab.html. Solo biblioteca estándar.
"""
import base64
import html
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(AQUI, "lab_template.html")
DIST = os.path.join(AQUI, "..", "dist")


def construir(variante, ruta_db, titulo):
    with open(TEMPLATE, encoding="utf-8") as f:
        plantilla = f.read()
    for marcador in ("__TITULO__", "__DB_BASE64__"):
        if marcador not in plantilla:
            raise SystemExit("El template no contiene el marcador " + marcador)
    with open(ruta_db, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    # __TITULO__ aparece en HTML (escapado) y en un string JS (escapado para JS).
    en_js = titulo.replace("\\", "\\\\").replace('"', '\\"')
    partes = plantilla.split('const TITULO = "__TITULO__";')
    if len(partes) != 2:
        raise SystemExit('No encontré la línea: const TITULO = "__TITULO__";')
    plantilla = partes[0].replace("__TITULO__", html.escape(titulo)) + 'const TITULO = "%s";' % en_js + \
        partes[1].replace("__TITULO__", html.escape(titulo))
    # Solo la línea del const: el marcador también se nombra en un comentario.
    linea_db = 'const DB_BASE64 = "__DB_BASE64__";'
    if plantilla.count(linea_db) != 1:
        raise SystemExit("No encontré la línea: " + linea_db)
    plantilla = plantilla.replace(linea_db, 'const DB_BASE64 = "%s";' % b64)

    destino_dir = os.path.normpath(os.path.join(DIST, variante))
    os.makedirs(destino_dir, exist_ok=True)
    destino = os.path.join(destino_dir, "lab.html")
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(plantilla)
    return destino


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    out = construir(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Lab generado: %s (%.0f KB)" % (out, os.path.getsize(out) / 1024))
