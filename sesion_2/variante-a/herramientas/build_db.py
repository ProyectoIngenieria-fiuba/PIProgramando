#!/usr/bin/env python3
"""Genera la base de datos FICTICIA de la variante A (Aerolíneas, "Torre de control").

Solo usa la biblioteca estándar. Es determinística: con la misma semilla produce
exactamente el mismo archivo (mismo SHA-256).

Uso:
    python build_db.py                 # escribe aerolineas.db junto a este script
    python build_db.py salida.db       # escribe en otra ruta
"""
import hashlib
import math
import os
import random
import sqlite3
import sys

# Semilla elegida tras barrer 40 candidatas: es la que mejor cumple a la vez
# las proporciones de estados, puntualidad, ocupación y cantidad de incidencias.
SEMILLA = 20250139
AQUI = os.path.dirname(os.path.abspath(__file__))
DB_POR_DEFECTO = os.path.join(AQUI, "aerolineas.db")

# --------------------------------------------------------------------------- #
# Catálogos
# --------------------------------------------------------------------------- #
# (iata, nombre, ciudad, provincia, region, lat, lon)
AEROPUERTOS = [
    ("AEP", "Aeroparque Jorge Newbery", "Buenos Aires", "Ciudad Autónoma de Buenos Aires", "AMBA", -34.56, -58.42),
    ("EZE", "Aeropuerto Internacional Ministro Pistarini", "Ezeiza", "Buenos Aires", "AMBA", -34.82, -58.54),
    ("COR", "Aeropuerto Internacional Ingeniero Ambrosio Taravella", "Córdoba", "Córdoba", "Centro", -31.32, -64.21),
    ("MDZ", "Aeropuerto Internacional Gobernador Francisco Gabrielli", "Mendoza", "Mendoza", "Cuyo", -32.83, -68.79),
    ("ROS", "Aeropuerto Internacional Islas Malvinas", "Rosario", "Santa Fe", "Centro", -32.92, -60.78),
    ("BRC", "Aeropuerto Internacional Teniente Luis Candelaria", "San Carlos de Bariloche", "Río Negro", "Patagonia", -41.15, -71.16),
    ("USH", "Aeropuerto Internacional Malvinas Argentinas", "Ushuaia", "Tierra del Fuego", "Patagonia", -54.84, -68.30),
    ("IGR", "Aeropuerto Internacional Cataratas del Iguazú", "Puerto Iguazú", "Misiones", "NEA", -25.74, -54.47),
    ("SLA", "Aeropuerto Internacional Martín Miguel de Güemes", "Salta", "Salta", "NOA", -24.86, -65.49),
    ("TUC", "Aeropuerto Internacional Teniente Benjamín Matienzo", "San Miguel de Tucumán", "Tucumán", "NOA", -26.84, -65.10),
    ("NQN", "Aeropuerto Internacional Presidente Perón", "Neuquén", "Neuquén", "Patagonia", -38.95, -68.16),
    ("CRD", "Aeropuerto General Enrique Mosconi", "Comodoro Rivadavia", "Chubut", "Patagonia", -45.79, -67.47),
    ("FTE", "Aeropuerto Internacional Comandante Armando Tola", "El Calafate", "Santa Cruz", "Patagonia", -50.28, -72.05),
    ("REL", "Aeropuerto Almirante Marcos A. Zar", "Trelew", "Chubut", "Patagonia", -43.21, -65.27),
    ("PMY", "Aeropuerto El Tehuelche", "Puerto Madryn", "Chubut", "Patagonia", -42.76, -65.10),
    ("RGL", "Aeropuerto Internacional Piloto Civil Norberto Fernández", "Río Gallegos", "Santa Cruz", "Patagonia", -51.61, -69.31),
    ("RES", "Aeropuerto Internacional de Resistencia", "Resistencia", "Chaco", "NEA", -27.45, -59.06),
    ("CNQ", "Aeropuerto Camba Punta", "Corrientes", "Corrientes", "NEA", -27.45, -58.76),
    ("PSS", "Aeropuerto Internacional Libertador General José de San Martín", "Posadas", "Misiones", "NEA", -27.39, -55.97),
    ("FMA", "Aeropuerto Internacional El Pucú", "Formosa", "Formosa", "NEA", -26.21, -58.23),
    ("JUJ", "Aeropuerto Internacional Gobernador Horacio Guzmán", "San Salvador de Jujuy", "Jujuy", "NOA", -24.39, -65.10),
    ("CTC", "Aeropuerto Coronel Felipe Varela", "San Fernando del Valle de Catamarca", "Catamarca", "NOA", -28.60, -65.75),
    ("IRJ", "Aeropuerto Capitán Vicente Almandos Almonacid", "La Rioja", "La Rioja", "NOA", -29.38, -66.80),
    ("UAQ", "Aeropuerto Domingo Faustino Sarmiento", "San Juan", "San Juan", "Cuyo", -31.57, -68.42),
    ("AFA", "Aeropuerto Suboficial Ayudante Santiago Germano", "San Rafael", "Mendoza", "Cuyo", -34.59, -68.40),
    ("SFN", "Aeropuerto Sauce Viejo", "Santa Fe", "Santa Fe", "Centro", -31.71, -60.81),
    ("MDQ", "Aeropuerto Internacional Astor Piazzolla", "Mar del Plata", "Buenos Aires", "Centro", -37.93, -57.57),
    ("SDE", "Aeropuerto Madre de Ciudades", "Santiago del Estero", "Santiago del Estero", "NOA", -27.77, -64.31),
]

