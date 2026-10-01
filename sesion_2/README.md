# Sesión 2 · Análisis de datos con SQL (taller PIP)

Cada escuadra responde un pedido de negocio con **SQL sobre una base ficticia**, todo en el
navegador (SQLite + sql.js, sin instalar nada) y con ayuda de IA. Hay **dos variantes** del mismo
proyecto (empresa y datos distintos) para repartir entre escuadras:

| Variante | Empresa | Estado |
|---|---|---|
| **A** · `variante-a/` | Aerolínea ficticia, "Torre de control" | ✅ lista |
| **B** | CNEA, distribución de radioisótopos | pendiente (lo compartido ya es reutilizable) |

> Todos los datos son **ficticios**. No tienen relación con los sistemas reales de Aerolíneas Argentinas ni de ninguna otra empresa.

## Estructura

```
sesion_2/
├── INTRODUCCION SQL Y DATOS.pdf   pre-lectura para los asistentes (igual que la de sesion_1)
├── armar_dist.py                  arma dist/ (lo único que se publica)
├── compartido/                    agnóstico de la variante: se reutiliza en la B
│   ├── lab_template.html          SQL Lab genérico (placeholders __TITULO__ y __DB_BASE64__)
│   ├── build_lab.py               inyecta una base en el template -> dist/<variante>/lab.html
│   ├── dashboard_base.html        dashboard con Chart.js donde pegan sus JSON
│   ├── introduccion_sql.html      fuente del PDF
│   ├── build_pdf.mjs              imprime ese HTML a PDF
│   ├── test_lab.mjs               test automatizado del Lab
│   └── test_dashboard.mjs         test automatizado del dashboard
├── variante-a/
│   ├── build_db.py                genera aerolineas.db (determinístico, semilla fija)
│   ├── verify_db.py               verifica la base, TEORIA.md y las consultas de SOLUCION.md
│   ├── solucion_util.py           mecánica compartida por los verificadores/generadores
│   ├── generar_teoria.py          pega los resultados reales en material/TEORIA.md
│   ├── material/                  CONSIGNA.md, TEORIA.md, GUIA_IA.md  (para los asistentes)
│   └── facilitadores/             ⚠️ NO SE PUBLICA (ver abajo)
│       ├── SOLUCION.src.md        fuente de la solución (a mano)
│       ├── generar_solucion.py    ejecuta cada consulta y genera SOLUCION.md con resultados reales
│       └── SOLUCION.md            solución, mapa de trampas, hallazgos, pistas, rúbrica
└── dist/                          ✅ lo único que se publica
    ├── INTRODUCCION SQL Y DATOS.pdf
    └── a-aerolineas/              lab.html, dashboard_base.html, CONSIGNA.md, TEORIA.md, GUIA_IA.md
```

## ⚠️ Facilitadores: no se publica

Este repo es **público**. `facilitadores/` está en [.gitignore](.gitignore), así que **git no lo sube**.
Consecuencias:

- Las soluciones viven **solo en tu máquina**: hagan una copia de seguridad aparte (o pasen la carpeta a un repo privado).
- En un clon del repo no existe `facilitadores/`: `verify_db.py` lo avisa y omite esa parte (el resto sigue verificando).
- `armar_dist.py` solo copia los archivos que lista y **aborta** si aparece algo de facilitadores dentro de `dist/`.
- Ojo: las `SOLUCION.md` de `sesion_1/` **sí están commiteadas** en el repo público.

## Requisitos

- **Python 3.9+** (solo biblioteca estándar, `sqlite3` con funciones de ventana: SQLite ≥ 3.25).
- Para los tests y el PDF: **Node** y el runner `browser-automation` (Playwright). Los asistentes no necesitan nada de esto.

## Comandos

Todos desde `sesion_2/` (en Windows, `set PYTHONIOENCODING=utf-8` si la consola no muestra bien las tildes).

