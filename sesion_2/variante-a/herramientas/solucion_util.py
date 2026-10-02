"""Utilidades para leer, ejecutar y comparar las consultas de SOLUCION.md y TEORIA.md.

No contiene soluciones: solo la mecánica. Lo usan verify_db.py, generar_teoria.py y
facilitadores/generar_solucion.py (que NO se publica).

Formato de los bloques:

    <!-- test: ID -->           una consulta SELECT cuyo resultado se documenta
    ```sql
    SELECT ...;
    ```
    (tabla markdown con el resultado, la escribe el generador)
    <!-- /test -->

    <!-- run: ID -->            uno o más comandos (DDL/DML) que se ejecutan en orden
    ```sql
    CREATE TABLE ...;
    ```
    <!-- /run -->
"""
import re
import sqlite3

MAX_FILAS_DOC = 15
BLOQUE = re.compile(
    r"<!-- (?P<tipo>test|run): (?P<id>[\w.\-]+) -->\s*```sql\n(?P<sql>.*?)```(?P<resto>.*?)<!-- /(?P=tipo) -->",
    re.S,
)


def valor_a_texto(v):
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return "%.10g" % v
    return str(v).replace("|", "\\|").replace("\n", " ")


def renderizar(columnas, filas):
    """Tabla markdown determinística (la misma función arma y verifica)."""
    mostrar = filas[:MAX_FILAS_DOC]
    lineas = ["| " + " | ".join(columnas) + " |", "|" + "|".join(["---"] * len(columnas)) + "|"]
    for f in mostrar:
        lineas.append("| " + " | ".join(valor_a_texto(v) for v in f) + " |")
    pie = "*(%d fila%s%s)*" % (len(filas), "" if len(filas) == 1 else "s",
                               "; se muestran las primeras %d" % MAX_FILAS_DOC if len(filas) > MAX_FILAS_DOC else "")
    return "\n".join(lineas) + "\n\n" + pie


def ejecutar_select(con, sql):
    cur = con.execute(sql)
    columnas = [d[0] for d in cur.description]
    return columnas, cur.fetchall()


def bloques(texto):
    """Devuelve [(tipo, id, sql, resto_documentado)] en el orden del documento."""
    return [(m["tipo"], m["id"], m["sql"].strip(), m["resto"].strip()) for m in BLOQUE.finditer(texto)]


def abrir_copia(ruta_db):
    """Copia en memoria de la base, con claves foráneas activas (como en el Lab)."""
    origen = sqlite3.connect(ruta_db)
    con = sqlite3.connect(":memory:")
    origen.backup(con)
    origen.close()
    con.execute("PRAGMA foreign_keys = ON")
    return con


def completar(texto, con):
    """Ejecuta los bloques en orden contra `con` y (re)escribe el resultado debajo de cada `test`.

    Lo usan generar_solucion.py (facilitadores) y generar_teoria.py (TEORIA.md, sin soluciones).
    Si una consulta falla, levanta RuntimeError indicando el bloque.
    """
    def reemplazo(m):
        tipo, id_, sql = m["tipo"], m["id"], m["sql"].strip()
        try:
            if tipo == "run":
                con.executescript(sql)
                return m.group(0)
            columnas, filas = ejecutar_select(con, sql)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError("Error en el bloque %s %s: %s\n\n%s" % (tipo, id_, e, sql)) from e
        return "<!-- test: %s -->\n```sql\n%s\n```\n\n%s\n<!-- /test -->" % (id_, sql, renderizar(columnas, filas))

    return BLOQUE.sub(reemplazo, texto)