MODELOS = {
    "Boeing 737-800": 170,
    "Boeing 737 MAX 8": 172,
    "Embraer 190": 96,
}

# (matricula, modelo, anio_incorporacion). LV-Z01 y LV-Z02 son las dos viejas.
AERONAVES = [
    ("LV-Z01", "Boeing 737-800", 2008),
    ("LV-Z02", "Boeing 737-800", 2011),
    ("LV-Z03", "Boeing 737-800", 2015),
    ("LV-Z04", "Boeing 737-800", 2016),
    ("LV-Z05", "Boeing 737-800", 2018),
    ("LV-Z06", "Boeing 737-800", 2019),
    ("LV-Z07", "Boeing 737 MAX 8", 2019),
    ("LV-Z08", "Boeing 737 MAX 8", 2021),
    ("LV-Z09", "Boeing 737 MAX 8", 2022),
    ("LV-Z10", "Boeing 737 MAX 8", 2023),
    ("LV-Z11", "Embraer 190", 2013),
    ("LV-Z12", "Embraer 190", 2015),
    ("LV-Z13", "Embraer 190", 2017),
    ("LV-Z14", "Embraer 190", 2018),
]
VIEJAS = ("LV-Z01", "LV-Z02")

CAUSAS = [
    ("Mantenimiento técnico", "Propia"),
    ("Tripulación", "Propia"),
    ("Operaciones de rampa", "Propia"),
    ("Rotación de aeronave", "Propia"),
    ("Meteorología", "Externa"),
    ("Control de tráfico aéreo", "Externa"),
    ("Seguridad aeroportuaria", "Externa"),
    ("Demora de pasajeros", "Externa"),
]
# Pesos base para elegir la causa de una demora (mismo orden que CAUSAS).
PESOS_CAUSA = [0.10, 0.10, 0.14, 0.16, 0.12, 0.18, 0.05, 0.15]
PESOS_CAUSA_CANCELADO = [0.20, 0.15, 0.05, 0.05, 0.35, 0.10, 0.05, 0.05]

# Rutas: 20 pares radiales (AEP/EZE en un extremo) + 10 transversales federales.
PARES_RADIALES = (
    [("AEP", d) for d in ("COR", "MDZ", "BRC", "TUC", "SLA", "NQN", "IGR", "MDQ", "CRD", "RES")]
    + [("EZE", d) for d in ("USH", "FTE", "REL", "PMY", "RGL", "JUJ", "CNQ", "PSS", "CTC", "UAQ")]
)
PARES_TRANSVERSALES = [
    ("COR", "MDZ"), ("COR", "BRC"), ("ROS", "BRC"), ("COR", "SLA"), ("COR", "IGR"),
    ("COR", "NQN"), ("ROS", "TUC"), ("MDZ", "BRC"), ("TUC", "IGR"), ("COR", "TUC"),
]
# Perfiles especiales (por par, se aplican a ida y vuelta).
PARES_CRITICOS = {("COR", "MDZ"), ("COR", "BRC"), ("ROS", "BRC"), ("COR", "SLA")}
PARES_BAJO_VOLUMEN = {("EZE", "UAQ"), ("EZE", "CTC"), ("EZE", "CNQ")}
PARES_ALTA_OCUPACION = {("AEP", "BRC"), ("EZE", "USH")}