```bash
# 1) Generar la base (determinística: mismo resultado siempre, SHA-256 se imprime)
python variante-a/build_db.py                   # -> variante-a/aerolineas.db

# 2) Verificar: base + trampas + hallazgos + determinismo + TEORIA.md + SOLUCION.md
cd variante-a && python verify_db.py && cd ..   # termina con "N verificaciones, 0 fallas"

# 3) Construir todo lo publicable (base -> Lab -> dist/)
python armar_dist.py                            # o: python armar_dist.py a-aerolineas

# Solo el Lab (sin armar todo dist/):
python compartido/build_lab.py a-aerolineas variante-a/aerolineas.db "Torre de control · Aerolíneas"
```

Si cambian la base, o las consultas, o los ejemplos:

```bash
cd variante-a
python generar_teoria.py                        # recalcula los resultados de material/TEORIA.md
python facilitadores/generar_solucion.py        # recalcula facilitadores/SOLUCION.md (solo en tu máquina)
python verify_db.py                             # tiene que volver a dar 0 fallas
```

### Tests del Lab y del dashboard (navegador headless)

```bash
SK=<carpeta del skill>/browser.mjs      # p. ej. ~/.claude/skills/browser-automation/browser.mjs
cd compartido
node $SK "file:///RUTA/sesion_2/dist/a-aerolineas/lab.html"           --script ./test_lab.mjs
node $SK "file:///RUTA/sesion_2/compartido/dashboard_base.html"       --script ./test_dashboard.mjs
```

Cada uno imprime `"pasaron": N, "fallaron": 0`. El del Lab abre el archivo con `file://` (como doble click),
ejecuta consultas, hace `CREATE TABLE`/`DROP`, reinicia la base, prueba errores, copias e historial (incluso sin `localStorage`).

### Regenerar el PDF

```bash
cd compartido
node $SK "file:///RUTA/sesion_2/compartido/introduccion_sql.html" --script ./build_pdf.mjs
# escribe sesion_2/INTRODUCCION SQL Y DATOS.pdf; después: python ../armar_dist.py
```

## Prueba manual (si no pueden correr los tests automáticos)

1. Abrir `dist/a-aerolineas/lab.html` con doble click. Esperar "Motor listo".
2. El panel izquierdo lista 7 tablas, con `PK`/`FK` y las relaciones abajo. Click en `vuelos` inserta `SELECT * FROM vuelos LIMIT 10;`.
3. `SELECT COUNT(*) FROM vuelos;` con **Ctrl+Enter** → 1 fila. `SELECT * FROM vuelos;` → avisa que muestra 500.
4. `SELEC 1;` → error en español + mensaje original.
5. `CREATE TABLE prueba (x INTEGER);` → la tabla aparece sola en el esquema. `DROP TABLE prueba;` → desaparece.
6. `DELETE FROM incidencias;` y luego **Reiniciar base** (aceptar) → vuelven las filas.
7. Botones "Copiar JSON / CSV / Markdown" y "Copiar esquema para la IA": pegar en un bloc de notas.
8. Abrir `compartido/dashboard_base.html`: 3 gráficos con carteles "EJEMPLO"; botón de tema alterna claro/oscuro.

## Publicar

Se publica **solo `dist/`** (por ejemplo con GitHub Pages apuntando a esa carpeta). Antes de publicar:

1. `python armar_dist.py` y `cd variante-a && python verify_db.py`.
2. Los `.md` de `dist/` ya traen los links relativos correctos (`lab.html`, `dashboard_base.html`, el PDF un nivel arriba).
3. Pasarle a los asistentes el link a `…/a-aerolineas/lab.html` y el de la consigna.

## Agregar la variante B

Lo compartido (`compartido/`, `armar_dist.py`, `solucion_util.py`) no depende de la variante. Para sumar la B:
crear `variante-b/` con su `build_db.py`, `verify_db.py`, `material/` y `facilitadores/`; registrarla en `VARIANTES`
dentro de `armar_dist.py`. El Lab, el dashboard y el PDF se reutilizan tal cual.

## Datos de la variante A (para tener presente)

Semilla `20250139`, período 2025-01-01 a 2025-12-31. Tablas: `aeropuertos` (28), `aeronaves` (14), `rutas` (60),
`causas_demora` (8), `vuelos` (5.211), `incidencias` (1.375), `reporte_legacy` (450, año 2024, solo para el extra E5).
El mapa de trampas, los hallazgos ocultos y las pistas están en `facilitadores/SOLUCION.md`.
