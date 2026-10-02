#!/usr/bin/env python3
"""Arma dist/: lo único que se publica (por ejemplo en GitHub Pages).

Para cada variante: genera la base, construye el SQL Lab y copia el dashboard base y los
materiales para los asistentes. NUNCA copia facilitadores/ (solo lleva las cosas listadas acá).

Uso (desde sesion_2/):
    python armar_dist.py             # todas las variantes registradas
    python armar_dist.py a-aerolineas

Solo biblioteca estándar.
"""
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
COMPARTIDO = os.path.join(AQUI, "compartido")
DIST = os.path.join(AQUI, "dist")
PDF = "INTRODUCCION SQL Y DATOS.pdf"

sys.path.insert(0, COMPARTIDO)
import build_lab  # noqa: E402

# nombre en dist -> (carpeta de la variante, título del Lab)
VARIANTES = {
    "a-aerolineas": ("variante-a", "Torre de control · Aerolíneas"),
    # "b-cnea": ("variante-b", "..."),   # se agrega cuando exista la variante B
}
MATERIALES = ("CONSIGNA.md", "TEORIA.md", "GUIA_IA.md")


def reescribir_links(texto):
    """En el repo el PDF está dos niveles arriba de material/; en dist, un nivel arriba de la variante."""
    texto = texto.replace("../../INTRODUCCION%20SQL%20Y%20DATOS.pdf", "../INTRODUCCION%20SQL%20Y%20DATOS.pdf")
    texto = texto.replace("(LINK_AL_LAB)", "(lab.html)")
    return texto


def armar(nombre):
    carpeta, titulo = VARIANTES[nombre]
    origen = os.path.join(AQUI, carpeta)
    sys.path.insert(0, origen)
    import build_db  # noqa: E402
    ruta_db = os.path.join(origen, "aerolineas.db")
    build_db.construir(ruta_db)
    build_lab.construir(nombre, ruta_db, titulo)
    destino = os.path.join(DIST, nombre)
    shutil.copy(os.path.join(COMPARTIDO, "dashboard_base.html"), os.path.join(destino, "dashboard_base.html"))
    for m in MATERIALES:
        with open(os.path.join(origen, "material", m), encoding="utf-8") as f:
            texto = reescribir_links(f.read())
        with open(os.path.join(destino, m), "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
    sys.path.remove(origen)
    sys.modules.pop("build_db", None)
    print("  %s: lab.html, dashboard_base.html, %s" % (nombre, ", ".join(MATERIALES)))


def main():
    pedidas = sys.argv[1:] or list(VARIANTES)
    desconocidas = [p for p in pedidas if p not in VARIANTES]
    if desconocidas:
        raise SystemExit("Variante desconocida: %s (disponibles: %s)" % (", ".join(desconocidas), ", ".join(VARIANTES)))
    os.makedirs(DIST, exist_ok=True)
    pdf = os.path.join(AQUI, PDF)
    if os.path.exists(pdf):
        shutil.copy(pdf, os.path.join(DIST, PDF))
    else:
        print("AVISO: falta '%s'. Generalo con compartido/build_pdf.mjs (el comando está en el encabezado de ese archivo)." % PDF)
    print("Armando dist/:")
    for nombre in pedidas:
        armar(nombre)
    # Resguardo: facilitadores no debe estar jamás en dist
    for raiz, dirs, archivos in os.walk(DIST):
        if "facilitadores" in dirs or any("SOLUCION" in a.upper() for a in archivos):
            raise SystemExit("ERROR: apareció material de facilitadores dentro de dist/ (%s)" % raiz)
    print("Listo. Publicá solamente la carpeta dist/.")


if __name__ == "__main__":
    main()