PESO_MES = [1.12, 0.90, 0.95, 0.95, 0.90, 0.92, 1.12, 0.95, 0.95, 0.98, 1.00, 1.10]
DIAS_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# --------------------------------------------------------------------------- #
# Esquema
# --------------------------------------------------------------------------- #
ESQUEMA = """
CREATE TABLE aeropuertos (
    id           INTEGER PRIMARY KEY,
    codigo_iata  TEXT NOT NULL UNIQUE,
    nombre       TEXT NOT NULL,
    ciudad       TEXT NOT NULL,
    provincia    TEXT NOT NULL,
    region       TEXT NOT NULL
);
CREATE TABLE aeronaves (
    id                  INTEGER PRIMARY KEY,
    matricula           TEXT NOT NULL UNIQUE,
    modelo              TEXT NOT NULL,
    capacidad_asientos  INTEGER NOT NULL,
    anio_incorporacion  INTEGER NOT NULL
);
CREATE TABLE rutas (
    id           INTEGER PRIMARY KEY,
    origen_id    INTEGER NOT NULL REFERENCES aeropuertos(id),
    destino_id   INTEGER NOT NULL REFERENCES aeropuertos(id),
    distancia_km INTEGER NOT NULL
);
CREATE TABLE causas_demora (
    id               INTEGER PRIMARY KEY,
    descripcion      TEXT NOT NULL,
    area_responsable TEXT NOT NULL CHECK (area_responsable IN ('Propia', 'Externa'))
);
CREATE TABLE vuelos (
    id                INTEGER PRIMARY KEY,
    ruta_id           INTEGER NOT NULL REFERENCES rutas(id),
    aeronave_id       INTEGER NOT NULL REFERENCES aeronaves(id),
    fecha_programada  TEXT NOT NULL,
    estado            TEXT NOT NULL,
    minutos_demora    INTEGER,
    pasajeros         INTEGER NOT NULL
);
CREATE TABLE incidencias (
    id                INTEGER PRIMARY KEY,
    vuelo_id          INTEGER NOT NULL REFERENCES vuelos(id),
    causa_id          INTEGER NOT NULL REFERENCES causas_demora(id),
    minutos_imputados INTEGER
);
CREATE TABLE reporte_legacy (
    id                 INTEGER PRIMARY KEY,
    fecha              TEXT,
    matricula          TEXT,
    modelo             TEXT,
    capacidad_asientos INTEGER,
    aeropuerto_origen  TEXT,
    ciudad_origen      TEXT,
    provincia_origen   TEXT,
    aeropuerto_destino TEXT,
    ciudad_destino     TEXT,
    provincia_destino  TEXT,
    causa_1            TEXT,
    minutos_1          INTEGER,
    causa_2            TEXT,
    minutos_2          INTEGER
);
"""


# --------------------------------------------------------------------------- #
# Generación
# --------------------------------------------------------------------------- #
def distancia_km(a, b):
    """Gran círculo entre dos aeropuertos, redondeada a múltiplos de 5 km."""
    r = 6371.0
    p1, p2 = math.radians(a[5]), math.radians(b[5])
    dp = p2 - p1
    dl = math.radians(b[6] - a[6])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    d = 2 * r * math.asin(math.sqrt(h))
    return int(round(d / 5.0)) * 5


def construir_rutas():
    por_iata = {a[0]: a for a in AEROPUERTOS}
    ids = {a[0]: i + 1 for i, a in enumerate(AEROPUERTOS)}
    rutas = []
    for tipo, pares in (("radial", PARES_RADIALES), ("transversal", PARES_TRANSVERSALES)):
        for a, b in pares:
            d = distancia_km(por_iata[a], por_iata[b])
            for o, de in ((a, b), (b, a)):
                par = (a, b)
                if par in PARES_CRITICOS:
                    perfil = "critica"
                elif par in PARES_BAJO_VOLUMEN:
                    perfil = "bajo_volumen"
                elif par in PARES_ALTA_OCUPACION:
                    perfil = "alta_ocupacion"
                else:
                    perfil = "normal"
                rutas.append({
                    "id": len(rutas) + 1, "o": o, "d": de, "o_id": ids[o], "d_id": ids[de],
                    "dist": d, "tipo": tipo, "perfil": perfil,
                    "region_o": por_iata[o][4],
                })
    return rutas


