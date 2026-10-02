#!/usr/bin/env python3
"""Arma lo que usan los participantes de la variante A, desde cero y en un paso.

    1) genera la base (herramientas/aerolineas.db, determinística)
    2) construye ../lab.html con esa base embebida
    3) vuelve a calcular los resultados de ../TEORIA.md

Uso (desde variante-a/herramientas/):
    python armar.py

Otros comandos (todos desde variante-a/herramientas/):
    python verify_db.py                      verifica base, trampas, hallazgos, determinismo, TEORIA y SOLUCION
    python ../facilitadores/generar_solucion.py   recalcula facilitadores/SOLUCION.md (solo en tu máquina)

Tests en navegador y PDF (usan el runner "browser-automation"; <SK> = ruta a su browser.mjs):
    node <SK> "file:///RUTA/sesion_2/variante-a/lab.html"            --script ./test_lab.mjs
    node <SK> "file:///RUTA/sesion_2/variante-a/dashboard_base.html" --script ./test_dashboard.mjs
    node <SK> "file:///RUTA/sesion_2/variante-a/herramientas/introduccion_sql.html" --script ./build_pdf.mjs

Solo biblioteca estándar.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import build_db  # noqa: E402
import build_lab  # noqa: E402
import generar_teoria  # noqa: E402

TITULO = "Torre de control · Aerolíneas"


def main():
    ruta_db = os.path.join(AQUI, "aerolineas.db")
    build_db.construir(ruta_db)
    print("Base generada. SHA-256: %s" % build_db.sha256(ruta_db))
    print(build_lab.construir(ruta_db, TITULO))
    generar_teoria.main()
    print("Listo. Para participantes: lab.html, dashboard_base.html, CONSIGNA.md, TEORIA.md, GUIA_IA.md y el PDF.")


if __name__ == "__main__":
    main()
