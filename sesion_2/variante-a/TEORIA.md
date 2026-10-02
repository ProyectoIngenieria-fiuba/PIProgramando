# Teoría — Sesión 2 · Análisis de datos con SQL

Referencia para consultar cuando algo no les cierre. **No hace falta leerla entera antes de
arrancar**: usen el índice y vuelvan a ella con la duda puntual. (Si es la primera vez que ven SQL,
la [introducción en PDF](INTRODUCCION%20SQL%20Y%20DATOS.pdf) es una mejor puerta de entrada.)

Todos los ejemplos de acá usan un **club de barrio** inventado (socios, cuotas, actividades),
*no* los datos de la aerolínea. Así pueden probar cada idea sin que les adelante nada del proyecto.

## Índice

1. [El club de barrio: cargalo en el Lab](#1-el-club-de-barrio-cargalo-en-el-lab)
2. [Leer una tabla: SELECT, FROM, WHERE, ORDER BY, LIMIT](#2-leer-una-tabla)
3. [Resumir: funciones de agregación, GROUP BY y HAVING](#3-resumir-funciones-de-agregación-group-by-y-having)
4. [Combinar tablas: JOIN](#4-combinar-tablas-join)
5. [NULL: la ausencia de dato](#5-null-la-ausencia-de-dato)
6. [CASE WHEN: decidir fila por fila](#6-case-when-decidir-fila-por-fila)
7. [COUNT(\*), COUNT(columna) y COUNT(DISTINCT)](#7-count-count-columna-y-count-distinct)
8. [Fechas con strftime](#8-fechas-con-strftime)
9. [La división entera de SQLite](#9-la-división-entera-de-sqlite)
10. [Subconsultas y CTE](#10-subconsultas-y-cte)
11. [Funciones de ventana (introducción)](#11-funciones-de-ventana-introducción)
12. [Ejemplo completamente resuelto](#12-ejemplo-completamente-resuelto)
13. [Normalización: 1FN, 2FN y 3FN](#13-normalización-1fn-2fn-y-3fn)
14. [Orden en que SQLite ejecuta una consulta](#14-orden-en-que-sqlite-ejecuta-una-consulta)

---

## 1. El club de barrio: cargalo en el Lab

El club tiene **socios** que se **inscriben** a **actividades** y pagan **cuotas** mensuales.
Hay una relación entre las tablas (las flechas son claves foráneas, `FK`):

```text
socios ──< inscripciones >── actividades
  │
  └──< cuotas
socios.recomendado_por ──> socios.id     (un socio puede haber sido recomendado por otro)
```

Para probar los ejemplos, copien este bloque en el editor del SQL Lab y ejecútenlo (con **Ctrl/⌘ + Enter**).
Crea 4 tablas nuevas **dentro de su copia de la base**; si algo sale mal o quieren limpiar, el botón
**"Reiniciar base"** vuelve a la original.

<!-- run: club -->
```sql
CREATE TABLE socios (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  barrio TEXT,
  fecha_alta TEXT NOT NULL,                       -- texto ISO: AAAA-MM-DD
  recomendado_por INTEGER REFERENCES socios(id)   -- NULL si llegó solo
);
CREATE TABLE actividades (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  cupo INTEGER NOT NULL,
  precio_mensual INTEGER NOT NULL
);
CREATE TABLE inscripciones (
  socio_id INTEGER NOT NULL REFERENCES socios(id),
  actividad_id INTEGER NOT NULL REFERENCES actividades(id),
  PRIMARY KEY (socio_id, actividad_id)
);
CREATE TABLE cuotas (
  id INTEGER PRIMARY KEY,
  socio_id INTEGER NOT NULL REFERENCES socios(id),
  mes TEXT NOT NULL,
  monto INTEGER NOT NULL,
  fecha_pago TEXT                                 -- NULL = todavía no pagó
);

INSERT INTO socios VALUES
  (1, 'Ana Pérez',     'Palermo',   '2021-03-15', NULL),
  (2, 'Bruno Díaz',    'Caballito', '2022-07-02', 1),
  (3, 'Carla Gómez',   'Palermo',   '2023-01-20', 1),
  (4, 'Diego Ruiz',    'Almagro',   '2023-06-11', 2),
  (5, 'Elena Sosa',    'Caballito', '2024-02-05', 3),
  (6, 'Facundo Luna',  'Palermo',   '2024-09-30', NULL),
  (7, 'Gala Torres',   'Almagro',   '2025-01-12', 5),
  (8, 'Hugo Paz',      'Caballito', '2025-03-01', NULL);

INSERT INTO actividades VALUES
  (1, 'Natación', 20, 18000),
  (2, 'Fútbol 5', 10, 12000),
  (3, 'Yoga',      4, 15000),
  (4, 'Ajedrez',  12,  6000);

INSERT INTO inscripciones VALUES
  (1,1),(2,1),(3,1),(5,1),(7,1),
  (2,2),(4,2),(6,2),(8,2),
  (1,3),(3,3),(5,3),(7,3);

INSERT INTO cuotas VALUES
  (1, 1,'2025-03',25000,'2025-03-05'), (2, 1,'2025-04',25000,'2025-04-04'),
  (3, 2,'2025-03',25000,'2025-03-07'), (4, 2,'2025-04',25000,'2025-04-08'),
  (5, 3,'2025-03',25000,'2025-03-02'), (6, 3,'2025-04',25000,'2025-04-02'),
  (7, 4,'2025-03',25000,'2025-03-10'), (8, 4,'2025-04',25000,NULL),
  (9, 5,'2025-03',25000,'2025-03-06'), (10,5,'2025-04',25000,'2025-04-06'),
  (11,6,'2025-03',25000,NULL),         (12,6,'2025-04',25000,NULL),
  (13,7,'2025-03',25000,'2025-03-12'), (14,7,'2025-04',25000,'2025-04-11'),
  (15,8,'2025-03',25000,'2025-03-15'), (16,8,'2025-04',25000,NULL);
```
<!-- /run -->

Después de ejecutarlo, el panel de esquema muestra las tablas nuevas.

---

## 2. Leer una tabla

Una consulta (`SELECT`) **pide datos**; no modifica nada. Las piezas básicas:

| Pieza | Para qué sirve |
|---|---|
| `SELECT columnas` | Qué columnas quiero ver (`*` = todas). |
| `FROM tabla` | De qué tabla. |
| `WHERE condición` | Me quedo solo con las **filas** que cumplen. |
| `ORDER BY columna [DESC]` | Cómo ordeno (por defecto de menor a mayor). |
| `LIMIT n` | Cuántas filas como máximo. |
| `AS alias` | Le pongo un nombre más lindo a una columna o tabla. |

<!-- test: t-basico -->
```sql
SELECT nombre, barrio, fecha_alta
FROM socios
WHERE barrio = 'Palermo'
ORDER BY fecha_alta DESC
LIMIT 2;
```

| nombre | barrio | fecha_alta |
|---|---|---|
| Facundo Luna | Palermo | 2024-09-30 |
| Carla Gómez | Palermo | 2023-01-20 |

*(2 filas)*
<!-- /test -->

Lectura: "de los socios, quedate con los de Palermo, ordenados del más nuevo al más viejo, y mostrame los 2 primeros".
Comparaciones útiles en `WHERE`: `=`, `<>`, `>`, `>=`, `BETWEEN a AND b`, `IN ('x','y')`, `LIKE 'A%'`, y combinarlas con `AND` / `OR`.
**Los textos van entre comillas simples.**

---

## 3. Resumir: funciones de agregación, GROUP BY y HAVING

Las funciones de agregación **resumen muchas filas en un número**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.

<!-- test: t-agregacion -->
```sql
SELECT COUNT(*) AS socios,
       MIN(fecha_alta) AS el_mas_antiguo,
       MAX(fecha_alta) AS el_mas_nuevo
FROM socios;
```

| socios | el_mas_antiguo | el_mas_nuevo |
|---|---|---|
| 8 | 2021-03-15 | 2025-03-01 |

*(1 fila)*
<!-- /test -->

Con `GROUP BY` armás **un resumen por grupo** (una fila por cada valor distinto):

<!-- test: t-groupby -->
```sql
SELECT barrio, COUNT(*) AS socios
FROM socios
GROUP BY barrio
ORDER BY socios DESC;
```

| barrio | socios |
|---|---|
| Palermo | 3 |
| Caballito | 3 |
| Almagro | 2 |

*(3 filas)*
<!-- /test -->

### `WHERE` vs `HAVING`

- `WHERE` filtra **filas, antes de agrupar**.
- `HAVING` filtra **grupos, después de agrupar** (por eso acepta funciones de agregación).

<!-- test: t-having -->
```sql
SELECT barrio, COUNT(*) AS socios
FROM socios
GROUP BY barrio
HAVING COUNT(*) >= 3;
```

| barrio | socios |
|---|---|
| Caballito | 3 |
| Palermo | 3 |

*(2 filas)*
<!-- /test -->

Regla práctica: si la condición menciona `COUNT`, `SUM`, `AVG`… va en `HAVING`. Si no, en `WHERE`.
Escribir `WHERE COUNT(*) >= 3` da error.

---

## 4. Combinar tablas: JOIN

La información está repartida en varias tablas. `JOIN` las **une fila a fila** cuando se cumple una condición (`ON`),
que casi siempre es "la clave foránea de una = la clave primaria de la otra".

<!-- test: t-join -->
```sql
SELECT a.nombre AS actividad, COUNT(*) AS inscriptos
FROM inscripciones i
JOIN actividades a ON a.id = i.actividad_id
GROUP BY a.id
ORDER BY inscriptos DESC;
```

| actividad | inscriptos |
|---|---|
| Natación | 5 |
| Yoga | 4 |
| Fútbol 5 | 4 |

*(3 filas)*
<!-- /test -->

Detalles que importan:

- Los **alias** (`i`, `a`) acortan el nombre de las tablas. Se usan como `alias.columna`; cuando una columna existe en las dos tablas (`id`), el alias es **obligatorio** para que SQLite sepa de cuál hablás.
- `JOIN` a secas = `INNER JOIN`: **solo** quedan las filas que tienen pareja en ambas tablas. *"Ajedrez" no aparece arriba porque nadie se inscribió.*

### LEFT JOIN: conservar todo lo de la izquierda

`LEFT JOIN` mantiene **todas** las filas de la tabla de la izquierda, aunque no tengan pareja (las columnas de la derecha quedan en `NULL`).

<!-- test: t-leftjoin -->
```sql
SELECT a.nombre AS actividad, COUNT(i.socio_id) AS inscriptos
FROM actividades a
LEFT JOIN inscripciones i ON i.actividad_id = a.id
GROUP BY a.id
ORDER BY inscriptos;
```

| actividad | inscriptos |
|---|---|
| Ajedrez | 0 |
| Fútbol 5 | 4 |
| Yoga | 4 |
| Natación | 5 |

*(4 filas)*
<!-- /test -->

Ahora aparece Ajedrez con 0. Fijate que se cuenta `COUNT(i.socio_id)` y no `COUNT(*)`: con `COUNT(*)` Ajedrez daría 1 (la fila "vacía" también cuenta). Más en la sección 7.

### Unir la misma tabla dos veces (autounión)

A veces una tabla se refiere **a sí misma** (acá, `recomendado_por` apunta a otro socio). Se une la tabla consigo misma usando **dos alias distintos**:

<!-- test: t-autojoin -->
```sql
SELECT s.nombre AS socio, r.nombre AS lo_recomendo
FROM socios s
LEFT JOIN socios r ON r.id = s.recomendado_por
ORDER BY s.id;
```

| socio | lo_recomendo |
|---|---|
| Ana Pérez | NULL |
| Bruno Díaz | Ana Pérez |
| Carla Gómez | Ana Pérez |
| Diego Ruiz | Bruno Díaz |
| Elena Sosa | Carla Gómez |
| Facundo Luna | NULL |
| Gala Torres | Elena Sosa |
| Hugo Paz | NULL |

*(8 filas)*
<!-- /test -->

Lo mismo pasa cuando una tabla aparece **dos veces con roles distintos** en la misma consulta (por ejemplo, una tabla de lugares que sirve tanto de origen como de destino):
hacen falta dos `JOIN` a la misma tabla, cada uno con su alias, y ahí cada alias es "la mitad" de la información.

### Cuidado: un JOIN puede duplicar filas

Si unís una tabla con otra en la que cada fila tiene **varias** parejas, la fila original se repite una vez por pareja. Si después sumás una columna de la tabla original, la suma sale inflada.

<!-- test: t-fanout -->
```sql
SELECT (SELECT SUM(monto) FROM cuotas) AS suma_directa,
       (SELECT SUM(c.monto) FROM cuotas c
          JOIN socios s ON s.id = c.socio_id
          JOIN inscripciones i ON i.socio_id = s.id) AS suma_tras_el_join;
```

| suma_directa | suma_tras_el_join |
|---|---|
| 400000 | 650000 |

*(1 fila)*
<!-- /test -->

Control de seguridad: **comparen el total antes y después del `JOIN`**. Si cambia sin que lo esperaran, el `JOIN` duplicó (o descartó) filas.

---

## 5. NULL: la ausencia de dato

`NULL` no es 0 ni vacío: significa **"no hay dato"**. Reglas que sorprenden:

- No se compara con `=`. Hay que usar **`IS NULL`** / **`IS NOT NULL`**.
- Casi toda operación con `NULL` da `NULL` (`5 + NULL` es `NULL`).
- `COUNT(columna)`, `SUM`, `AVG`, `MIN`, `MAX` **ignoran** los `NULL`.

<!-- test: t-null-mal -->
```sql
-- Esto NO falla, pero siempre devuelve 0 filas: nada es "igual" a NULL
SELECT COUNT(*) AS filas FROM cuotas WHERE fecha_pago = NULL;
```

| filas |
|---|
| 0 |

*(1 fila)*
<!-- /test -->

<!-- test: t-null-bien -->
```sql
SELECT s.nombre, c.mes, c.monto
FROM cuotas c
JOIN socios s ON s.id = c.socio_id
WHERE c.fecha_pago IS NULL
ORDER BY s.nombre, c.mes;
```

| nombre | mes | monto |
|---|---|---|
| Diego Ruiz | 2025-04 | 25000 |
| Facundo Luna | 2025-03 | 25000 |
| Facundo Luna | 2025-04 | 25000 |
| Hugo Paz | 2025-04 | 25000 |

*(4 filas)*
<!-- /test -->

`COALESCE(x, valor)` reemplaza `NULL` por un valor por defecto:

<!-- test: t-coalesce -->
```sql
SELECT nombre, COALESCE(barrio, 'sin barrio') AS barrio,
       COALESCE(recomendado_por, 0) AS recomendado_por
FROM socios
LIMIT 3;
```

| nombre | barrio | recomendado_por |
|---|---|---|
| Ana Pérez | Palermo | 0 |
| Bruno Díaz | Caballito | 1 |
| Carla Gómez | Palermo | 1 |

*(3 filas)*
<!-- /test -->

Orden con `NULL`: SQLite los considera **los valores más chicos**. Con `ORDER BY x` (ascendente) aparecen primero; con `DESC`, al final.

---

## 6. CASE WHEN: decidir fila por fila

`CASE` es el "si… entonces… sino" de SQL. Sirve para clasificar y también para contar condicionalmente.

<!-- test: t-case -->
```sql
SELECT nombre,
       fecha_alta,
       CASE WHEN fecha_alta < '2023-01-01' THEN 'histórico'
            WHEN fecha_alta < '2025-01-01' THEN 'reciente'
            ELSE 'nuevo' END AS antiguedad
FROM socios
ORDER BY fecha_alta;
```

| nombre | fecha_alta | antiguedad |
|---|---|---|
| Ana Pérez | 2021-03-15 | histórico |
| Bruno Díaz | 2022-07-02 | histórico |
| Carla Gómez | 2023-01-20 | reciente |
| Diego Ruiz | 2023-06-11 | reciente |
| Elena Sosa | 2024-02-05 | reciente |
| Facundo Luna | 2024-09-30 | reciente |
| Gala Torres | 2025-01-12 | nuevo |
| Hugo Paz | 2025-03-01 | nuevo |

*(8 filas)*
<!-- /test -->

Truco muy usado: **contar o sumar solo lo que cumple una condición**, dentro de un `GROUP BY`:

<!-- test: t-case-agregado -->
```sql
SELECT mes,
       COUNT(*) AS cuotas,
       SUM(CASE WHEN fecha_pago IS NULL THEN 1 ELSE 0 END) AS impagas,
       ROUND(100.0 * SUM(CASE WHEN fecha_pago IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_pagadas
FROM cuotas
GROUP BY mes;
```

| mes | cuotas | impagas | pct_pagadas |
|---|---|---|---|
| 2025-03 | 8 | 1 | 87.5 |
| 2025-04 | 8 | 3 | 62.5 |

*(2 filas)*
<!-- /test -->

---

## 7. COUNT(\*), COUNT(columna) y COUNT(DISTINCT)

| Forma | Cuenta |
|---|---|
| `COUNT(*)` | Todas las **filas** del grupo. |
| `COUNT(columna)` | Las filas donde esa columna **no es NULL**. |
| `COUNT(DISTINCT columna)` | Los valores **distintos** (y no nulos). |

<!-- test: t-counts -->
```sql
SELECT COUNT(*) AS filas,
       COUNT(fecha_pago) AS pagadas,
       COUNT(DISTINCT socio_id) AS socios_distintos,
       COUNT(DISTINCT mes) AS meses_distintos
FROM cuotas;
```

| filas | pagadas | socios_distintos | meses_distintos |
|---|---|---|---|
| 16 | 12 | 8 | 2 |

*(1 fila)*
<!-- /test -->

La diferencia `COUNT(*) − COUNT(columna)` te dice cuántos `NULL` hay. Es una forma rápida de **explorar** una columna.

---

## 8. Fechas con strftime

En SQLite no existe un tipo "fecha": se guardan como **texto** `AAAA-MM-DD`, y por eso se ordenan y comparan bien como texto.
Para extraer partes se usa `strftime(formato, fecha)`:

| Formato | Resultado |
|---|---|
| `'%Y'` | año (`2025`) |
| `'%m'` | mes con dos dígitos (`03`) |
| `'%Y-%m'` | año-mes (`2025-03`) |
| `'%d'` | día |
| `'%w'` | día de la semana (0 = domingo) |

<!-- test: t-strftime -->
```sql
SELECT strftime('%Y', fecha_alta) AS anio,
       COUNT(*) AS altas
FROM socios
GROUP BY anio
ORDER BY anio;
```

| anio | altas |
|---|---|
| 2021 | 1 |
| 2022 | 1 |
| 2023 | 2 |
| 2024 | 2 |
| 2025 | 2 |

*(5 filas)*
<!-- /test -->

`strftime` devuelve **texto**. Si necesitás comparar con un número, convertilo: `CAST(strftime('%m', fecha) AS INTEGER)`.

---

## 9. La división entera de SQLite

Si dividís **dos enteros**, SQLite devuelve un **entero** (se descarta la parte decimal). Es una de las trampas más comunes al calcular porcentajes.

<!-- test: t-division -->
```sql
SELECT a.nombre AS actividad,
       a.cupo,
       COUNT(*) AS inscriptos,
       COUNT(*) / a.cupo        AS ocupacion_mal,
       1.0 * COUNT(*) / a.cupo  AS ocupacion_bien
FROM inscripciones i
JOIN actividades a ON a.id = i.actividad_id
GROUP BY a.id;
```

| actividad | cupo | inscriptos | ocupacion_mal | ocupacion_bien |
|---|---|---|---|---|
| Natación | 20 | 5 | 0 | 0.25 |
| Fútbol 5 | 10 | 4 | 0 | 0.4 |
| Yoga | 4 | 4 | 1 | 1 |

*(3 filas)*
<!-- /test -->

Natación (5 de 20) da `0` en vez de `0.25`. La solución: que **uno** de los dos números sea decimal (multiplicar por `1.0`, o por `100.0` si querés porcentaje).
**Siempre** conviene preguntarse: *"¿este resultado tiene sentido?"* (una ocupación nunca es 0 si hay gente inscripta).

---

## 10. Subconsultas y CTE

Una **subconsulta** es un `SELECT` adentro de otro, entre paréntesis. Sirve cuando necesitás un resultado intermedio.

<!-- test: t-subconsulta -->
```sql
-- Socios que tienen al menos una cuota impaga
SELECT nombre
FROM socios
WHERE id IN (SELECT socio_id FROM cuotas WHERE fecha_pago IS NULL);
```

| nombre |
|---|
| Diego Ruiz |
| Facundo Luna |
| Hugo Paz |

*(3 filas)*
<!-- /test -->

Cuando tenés varios pasos, se lee mejor con una **CTE** (`WITH nombre AS (…)`): le ponés nombre a cada paso intermedio y lo usás como si fuera una tabla.

<!-- test: t-cte -->
```sql
WITH deuda AS (
  SELECT socio_id, SUM(monto) AS adeudado
  FROM cuotas
  WHERE fecha_pago IS NULL
  GROUP BY socio_id
)
SELECT s.nombre, d.adeudado
FROM deuda d
JOIN socios s ON s.id = d.socio_id
ORDER BY d.adeudado DESC;
```

| nombre | adeudado |
|---|---|
| Facundo Luna | 50000 |
| Diego Ruiz | 25000 |
| Hugo Paz | 25000 |

*(3 filas)*
<!-- /test -->

Una subconsulta que devuelve **un solo valor** se puede usar para comparar cada fila contra un número global (un promedio, un máximo…):

<!-- test: t-subconsulta-escalar -->
```sql
-- Actividades más caras que el precio promedio de todas
SELECT nombre, precio_mensual
FROM actividades
WHERE precio_mensual > (SELECT AVG(precio_mensual) FROM actividades);
```

| nombre | precio_mensual |
|---|---|
| Natación | 18000 |
| Yoga | 15000 |

*(2 filas)*
<!-- /test -->

---

## 11. Funciones de ventana (introducción)

Una función de ventana calcula algo **mirando un grupo de filas, pero sin colapsarlas** (a diferencia de `GROUP BY`). Se escribe `función() OVER (PARTITION BY … ORDER BY …)`:

- `PARTITION BY x`: "reiniciá la cuenta para cada valor de x" (los grupos).
- `ORDER BY y`: "ordená dentro de cada grupo".
- Funciones típicas: `ROW_NUMBER()` (1, 2, 3…), `RANK()` (igual que la anterior pero los empates comparten posición).

<!-- test: t-ventana -->
```sql
SELECT barrio, nombre, fecha_alta,
       RANK() OVER (PARTITION BY barrio ORDER BY fecha_alta) AS antiguedad_en_el_barrio
FROM socios
ORDER BY barrio, antiguedad_en_el_barrio;
```

| barrio | nombre | fecha_alta | antiguedad_en_el_barrio |
|---|---|---|---|
| Almagro | Diego Ruiz | 2023-06-11 | 1 |
| Almagro | Gala Torres | 2025-01-12 | 2 |
| Caballito | Bruno Díaz | 2022-07-02 | 1 |
| Caballito | Elena Sosa | 2024-02-05 | 2 |
| Caballito | Hugo Paz | 2025-03-01 | 3 |
| Palermo | Ana Pérez | 2021-03-15 | 1 |
| Palermo | Carla Gómez | 2023-01-20 | 2 |
| Palermo | Facundo Luna | 2024-09-30 | 3 |

*(8 filas)*
<!-- /test -->

Para quedarte con "el primero de cada grupo" no podés filtrar la ventana directamente en el `WHERE`: se calcula en un paso (CTE o subconsulta) y se filtra en el siguiente.

<!-- test: t-ventana-primero -->
```sql
WITH rankeados AS (
  SELECT barrio, nombre, fecha_alta,
         RANK() OVER (PARTITION BY barrio ORDER BY fecha_alta) AS pos
  FROM socios
)
SELECT barrio, nombre, fecha_alta
FROM rankeados
WHERE pos = 1
ORDER BY barrio;
```

| barrio | nombre | fecha_alta |
|---|---|---|
| Almagro | Diego Ruiz | 2023-06-11 |
| Caballito | Bruno Díaz | 2022-07-02 |
| Palermo | Ana Pérez | 2021-03-15 |

*(3 filas)*
<!-- /test -->

---

## 12. Ejemplo completamente resuelto

**Pedido de la comisión directiva del club:** *"Queremos saber qué actividades están casi llenas y qué socios nos deben plata, para reforzar las cobranzas de los que más deben."*

No empecemos escribiendo SQL: primero **traducimos el pedido en preguntas concretas y decidimos las definiciones**.

| Pregunta de negocio | Decisión |
|---|---|
| ¿Qué es "casi llena"? | Inscriptos ÷ cupo ≥ 80 %. |
| ¿Qué es "deber"? | Una cuota con `fecha_pago` vacío (`NULL`). Se suma el `monto`. |
| ¿Quiénes "más deben"? | Los que deben **más de una cuota**. |

### Paso 1 · Mirar las tablas (explorar antes de preguntar)

<!-- test: t-ej-explorar -->
```sql
SELECT * FROM actividades;
```

| id | nombre | cupo | precio_mensual |
|---|---|---|---|
| 1 | Natación | 20 | 18000 |
| 2 | Fútbol 5 | 10 | 12000 |
| 3 | Yoga | 4 | 15000 |
| 4 | Ajedrez | 12 | 6000 |

*(4 filas)*
<!-- /test -->

### Paso 2 · Actividades casi llenas

Necesitamos **contar inscriptos por actividad** (un `JOIN` + `GROUP BY`) y quedarnos con los grupos que superan el 80 % del cupo (un `HAVING`, porque la condición usa `COUNT`). Ojo con la división entera: `1.0 *`.

<!-- test: t-ej-llenas -->
```sql
SELECT a.nombre AS actividad,
       a.cupo,
       COUNT(*) AS inscriptos,
       ROUND(100.0 * COUNT(*) / a.cupo, 0) AS ocupacion_pct
FROM inscripciones i
JOIN actividades a ON a.id = i.actividad_id
GROUP BY a.id
HAVING 1.0 * COUNT(*) / a.cupo >= 0.8
ORDER BY ocupacion_pct DESC;
```

| actividad | cupo | inscriptos | ocupacion_pct |
|---|---|---|---|
| Yoga | 4 | 4 | 100 |

*(1 fila)*
<!-- /test -->

Lectura paso a paso, en el orden en que SQLite lo ejecuta: **(1)** `FROM … JOIN`: junto cada inscripción con su actividad. **(2)** `GROUP BY a.id`: una fila por actividad. **(3)** `HAVING`: descarto las que no llegan al 80 %. **(4)** `SELECT`: calculo columnas. **(5)** `ORDER BY`.
Resultado: solo Yoga (4 de 4). *Ajedrez no aparece porque tiene 0 inscriptos; si quisiéramos verla igual tendríamos que usar `LEFT JOIN`.*

### Paso 3 · Quién debe y cuánto (manejo de NULL)

La deuda está en las cuotas donde `fecha_pago IS NULL`. Agrupamos por socio, sumamos, y nos quedamos con los que deben más de una cuota:

<!-- test: t-ej-deudores -->
```sql
SELECT s.nombre,
       s.barrio,
       COUNT(*) AS cuotas_impagas,
       SUM(c.monto) AS adeudado
FROM cuotas c
JOIN socios s ON s.id = c.socio_id
WHERE c.fecha_pago IS NULL
GROUP BY s.id
HAVING COUNT(*) > 1
ORDER BY adeudado DESC;
```

| nombre | barrio | cuotas_impagas | adeudado |
|---|---|---|---|
| Facundo Luna | Palermo | 2 | 50000 |

*(1 fila)*
<!-- /test -->

Fijate la diferencia: `WHERE c.fecha_pago IS NULL` filtra **filas** (antes de agrupar: solo las cuotas impagas), `HAVING COUNT(*) > 1` filtra **grupos** (después: socios con más de una).

### Paso 4 · Verificar (¿el resultado tiene sentido?)

Controles cruzados antes de entregar:

<!-- test: t-ej-control -->
```sql
SELECT (SELECT SUM(monto) FROM cuotas WHERE fecha_pago IS NULL) AS deuda_total,
       (SELECT SUM(adeudado) FROM (
          SELECT socio_id, SUM(monto) AS adeudado
          FROM cuotas WHERE fecha_pago IS NULL GROUP BY socio_id
        )) AS suma_de_las_deudas_por_socio,
       (SELECT COUNT(*) FROM cuotas) - (SELECT COUNT(fecha_pago) FROM cuotas) AS cuotas_impagas;
```

| deuda_total | suma_de_las_deudas_por_socio | cuotas_impagas |
|---|---|---|
| 100000 | 100000 | 4 |

*(1 fila)*
<!-- /test -->

La deuda total tiene que dar igual sumada directamente que sumando las deudas de cada socio, y las impagas = total − pagas. Si no cerrara, buscamos qué `JOIN` duplicó o descartó filas.

### Paso 5 · Escribir la definición y la conclusión

> **Definiciones.** "Casi llena" = inscriptos/cupo ≥ 80 %. "Deuda" = suma de cuotas sin fecha de pago.
> **Hallazgo.** Yoga está al 100 % (4/4); Facundo Luna debe 2 cuotas ($50.000).
> **Recomendación.** Abrir otro grupo de Yoga y llamar primero a quienes deben 2 cuotas.

Esta estructura (pregunta → definiciones → consulta → control → conclusión) es la que se espera en el proyecto.

---

## 13. Normalización: 1FN, 2FN y 3FN

Normalizar es **reorganizar una tabla para que cada dato viva en un solo lugar**. Evita repetir información (y que se desactualice) y permite agregar datos sin inventar filas.

**Punto de partida: una planilla "todo en una" del club**

| id | socio | barrio | actividades | precio |
|---|---|---|---|---|
| 1 | Ana Pérez | Palermo | Natación, Yoga | 18000, 15000 |
| 2 | Bruno Díaz | Caballito | Natación, Fútbol 5 | 18000, 12000 |
| 3 | Ana Pérez | Palermo | Yoga | 15000 |

Problemas: Ana aparece repetida (si se muda hay que corregirla en dos lugares), y hay celdas con varios valores.

### 1FN — una celda, un valor (sin grupos repetidos)

Una celda no puede tener una lista (`"Natación, Yoga"`), ni columnas tipo `actividad_1`, `actividad_2`. Cada combinación va en **su propia fila**:

| id | socio | barrio | actividad | precio |
|---|---|---|---|---|
| 1 | Ana Pérez | Palermo | Natación | 18000 |
| 2 | Ana Pérez | Palermo | Yoga | 15000 |
| 3 | Bruno Díaz | Caballito | Natación | 18000 |
| 4 | Bruno Díaz | Caballito | Fútbol 5 | 12000 |

### 2FN — cada dato depende de la clave *entera*

Cuando la clave está formada por **varias columnas** (acá: `socio + actividad`), no puede haber datos que dependan de solo una parte. El `precio` depende solo de la `actividad`, no del socio → hay que sacarlo a otra tabla.
*(Si la clave es una sola columna, como un `id`, la 2FN se cumple casi sin querer: no existen "partes" de la clave.)*

### 3FN — nada depende de otra columna que no sea la clave

Si `socio → barrio` (el barrio depende del socio, no de la inscripción), el barrio no debería repetirse en cada inscripción. Una **dependencia transitiva** es una cadena: `clave → A → B`. B se saca a la tabla de A.

**Después** — cada cosa en su tabla, unidas por claves:

| socios | | |
|---|---|---|
| **id** | nombre | barrio |
| 1 | Ana Pérez | Palermo |
| 2 | Bruno Díaz | Caballito |

| actividades | | |
|---|---|---|
| **id** | nombre | precio |
| 1 | Natación | 18000 |
| 2 | Yoga | 15000 |
| 3 | Fútbol 5 | 12000 |

| inscripciones | |
|---|---|
| **socio_id** → socios | **actividad_id** → actividades |
| 1 | 1 |
| 1 | 2 |
| 2 | 1 |
| 2 | 3 |

Para volver a ver la planilla original se usa un `JOIN`:

<!-- test: t-normalizada -->
```sql
SELECT s.nombre AS socio, s.barrio, a.nombre AS actividad, a.precio_mensual AS precio
FROM inscripciones i
JOIN socios s      ON s.id = i.socio_id
JOIN actividades a ON a.id = i.actividad_id
ORDER BY s.id, a.id
LIMIT 5;
```

| socio | barrio | actividad | precio |
|---|---|---|---|
| Ana Pérez | Palermo | Natación | 18000 |
| Ana Pérez | Palermo | Yoga | 15000 |
| Bruno Díaz | Caballito | Natación | 18000 |
| Bruno Díaz | Caballito | Fútbol 5 | 12000 |
| Carla Gómez | Palermo | Natación | 18000 |

*(5 filas)*
<!-- /test -->

**Cómo reconocer que hay que normalizar:** el mismo dato se repite en muchas filas; hay columnas numeradas (`causa_1`, `causa_2`); el mismo concepto está escrito de formas distintas (`Palermo`, `PALERMO`, `Palermo `); o para cambiar un dato tenés que tocar muchas filas.
**Cómo migrar:** (1) limpiar los valores, (2) crear las tablas nuevas con `PRIMARY KEY` y `FOREIGN KEY`, (3) llenarlas con `INSERT INTO … SELECT DISTINCT …` (primero las que otras necesitan, después las que las referencian), (4) verificar con un `JOIN` que se reconstruye lo original: misma cantidad de filas y mismos totales.

---

## 14. Orden en que SQLite ejecuta una consulta

Se escribe en un orden, pero se **ejecuta en otro**. Entenderlo explica casi todos los errores:

| # | Cláusula | Qué hace |
|---|---|---|
| 1 | `FROM` / `JOIN` | Arma el conjunto de filas de partida. |
| 2 | `WHERE` | Descarta filas. *(Todavía no existen los alias del `SELECT` ni las agregaciones.)* |
| 3 | `GROUP BY` | Agrupa. |
| 4 | `HAVING` | Descarta grupos. |
| 5 | `SELECT` | Calcula las columnas y los alias. |
| 6 | `ORDER BY` | Ordena. |
| 7 | `LIMIT` | Corta. |

Por eso: no se puede filtrar por una agregación en el `WHERE` (todavía no se calculó), y sí se puede ordenar por un alias (el `SELECT` ya corrió).