def cantidades_por_ruta(rutas, rng):
    """Cuántos vuelos tiene cada ruta (suma ≈ 5.200)."""
    n = {}
    especiales = {"critica": (66, 82), "bajo_volumen": (14, 34), "alta_ocupacion": (120, 150)}
    pesos = {}
    for r in rutas:
        if r["perfil"] in especiales:
            lo, hi = especiales[r["perfil"]]
            n[r["id"]] = rng.randint(lo, hi)
        elif r["tipo"] == "transversal":
            pesos[r["id"]] = 0.55
        elif r["o"] == "AEP" or r["d"] == "AEP":
            pesos[r["id"]] = 1.5
        else:
            pesos[r["id"]] = 0.8
    restante = 5200 - sum(n.values())
    unidad = restante / sum(pesos.values())
    for rid, w in pesos.items():
        n[rid] = max(54, int(round(w * unidad * rng.uniform(0.92, 1.08))))
    return n


PERFIL = {
    #                 p_tarde  carga  desvio  p_cancel
    "critica":        (0.370, 0.905, 0.050, 0.020),
    "bajo_volumen":   (0.150, 0.995, 0.040, 0.010),
    "alta_ocupacion": (0.110, 0.865, 0.060, 0.030),
    "normal":         (0.180, 0.765, 0.100, 0.041),
}
AJUSTE_REGION_P_TARDE = {"AMBA": 0.03, "Patagonia": 0.02}


def elegir_fecha(rng):
    mes = rng.choices(range(12), weights=PESO_MES)[0]
    dia = rng.randint(1, DIAS_MES[mes])
    return "2025-%02d-%02d" % (mes + 1, dia), mes + 1


def elegir_aeronave(ruta, aeronaves, rng):
    """aeronaves: lista de (id, matricula, modelo, cap). Devuelve una tupla."""
    b737 = [a for a in aeronaves if a[2].startswith("Boeing")]
    emb = [a for a in aeronaves if a[2].startswith("Embraer")]
    if ruta["perfil"] in ("critica", "alta_ocupacion"):
        pool = b737
    elif ruta["perfil"] == "bajo_volumen":
        pool = emb
    elif ruta["dist"] < 900 and rng.random() < 0.5:
        pool = emb
    else:
        pool = b737
    pesos = [1.3 if a[1] in VIEJAS else 1.0 for a in pool]
    return rng.choices(pool, weights=pesos)[0]


