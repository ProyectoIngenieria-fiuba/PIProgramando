#!/usr/bin/env python3
"""Verifica la base de la variante A: estructura, trampas, hallazgos ocultos y
determinismo. Solo biblioteca estándar.

Uso:  python verify_db.py            (genera la base en un temporal y la prueba)
"""
import os
import sqlite3
import sys
import tempfile

import build_db
import solucion_util as su

OPERADO = "LOWER(v.estado) = 'operado'"
CARGA = "1.0 * v.pasajeros / a.capacidad_asientos"

resultados = []


def check(nombre, condicion, detalle=""):
    resultados.append((nombre, bool(condicion), detalle))
    estado = "OK  " if condicion else "FALLA"
    print("[%s] %s%s" % (estado, nombre, ("  ->  " + detalle) if detalle else ""))


def en_rango(valor, lo, hi):
    return lo <= valor <= hi


def verificar_base(con):
    q1 = lambda sql: con.execute(sql).fetchone()[0]
    qa = lambda sql: con.execute(sql).fetchall()

    # --- Conteos ---------------------------------------------------------
    for tabla, lo, hi in [("aeropuertos", 28, 28), ("aeronaves", 14, 14), ("rutas", 60, 60),
                          ("causas_demora", 8, 8), ("vuelos", 4900, 5500),
                          ("incidencias", 1150, 1450), ("reporte_legacy", 400, 500)]:
        n = q1("SELECT COUNT(*) FROM " + tabla)
        check("conteo %s en [%d, %d]" % (tabla, lo, hi), en_rango(n, lo, hi), "n=%d" % n)

    check("integridad referencial (foreign_key_check)", not qa("PRAGMA foreign_key_check"))
    check("fechas dentro de 2025", q1("SELECT MIN(fecha_programada) >= '2025-01-01' AND MAX(fecha_programada) <= '2025-12-31' FROM vuelos"))

    # --- Catálogos --------------------------------------------------------
    regiones = dict(qa("SELECT region, COUNT(*) FROM aeropuertos GROUP BY region"))
    check("regiones de aeropuertos", regiones == {"AMBA": 2, "Centro": 4, "Cuyo": 3, "NOA": 6, "NEA": 5, "Patagonia": 8}, str(regiones))
    check("3 modelos y capacidades",
          dict(qa("SELECT modelo, MAX(capacidad_asientos) FROM aeronaves GROUP BY modelo")) ==
          {"Boeing 737-800": 170, "Boeing 737 MAX 8": 172, "Embraer 190": 96})
    check("matrículas con prefijo LV-Z", q1("SELECT COUNT(*) FROM aeronaves WHERE matricula NOT LIKE 'LV-Z%'") == 0)
    check("exactamente 2 aeronaves viejas (737-800, <=2011)",
          q1("SELECT COUNT(*) FROM aeronaves WHERE anio_incorporacion <= 2011") == 2 and
          q1("SELECT COUNT(*) FROM aeronaves WHERE anio_incorporacion <= 2011 AND modelo='Boeing 737-800'") == 2)
    check("rutas: 40 radiales y 20 transversales",
          (q1("""SELECT COUNT(*) FROM rutas r JOIN aeropuertos o ON o.id=r.origen_id JOIN aeropuertos d ON d.id=r.destino_id
                 WHERE o.codigo_iata IN ('AEP','EZE') OR d.codigo_iata IN ('AEP','EZE')"""),
           q1("""SELECT COUNT(*) FROM rutas r JOIN aeropuertos o ON o.id=r.origen_id JOIN aeropuertos d ON d.id=r.destino_id
                 WHERE o.codigo_iata NOT IN ('AEP','EZE') AND d.codigo_iata NOT IN ('AEP','EZE')""")) == (40, 20))
    check("rutas ida/vuelta con la misma distancia",
          q1("""SELECT COUNT(*) FROM rutas a JOIN rutas b ON a.origen_id=b.destino_id AND a.destino_id=b.origen_id
                WHERE a.distancia_km <> b.distancia_km""") == 0)
    check("causas: 4 propias y 4 externas",
          dict(qa("SELECT area_responsable, COUNT(*) FROM causas_demora GROUP BY 1")) == {"Propia": 4, "Externa": 4})

    # --- Distribución de estados -------------------------------------------
    total = q1("SELECT COUNT(*) FROM vuelos")
    pct = lambda cond: 100.0 * q1("SELECT COUNT(*) FROM vuelos v WHERE " + cond) / total
    # Nota: 94% + 3,5% + 0,8% no suma 100; con los 'operado' en minúscula
    # (~0,6%) el total de operados queda en ~95,6%.
    p_op = pct("estado='Operado'")
    p_ca, p_de = pct("estado='Cancelado'"), pct("estado='Desviado'")
    check("~94-95% 'Operado' (exacto)", en_rango(p_op, 93.8, 95.6), "%.2f%%" % p_op)
    check("~3,5% cancelados", en_rango(p_ca, 3.2, 3.8), "%.2f%%" % p_ca)
    check("~0,8% desviados", en_rango(p_de, 0.65, 0.95), "%.2f%%" % p_de)
    check("estados posibles", {e for (e,) in qa("SELECT DISTINCT estado FROM vuelos")} == {"Operado", "operado", "Cancelado", "Desviado"})

    # --- Trampas ------------------------------------------------------------
    n_t1 = q1("SELECT COUNT(*) FROM vuelos WHERE estado='operado'")
    check("T1: 30 +/- 10 'operado' en minúscula", en_rango(n_t1, 20, 40), "n=%d" % n_t1)
    check("T2: cancelados con demora NULL y pasajeros 0",
          q1("SELECT COUNT(*) FROM vuelos WHERE estado='Cancelado' AND (minutos_demora IS NOT NULL OR pasajeros <> 0)") == 0
          and q1("SELECT COUNT(*) FROM vuelos WHERE estado<>'Cancelado' AND minutos_demora IS NULL") == 0)
    n_op = q1("SELECT COUNT(*) FROM vuelos v WHERE " + OPERADO)
    n_adel = q1("SELECT COUNT(*) FROM vuelos v WHERE %s AND minutos_demora < 0" % OPERADO)
    n_tarde = q1("SELECT COUNT(*) FROM vuelos v WHERE %s AND minutos_demora > 15" % OPERADO)
    check("T3: ~8% de operados adelantados (-3 a -10)",
          en_rango(100.0 * n_adel / n_op, 6.5, 9.5)
          and q1("SELECT MIN(minutos_demora) >= -10 FROM vuelos WHERE minutos_demora < 0")
          and q1("SELECT MAX(minutos_demora) <= -3 FROM vuelos WHERE minutos_demora < 0"),
          "%.2f%%" % (100.0 * n_adel / n_op))
    check("operados: ~22% con demora > 15", en_rango(100.0 * n_tarde / n_op, 20.0, 24.5), "%.2f%%" % (100.0 * n_tarde / n_op))
    check("T4: desviados con demora entre 60 y 240",
          q1("SELECT COUNT(*) FROM vuelos WHERE estado='Desviado'") > 0
          and q1("SELECT COUNT(*) FROM vuelos WHERE estado='Desviado' AND minutos_demora NOT BETWEEN 60 AND 240") == 0)
    check("nunca más pasajeros que asientos",
          q1("SELECT COUNT(*) FROM vuelos v JOIN aeronaves a ON a.id=v.aeronave_id WHERE v.pasajeros > a.capacidad_asientos") == 0)
    # El piso es 0,35 antes de redondear los pasajeros a entero (ej. 60/172 = 0,3488).
    check("factor de carga mínimo ~0,35 en vuelos con pasajeros",
          q1("SELECT MIN(%s) FROM vuelos v JOIN aeronaves a ON a.id=v.aeronave_id WHERE v.pasajeros > 0" % CARGA) >= 0.34)

    # --- Incidencias --------------------------------------------------------
    n_con = q1("""SELECT COUNT(*) FROM vuelos v WHERE minutos_demora > 15 AND EXISTS (SELECT 1 FROM incidencias i WHERE i.vuelo_id=v.id)""")
    n_dem = q1("SELECT COUNT(*) FROM vuelos WHERE minutos_demora > 15")
    check("T8: ~85% de los demorados >15 tienen incidencia", en_rango(100.0 * n_con / n_dem, 80, 90), "%.1f%%" % (100.0 * n_con / n_dem))
    check("T8: existen demorados >15 sin incidencia", n_dem - n_con > 50, "n=%d" % (n_dem - n_con))
    con_inc = q1("SELECT COUNT(DISTINCT vuelo_id) FROM incidencias WHERE minutos_imputados IS NOT NULL")
    con_2 = q1("SELECT COUNT(*) FROM (SELECT vuelo_id FROM incidencias WHERE minutos_imputados IS NOT NULL GROUP BY vuelo_id HAVING COUNT(*) >= 2)")
    check("T5: ~25% de los vuelos con incidencias tienen 2", en_rango(100.0 * con_2 / con_inc, 20, 30), "%.1f%%" % (100.0 * con_2 / con_inc))
    check("T5: nadie tiene más de 2 incidencias", q1("SELECT MAX(c) FROM (SELECT COUNT(*) c FROM incidencias GROUP BY vuelo_id)") == 2)
    check("suma de minutos_imputados == minutos_demora (vuelos con incidencias)",
          q1("""SELECT COUNT(*) FROM vuelos v JOIN (SELECT vuelo_id, SUM(minutos_imputados) s FROM incidencias
                WHERE minutos_imputados IS NOT NULL GROUP BY vuelo_id) i ON i.vuelo_id=v.id WHERE i.s <> v.minutos_demora""") == 0)
    check("minutos_imputados positivos", q1("SELECT COUNT(*) FROM incidencias WHERE minutos_imputados <= 0") == 0)
    check("cada cancelado: exactamente 1 incidencia con minutos NULL",
          q1("""SELECT COUNT(*) FROM vuelos v WHERE estado='Cancelado' AND
                (SELECT COUNT(*) FROM incidencias i WHERE i.vuelo_id=v.id) = 1
                AND (SELECT COUNT(*) FROM incidencias i WHERE i.vuelo_id=v.id AND minutos_imputados IS NULL) = 1""")
          == q1("SELECT COUNT(*) FROM vuelos WHERE estado='Cancelado'")
          and q1("SELECT COUNT(*) FROM incidencias i JOIN vuelos v ON v.id=i.vuelo_id WHERE v.estado<>'Cancelado' AND i.minutos_imputados IS NULL") == 0)
    check("vuelos sin demora >15 (no cancelados) sin incidencias",
          q1("""SELECT COUNT(*) FROM incidencias i JOIN vuelos v ON v.id=i.vuelo_id
                WHERE v.estado<>'Cancelado' AND v.minutos_demora <= 15""") == 0)

    # --- Valores globales -----------------------------------------------------
    punt = 100.0 * q1("SELECT AVG(minutos_demora <= 15) FROM vuelos v WHERE " + OPERADO)
    ocup = 100.0 * q1("SELECT AVG(%s) FROM vuelos v JOIN aeronaves a ON a.id=v.aeronave_id WHERE %s" % (CARGA, OPERADO))
    check("puntualidad global ~75-80%", en_rango(punt, 75, 80), "%.2f%%" % punt)
    check("ocupación global ~78-82%", en_rango(ocup, 78, 82), "%.2f%%" % ocup)

    # --- Hallazgos ocultos --------------------------------------------------
    # 1) Mantenimiento: las dos viejas concentran los minutos
    tot_m = q1("SELECT SUM(minutos_imputados) FROM incidencias WHERE causa_id=1")
    viejas_m = q1("""SELECT SUM(i.minutos_imputados) FROM incidencias i JOIN vuelos v ON v.id=i.vuelo_id
                     JOIN aeronaves a ON a.id=v.aeronave_id WHERE i.causa_id=1 AND a.anio_incorporacion <= 2011""")
    check("H1: las 2 aeronaves viejas concentran >=50% de los minutos de Mantenimiento",
          100.0 * viejas_m / tot_m >= 50, "%.1f%% (2 de 14 aeronaves)" % (100.0 * viejas_m / tot_m))
    top2 = [m for (m,) in qa("""SELECT a.matricula FROM incidencias i JOIN vuelos v ON v.id=i.vuelo_id JOIN aeronaves a ON a.id=v.aeronave_id
                               WHERE i.causa_id=1 GROUP BY a.id ORDER BY SUM(i.minutos_imputados) DESC LIMIT 2""")]
    check("H1: las 2 primeras en Mantenimiento son LV-Z01 y LV-Z02", set(top2) == {"LV-Z01", "LV-Z02"}, str(top2))

    # 2) Rutas críticas
    rutas = qa("""SELECT r.id, COUNT(*) n, AVG(%s) oc, AVG(v.minutos_demora <= 15) pu
                  FROM vuelos v JOIN rutas r ON r.id=v.ruta_id JOIN aeronaves a ON a.id=v.aeronave_id
                  JOIN aeropuertos o ON o.id=r.origen_id JOIN aeropuertos d ON d.id=r.destino_id
                  WHERE %s AND o.codigo_iata NOT IN ('AEP','EZE') AND d.codigo_iata NOT IN ('AEP','EZE')
                  GROUP BY r.id""" % (CARGA, OPERADO))
    criticas = [r for r in rutas if r[1] >= 40 and r[2] > 0.88 and 0.58 <= r[3] <= 0.68]
    check("H2: >=5 transversales críticas (>=40 operados, ocup >88%, puntualidad 58-68%)", len(criticas) >= 5, "n=%d" % len(criticas))

    # 3) Rutas de bajo volumen con ocupación extrema
    bajas = qa("""SELECT r.id, COUNT(*) n, AVG(%s) oc FROM vuelos v JOIN rutas r ON r.id=v.ruta_id JOIN aeronaves a ON a.id=v.aeronave_id
                  WHERE %s GROUP BY r.id""" % (CARGA, OPERADO))
    bajo_vol = [r for r in bajas if r[1] < 40 and r[2] >= 0.96]
    check("H3: >=3 rutas con <40 operados y ocupación >=96%", len(bajo_vol) >= 3, "n=%d" % len(bajo_vol))
    top_sin_having = sorted(bajas, key=lambda r: -r[2])[:6]
    check("H3: sin HAVING, el top 6 de ocupación son todas de bajo volumen",
          all(r[1] < 40 for r in top_sin_having))
    top_con_having = sorted([r for r in bajas if r[1] >= 40], key=lambda r: -r[2])[:10]
    check("H3: con HAVING >=40, el top 10 incluye las críticas",
          len({r[0] for r in top_con_having} & {r[0] for r in criticas}) >= 5)

    # 4) Estacionalidad
    por_mes = dict(qa("""SELECT substr(fecha_programada,6,2), AVG(%s) FROM vuelos v JOIN aeronaves a ON a.id=v.aeronave_id
                         WHERE %s GROUP BY 1""" % (CARGA, OPERADO)))
    resto = [por_mes[m] for m in por_mes if m not in ("01", "07")]
    check("H4: ocupación de enero y julio >= 5 pts sobre el resto",
          min(por_mes["01"], por_mes["07"]) - max(resto) >= 0.04,
          "ene=%.3f jul=%.3f max resto=%.3f" % (por_mes["01"], por_mes["07"], max(resto)))
    meteo = qa("""SELECT ao.region, substr(v.fecha_programada,6,2) BETWEEN '06' AND '08', COALESCE(SUM(i.minutos_imputados), 0)
                  FROM incidencias i JOIN vuelos v ON v.id=i.vuelo_id JOIN rutas r ON r.id=v.ruta_id
                  JOIN aeropuertos ao ON ao.id=r.origen_id WHERE i.causa_id=5 GROUP BY 1, 2""")
    pat_inv = sum(m for (reg, inv, m) in meteo if reg == "Patagonia" and inv == 1)
    pat_tot = sum(m for (reg, inv, m) in meteo if reg == "Patagonia")
    check("H4: >=50% de la Meteorología patagónica cae en jun-ago (25% si fuera parejo)",
          pat_inv / pat_tot >= 0.5, "%.1f%%" % (100.0 * pat_inv / pat_tot))
    otras_inv = sum(m for (reg, inv, m) in meteo if reg != "Patagonia" and inv == 1)
    otras_tot = sum(m for (reg, inv, m) in meteo if reg != "Patagonia")
    check("H4: fuera de la Patagonia la Meteorología NO se concentra en jun-ago",
          otras_inv / otras_tot < 0.35, "%.1f%%" % (100.0 * otras_inv / otras_tot))

    # --- reporte_legacy -----------------------------------------------------------
    check("legacy: año 2024", q1("SELECT MIN(fecha) >= '2024-01-01' AND MAX(fecha) <= '2024-12-31' FROM reporte_legacy"))
    for col, esperado in [("modelo", 3 * 3), ("aeropuerto_origen", 20)]:
        n_dist = q1("SELECT COUNT(DISTINCT %s) FROM reporte_legacy" % col)
        n_norm = q1("SELECT COUNT(DISTINCT LOWER(TRIM(%s))) FROM reporte_legacy" % col)
        check("legacy: %s tiene variantes de formato" % col, n_dist > n_norm, "%d valores -> %d tras LOWER/TRIM" % (n_dist, n_norm))
    check("legacy: modelo con espacio al final", q1("SELECT COUNT(*) FROM reporte_legacy WHERE modelo LIKE '% '") > 0)
    check("legacy: abreviatura 'B737-800'", q1("SELECT COUNT(*) FROM reporte_legacy WHERE modelo = 'B737-800'") > 0)
    check("legacy: Aeroparque en 2+ formas",
          q1("SELECT COUNT(DISTINCT aeropuerto_origen) FROM reporte_legacy WHERE LOWER(aeropuerto_origen) LIKE '%newbery%'") >= 2)
    check("legacy: Bariloche con 3 variantes",
          q1("""SELECT COUNT(DISTINCT t) FROM (SELECT ciudad_origen t FROM reporte_legacy UNION SELECT ciudad_destino FROM reporte_legacy)
                WHERE t IN ('Bariloche','San Carlos de Bariloche','S. C. de Bariloche')""") == 3)
    check("legacy: causas con mayúsculas/espacios inconsistentes",
          q1("SELECT COUNT(DISTINCT causa_1) FROM reporte_legacy") > q1("SELECT COUNT(DISTINCT LOWER(TRIM(causa_1))) FROM reporte_legacy"))
    check("legacy: 1FN (causa_2 NULL en algunas y presente en otras)",
          q1("SELECT COUNT(*) FROM reporte_legacy WHERE causa_2 IS NULL") > 0 and q1("SELECT COUNT(*) FROM reporte_legacy WHERE causa_2 IS NOT NULL") > 0)
    check("legacy: causa_2 nunca repite a causa_1 (tras limpiar)",
          q1("SELECT COUNT(*) FROM reporte_legacy WHERE causa_2 IS NOT NULL AND LOWER(TRIM(causa_1)) = LOWER(TRIM(causa_2))") == 0)
    check("legacy: causa_2 y minutos_2 consistentes",
          q1("SELECT COUNT(*) FROM reporte_legacy WHERE (causa_2 IS NULL) <> (minutos_2 IS NULL)") == 0)
    rara = q1("""SELECT COUNT(*) FROM reporte_legacy WHERE
                 (LOWER(TRIM(modelo)) LIKE '%737-800%' OR LOWER(TRIM(modelo)) LIKE 'b737-800%') AND capacidad_asientos <> 170
                 OR (LOWER(TRIM(modelo)) LIKE '%max%' AND capacidad_asientos <> 172)
                 OR (LOWER(TRIM(modelo)) LIKE '%190%' OR LOWER(TRIM(modelo))='e190') AND capacidad_asientos <> 96""")
    check("legacy: ~5 filas con capacidad anómala", rara == 5, "n=%d" % rara)
    check("legacy: matrícula -> modelo consistente tras limpiar",
          q1("""SELECT COUNT(*) FROM (SELECT matricula FROM reporte_legacy GROUP BY matricula
                HAVING COUNT(DISTINCT CASE WHEN LOWER(modelo) LIKE '%737-800%' THEN 'a' WHEN LOWER(modelo) LIKE '%max%' THEN 'b' ELSE 'c' END) > 1)""") == 0)
    check("legacy: independiente de vuelos (no hay vuelos de 2024)", q1("SELECT COUNT(*) FROM vuelos WHERE fecha_programada < '2025-01-01'") == 0)


ESPERADOS_EN_SOLUCION = [
    "P1a", "P1b", "P1c", "P2a", "P3", "P4a", "P4b", "P5", "P6a", "P6b", "P6c",
    "C1", "C2", "C3", "C4", "E1", "E2", "E3-kpis", "E4",
    "E5-limpieza", "E5-esquema", "E5-migracion", "E5-reconstruccion", "E5-integridad",
    "H1", "H3", "H4", "T3", "T4", "T5", "T8",
]


def verificar_solucion(ruta_db):
    """Punto de control 3: corre TODAS las consultas de SOLUCION.md y compara con lo documentado.

    SOLUCION.md vive en facilitadores/ (no se publica). Si no está, se avisa y se sigue.
    """
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "facilitadores", "SOLUCION.md")
    if not os.path.exists(ruta):
        print("\n[AVISO] No hay facilitadores/SOLUCION.md en este clon (no se publica): se omite el punto de control 3.")
        return
    print("\n--- Consultas de SOLUCION.md ---")
    con = su.abrir_copia(ruta_db)
    try:
        lista = su.bloques(open(ruta, encoding="utf-8").read())
        ids = {b[1] for b in lista}
        faltan = [i for i in ESPERADOS_EN_SOLUCION if i not in ids]
        check("SOLUCION.md documenta P1-P6, controles, E1-E5, hallazgos y trampas", not faltan, "faltan: %s" % faltan if faltan else "%d bloques" % len(lista))
        for tipo, id_, sql, documentado in lista:
            try:
                if tipo == "run":
                    con.executescript(sql)
                    check("SOLUCION %s corre sin error" % id_, True)
                    continue
                columnas, filas = su.ejecutar_select(con, sql)
            except Exception as e:  # noqa: BLE001
                check("SOLUCION %s corre sin error" % id_, False, str(e))
                continue
            esperado = su.renderizar(columnas, filas).strip()
            check("SOLUCION %s devuelve lo documentado" % id_, documentado == esperado,
                  "" if documentado == esperado else "documentado y real difieren; regenerá con generar_solucion.py")
        # Controles propios de la solución, independientes del texto documentado
        check("SOLUCION C1: suma por estado == total", con.execute("SELECT (SELECT COUNT(*) FROM vuelos) = (SELECT SUM(c) FROM (SELECT COUNT(*) c FROM vuelos GROUP BY estado))").fetchone()[0] == 1)
        check("SOLUCION E2: devuelve exactamente las 8 rutas críticas",
              [b for b in lista if b[1] == "E2"] and len(su.ejecutar_select(con, [b for b in lista if b[1] == "E2"][0][2])[1]) == 8)
        check("SOLUCION E5: reconstrucción sin diferencias en ninguna dirección",
              su.ejecutar_select(con, [b for b in lista if b[1] == "E5-reconstruccion"][0][2])[1] == [(0, 0)])
    finally:
        con.close()