def generar_vuelos(rutas, aeronaves, rng):
    cant = cantidades_por_ruta(rutas, rng)
    crudos = []
    for r in rutas:
        p_tarde, carga, desvio, p_cancel = PERFIL[r["perfil"]]
        n = cant[r["id"]]
        # Muestreo estratificado: cada ruta cumple su tasa de demora casi exacta,
        # sin el ruido de un sorteo puro (que dejaba rutas críticas fuera de rango).
        estratos = [(j + rng.random()) / n for j in range(n)]
        rng.shuffle(estratos)
        for k in range(n):
            fecha, mes = elegir_fecha(rng)
            aer = elegir_aeronave(r, aeronaves, rng)
            vieja = aer[1] in VIEJAS
            crudos.append((fecha, r["id"], rng.random(), mes, aer, vieja, p_tarde, carga, desvio, p_cancel, r, estratos[k]))
    crudos.sort(key=lambda t: (t[0], t[1], t[2]))

    vuelos = []
    incidencias = []
    for i, (fecha, rid, _u, mes, aer, vieja, p_tarde, carga, desvio, p_cancel, r, estrato) in enumerate(crudos, start=1):
        cap = aer[3]
        invierno_patagonico = r["region_o"] == "Patagonia" and mes in (6, 7, 8)
        p_t = p_tarde + AJUSTE_REGION_P_TARDE.get(r["region_o"], 0.0)
        if r["perfil"] == "normal":
            if vieja:
                p_t += 0.06
            if invierno_patagonico:
                p_t += 0.12

        u = rng.random()
        if u < p_cancel:
            estado, demora, pax = "Cancelado", None, 0
        else:
            if rng.random() < 0.0115 and r["perfil"] == "normal":
                estado = "Desviado"
                demora = rng.randint(60, 240)
            else:
                estado = "Operado"
                v = estrato
                if v < p_t:
                    demora = 16 + int(rng.expovariate(1 / 40.0))
                    demora = min(demora, 280)
                elif v < p_t + 0.08:
                    demora = -rng.randint(3, 10)
                else:
                    demora = min(15, int(rng.expovariate(1 / 5.0)))
            media = carga + (0.08 if mes in (1, 7) else 0.0)
            f = min(1.0, max(0.35, rng.gauss(media, desvio)))
            pax = min(cap, int(round(cap * f)))
        vuelos.append([i, rid, aer[0], fecha, estado, demora, pax, mes, vieja, invierno_patagonico])

    # Trampa T1: ~30 "Operado" escritos en minúscula.
    operados = [v for v in vuelos if v[4] == "Operado"]
    for v in rng.sample(operados, 30):
        v[4] = "operado"

    # Incidencias
    inc_id = 1
    for v in vuelos:
        vid, estado, demora, vieja, inv = v[0], v[4], v[5], v[8], v[9]
        if estado == "Cancelado":
            causa = rng.choices(range(8), weights=PESOS_CAUSA_CANCELADO)[0] + 1
            incidencias.append((inc_id, vid, causa, None))
            inc_id += 1
            continue
        if demora is None or demora <= 15:
            continue
        if rng.random() >= 0.85:
            continue  # T8: vuelo demorado sin incidencia registrada
        pesos = list(PESOS_CAUSA)
        if vieja:
            pesos[0] = 1.8
        if inv:
            pesos[4] = 1.2
        c1 = rng.choices(range(8), weights=pesos)[0]
        if rng.random() < 0.25:  # T5: dos incidencias
            pesos2 = list(pesos)
            pesos2[c1] = 0.0
            c2 = rng.choices(range(8), weights=pesos2)[0]
            m1 = rng.randint(max(1, int(round(0.2 * demora))), int(round(0.8 * demora)))
            m2 = demora - m1
            incidencias.append((inc_id, vid, c1 + 1, m1))
            incidencias.append((inc_id + 1, vid, c2 + 1, m2))
            inc_id += 2
        else:
            incidencias.append((inc_id, vid, c1 + 1, demora))
            inc_id += 1

    filas = [(v[0], v[1], v[2], v[3], v[4], v[5], v[6]) for v in vuelos]
    return filas, incidencias


# --------------------------------------------------------------------------- #
# reporte_legacy (2024, plano y sucio, independiente de vuelos)
# --------------------------------------------------------------------------- #
VARIANTES_MODELO = {
    "Boeing 737-800": ["Boeing 737-800", "B737-800", "boeing 737-800 "],
    "Boeing 737 MAX 8": ["Boeing 737 MAX 8", "B737 MAX 8", "boeing 737 max 8 "],
    "Embraer 190": ["Embraer 190", "EMBRAER 190", "embraer 190 "],
}
VARIANTES_CIUDAD = {
    "San Carlos de Bariloche": ["Bariloche", "San Carlos de Bariloche", "S. C. de Bariloche"],
    "San Miguel de Tucumán": ["San Miguel de Tucumán", "Tucumán", "S. M. de Tucumán"],
    "San Salvador de Jujuy": ["San Salvador de Jujuy", "Jujuy", "S. S. de Jujuy"],
    "Buenos Aires": ["Buenos Aires", "CABA", "Capital Federal"],
}
VARIANTES_NOMBRE_ESPECIAL = {
    "Aeroparque Jorge Newbery": ["Aeroparque Jorge Newbery", "AEROPARQUE J. NEWBERY", "Aeroparque J. Newbery"],
}


def otro_caso(valor):
    """Variante de mayúsculas/minúsculas que el LOWER() de SQLite sabe deshacer.

    LOWER/UPPER de SQLite solo conocen ASCII: 'CÓRDOBA' no se convierte en 'córdoba'.
    Por eso los textos con tilde/ñ se pasan a minúscula y el resto a MAYÚSCULA.
    """
    return valor.upper() if valor.isascii() else valor.lower()


def variantes_nombre(nombre):
    if nombre in VARIANTES_NOMBRE_ESPECIAL:
        return VARIANTES_NOMBRE_ESPECIAL[nombre]
    abrev = nombre.replace("Aeropuerto Internacional", "Aerop. Int.").replace("Aeropuerto ", "Aerop. ")
    out = [nombre, otro_caso(nombre)]
    if abrev != nombre:
        out.append(abrev)
    return out


def variantes_simple(valor, especiales=None):
    if especiales and valor in especiales:
        return especiales[valor]
    return [valor, otro_caso(valor), valor + " "]