def verificar_teoria():
    """Los ejemplos de TEORIA.md (club de barrio) corren y devuelven lo documentado."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TEORIA.md")
    print("\n--- Ejemplos de TEORIA.md (club de barrio) ---")
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    try:
        lista = su.bloques(open(ruta, encoding="utf-8").read())
        check("TEORIA.md tiene ejemplos ejecutables", len(lista) >= 20, "%d bloques" % len(lista))
        malos = []
        for tipo, id_, sql, documentado in lista:
            try:
                if tipo == "run":
                    con.executescript(sql)
                    continue
                columnas, filas = su.ejecutar_select(con, sql)
            except Exception as e:  # noqa: BLE001
                malos.append("%s (%s)" % (id_, e))
                continue
            if documentado != su.renderizar(columnas, filas).strip():
                malos.append("%s (resultado distinto al documentado)" % id_)
        check("TEORIA.md: todos los ejemplos corren y devuelven lo documentado", not malos, "; ".join(malos))
    finally:
        con.close()


def main():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        a, b = os.path.join(tmp, "a.db"), os.path.join(tmp, "b.db")
        build_db.construir(a)
        build_db.construir(b)
        con = sqlite3.connect(a)
        print("SQLite %s\n" % sqlite3.sqlite_version)
        try:
            verificar_base(con)
        finally:
            con.close()
        verificar_teoria()
        verificar_solucion(a)
        ha, hb = build_db.sha256(a), build_db.sha256(b)
        check("determinismo: dos generaciones, mismo SHA-256", ha == hb, ha[:16] + "...")

    fallas = [r for r in resultados if not r[1]]
    print("\n%d verificaciones, %d fallas" % (len(resultados), len(fallas)))
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