def pick(rng, opciones):
    """Primera opción (la 'canónica') con 55%, el resto se reparte."""
    if len(opciones) == 1 or rng.random() < 0.55:
        return opciones[0]
    return rng.choice(opciones[1:])


def generar_legacy(rutas, rng):
    ap = {i + 1: a for i, a in enumerate(AEROPUERTOS)}
    aeronaves = [(m, mod) for m, mod, _ in AERONAVES]
    filas = []
    n = 450
    idx_capacidad_rara = set(rng.sample(range(n), 5))
    for i in range(n):
        m = 1 + rng.randrange(12)
        d = rng.randint(1, DIAS_MES[m - 1])
        fecha = "2024-%02d-%02d" % (m, d)
        mat, modelo = rng.choice(aeronaves)
        cap = MODELOS[modelo]
        if i in idx_capacidad_rara:
            cap = cap - 1  # anomalía de actualización (169 en vez de 170, etc.)
        r = rng.choice(rutas)
        o, de = ap[r["o_id"]], ap[r["d_id"]]
        total = 16 + min(200, int(rng.expovariate(1 / 40.0)))
        i1 = rng.randrange(8)
        causa_1 = pick(rng, variantes_simple(CAUSAS[i1][0]))
        if rng.random() < 0.35 and total >= 30:
            m1 = rng.randint(int(0.2 * total), int(0.8 * total))
            c2_base = CAUSAS[(i1 + 1 + rng.randrange(7)) % 8][0]  # siempre distinta de causa_1
            causa_2, minutos_2 = pick(rng, variantes_simple(c2_base)), total - m1
        else:
            m1, causa_2, minutos_2 = total, None, None
        filas.append((
            i + 1, fecha, mat, pick(rng, VARIANTES_MODELO[modelo]), cap,
            pick(rng, variantes_nombre(o[1])), pick(rng, variantes_simple(o[2], VARIANTES_CIUDAD)),
            pick(rng, variantes_simple(o[3])),
            pick(rng, variantes_nombre(de[1])), pick(rng, variantes_simple(de[2], VARIANTES_CIUDAD)),
            pick(rng, variantes_simple(de[3])),
            causa_1, m1, causa_2, minutos_2,
        ))
    return filas


# --------------------------------------------------------------------------- #
# Armado
# --------------------------------------------------------------------------- #
def construir(ruta_db, semilla=SEMILLA):
    if os.path.exists(ruta_db):
        os.remove(ruta_db)
    rng = random.Random(semilla)
    rng_legacy = random.Random(semilla + 1)

    rutas = construir_rutas()
    aeronaves = [(i + 1, m, mod, MODELOS[mod]) for i, (m, mod, _) in enumerate(AERONAVES)]
    vuelos, incidencias = generar_vuelos(rutas, aeronaves, rng)
    legacy = generar_legacy(rutas, rng_legacy)

    con = sqlite3.connect(ruta_db)
    con.executescript(ESQUEMA)
    con.executemany("INSERT INTO aeropuertos VALUES (?,?,?,?,?,?)",
                    [(i + 1, a[0], a[1], a[2], a[3], a[4]) for i, a in enumerate(AEROPUERTOS)])
    con.executemany("INSERT INTO aeronaves VALUES (?,?,?,?,?)",
                    [(i + 1, m, mod, MODELOS[mod], anio) for i, (m, mod, anio) in enumerate(AERONAVES)])
    con.executemany("INSERT INTO rutas VALUES (?,?,?,?)",
                    [(r["id"], r["o_id"], r["d_id"], r["dist"]) for r in rutas])
    con.executemany("INSERT INTO causas_demora VALUES (?,?,?)",
                    [(i + 1, d, a) for i, (d, a) in enumerate(CAUSAS)])
    con.executemany("INSERT INTO vuelos VALUES (?,?,?,?,?,?,?)", vuelos)
    con.executemany("INSERT INTO incidencias VALUES (?,?,?,?)", incidencias)
    con.executemany("INSERT INTO reporte_legacy VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", legacy)
    con.commit()
    con.execute("VACUUM")
    con.close()
    return ruta_db


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


if __name__ == "__main__":
    destino = sys.argv[1] if len(sys.argv) > 1 else DB_POR_DEFECTO
    construir(destino)
    con = sqlite3.connect(destino)
    print("Base generada en:", destino)
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        print("  %-16s %6d filas" % (t, con.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]))
    con.close()
    print("SHA-256:", sha256(destino))
