# Guía de uso de IA — Sesión 2 · Análisis de datos con SQL

Van a resolver esta actividad con ayuda de una IA (ChatGPT, Claude, Copilot, la que tengan a mano).
Esta guía es para que la usen **bien**: que les ahorre tiempo sin que dejen de entender qué números
están entregando.

La idea central: **la IA escribe SQL muy rápido, pero no conoce sus datos.** No sabe cómo están
escritos los valores, qué columnas tienen huecos ni qué decisiones tomaron ustedes. Cualquier consulta
que les devuelva es una **hipótesis a verificar**, no una respuesta.

## 1. Siempre pásenle el esquema y aclaren el motor

Una IA a la que no le dicen nada tiende a adivinar nombres de tablas y columnas, y a escribir
la sintaxis de otro motor (PostgreSQL, MySQL, SQL Server…). Acá el motor es **SQLite**, y tiene sus
particularidades.

**El camino corto:** en el SQL Lab, botón **"Copiar esquema para la IA"**. Copia un texto con el motor
aclarado, el `CREATE TABLE` de cada tabla y 3 filas de ejemplo. Pégenlo al principio de la conversación.

### Un prompt malo

> *Dame una consulta que calcule la demora promedio por avión.*

Qué le falta: no sabe de qué tablas hablan, cómo se llaman las columnas, ni qué motor usan. Va a inventar
(`flights`, `delay_minutes`…) o a usar funciones que no existen en SQLite.

### Un prompt bueno

> *Estoy trabajando con SQLite (no PostgreSQL). Este es mi esquema:* `[pegar lo que copió el botón]`
>
> *Quiero [lo que necesitan, en una frase de negocio]. Antes de escribir la consulta, decime
> qué supuestos estás haciendo sobre los datos. Después escribí la consulta, y debajo explicame
> línea por línea qué hace cada parte.*
>
> *No uses funciones que no existan en SQLite.*

### Otro ejemplo, con el club de barrio de la [TEORIA.md](TEORIA.md)

> Malo: *"Mostrame los socios que deben plata."*
>
> Bueno: *"SQLite. Esquema: [...]. Quiero la lista de socios con al menos una cuota sin pagar, con la cantidad
> de cuotas impagas y el monto total que deben, ordenado de mayor a menor deuda. Una cuota está impaga cuando
> `fecha_pago` está vacío. Explicame la consulta paso a paso."*

Qué cambió: **da la definición** ("impaga = fecha_pago vacío"), **pide el resultado exacto** (qué columnas, qué orden),
y **pide la explicación**. Cuanto más precisa sea su pregunta de negocio, mejor consulta van a recibir.

## 2. Exploren los datos *antes* de pedir una consulta

La IA no ve sus datos. Si le piden "los vuelos operados" sin saber cómo está escrito ese valor en la
columna, va a escribir lo que le parezca razonable, y puede estar mal sin darse cuenta.

Antes de cada pregunta importante, hagan ustedes una **exploración rápida** de las columnas que van a usar:

- ¿Qué **valores distintos** tiene una columna de texto? (`SELECT DISTINCT columna …` o `GROUP BY columna` con `COUNT(*)`).
- ¿Cuáles son el **mínimo y el máximo** de una columna numérica o de fechas?
- ¿Hay **`NULL`**? (`COUNT(*)` contra `COUNT(columna)` se los dice).
- ¿Los **totales cierran**? (la suma de las partes contra el total).

Y después **cuéntenle a la IA lo que encontraron**: *"la columna estado tiene estos valores: …"*. Eso vale más que cualquier
prompt largo.

## 3. Cómo leer una consulta que les devuelve la IA

No la copien y ejecuten sin leerla. Léanla **en el orden en que SQLite la ejecuta**, que no es el orden en que está escrita:

| Orden | Cláusula | Se pregunta... |
|---|---|---|
| 1 | `FROM` | ¿De qué tabla(s) salen las filas? |
| 2 | `JOIN … ON` | ¿Cómo se unen? ¿Puede una fila repetirse por la unión? ¿Se pierden filas? |
| 3 | `WHERE` | ¿Qué filas se descartan **antes** de agrupar? |
| 4 | `GROUP BY` | ¿Qué es "una fila" del resultado? |
| 5 | `HAVING` | ¿Qué grupos se descartan **después** de agrupar? |
| 6 | `SELECT` | ¿Qué columnas y cálculos aparecen? |
| 7 | `ORDER BY` / `LIMIT` | ¿Cómo se ordena y cuántas filas quedan? |

Truco: pídanle a la IA que **explique su propia consulta línea por línea**, y verifiquen que lo que dice coincide
con lo que ustedes querían. Si no pueden explicarle a un compañero qué hace una línea, no la acepten todavía.

## 4. Errores típicos que tienen que buscar

Revisen cada consulta contra esta lista antes de confiar en el resultado:

- [ ] **Sintaxis de otro motor.** Funciones o formas que no existen en SQLite (por ejemplo, las que vienen de PostgreSQL o MySQL).
      Si el Lab devuelve "no existe la función…", es esto: vuelvan a pedir aclarando **SQLite**.
- [ ] **Un `JOIN` que duplica filas.** Si unen una tabla con otra donde cada fila tiene varias parejas, la fila original se repite,
      y cualquier suma o conteo sale inflado. Comparen el total **antes y después** del `JOIN`.
- [ ] **`WHERE` vs `HAVING`.** Filtrar por una cantidad o un promedio (resultado de una agregación) va en `HAVING`.
- [ ] **`NULL`.** Los `NULL` no se comparan con `=` (se usa `IS NULL`), y las funciones como `AVG` o `SUM` los ignoran.
      ¿La consulta los está tratando como ustedes querían?
- [ ] **`COUNT(*)` vs `COUNT(columna)`.** No cuentan lo mismo. ¿Cuál necesitan?
- [ ] **Fechas.** En SQLite son texto `AAAA-MM-DD`. Para mes o año se usa `strftime`. ¿Agrupa por lo que ustedes pensaron?
- [ ] **División entera.** Dividir dos enteros devuelve un entero. Un porcentaje que da 0 o 1 es una señal de alarma.
- [ ] **`UPDATE` o `DELETE` sin `WHERE`.** Modifican **toda** la tabla. (En el Lab pueden "Reiniciar base", pero en la vida real no hay botón.)
- [ ] **Inventó algo.** Una columna que no existe, una tabla con otro nombre. El mensaje de error del Lab los ayuda a verlo.
- [ ] **Hizo una suposición que ustedes no tomaron.** ¿Qué entra en ese promedio? ¿Qué filas deja afuera? Pregúntenselo a la IA.

## 5. Cómo verificar el resultado

Una consulta que corre sin error **no está necesariamente bien**. Tres formas de comprobar:

1. **Pidan una consulta de control.** *"Escribime una segunda consulta, hecha de otra manera, que me permita comprobar el
   total de la primera."* Si las dos coinciden, ganan confianza; si no, encontraron un problema.
2. **Comparen totales antes y después de cada `JOIN` o filtro.** Cada vez que agregan una pieza a la consulta, ¿cambió
   la cantidad de filas o el total? Si cambió, ¿lo esperaban?
3. **Prueben con `LIMIT` y con un caso chico.** Miren 5 filas "a ojo" y hagan la cuenta a mano. Pidan un caso concreto
   (un solo vuelo, una sola ruta) y comprueben que el número coincide con lo que ven en los datos crudos.

Y siempre la pregunta de sentido común: **¿este número es razonable?** (una ocupación del 400 %, una puntualidad del 0 %, un
promedio idéntico al total…).

## 6. Cómo pedirle el dashboard a partir de sus JSON

En el SQL Lab, después de ejecutar una consulta, el botón **"Copiar JSON"** copia el resultado. Con el
[dashboard base](dashboard_base.html) hay dos formas de usarlo:

**A mano:** abran el archivo, busquen el bloque `const DATA = {…}` y peguen el JSON en el campo `datos` del
gráfico que corresponda. Indiquen en `campoX` / `campoValor` / `series` cómo se llaman **sus** columnas.

**Con ayuda de la IA:** pasenle el archivo y los JSON, y pídanle algo así:

> *Te paso mi archivo `dashboard_base.html`. Solo hay que modificar el objeto `const DATA`.*
> *Estos son los resultados de mis consultas, en JSON:*
> *— Consulta de KPIs: `[…]`*
> *— Consulta mensual: `[…]`*
> *— Consulta del top de rutas: `[…]`*
> *— Consulta de causas: `[…]`*
> *Completá `DATA` con estos datos: ajustá `campoX`, `campoValor`, `series` al nombre de mis columnas, borrá los
> `ejemplo: true`, y no toques nada del código que está debajo del bloque DATA. Después devolveme solo el bloque DATA modificado.*

Cuando lo abran en el navegador, **comparen los números del tablero con los de sus consultas**: tienen que coincidir.
Si una tarjeta muestra un error en rojo, dice qué columna no encuentra.

## 7. Plantilla de prompt log

Llevar el registro de qué le pidieron a la IA **y qué hicieron con la respuesta** es parte de la entrega.
Una tabla alcanza (pueden copiarla):

| # | Pregunta (P1, P2…) | Prompt que usé (pegado completo) | Qué devolvió la IA (resumen) | ¿Lo verifiqué? ¿Cómo? | ¿Lo acepté, lo corregí o lo descarté? ¿Por qué? |
|---|---|---|---|---|---|
| 1 | P1 | *"SQLite. Esquema: … Quiero saber cuántos…"* | Una consulta con 3 subconsultas | Corrí el `COUNT(*)` por mi cuenta y coincide | La acepté |
| 2 | P5 | *"…"* | *"…"* | *"…"* | *"…"* |

Dos reglas para que el log sirva de verdad:

- Anoten **también lo que la IA hizo mal**: es lo más útil para aprender.
- Si cambian de opinión sobre una definición, anótenlo (y actualicen el diccionario de métricas).

## 8. Cómo iterar sin dar vueltas en círculo

- Si la consulta no da lo esperado, **cuéntenle qué ven ahora con datos concretos**
  (*"me devuelve miles de filas y debería devolver 10"*), en vez de repetir "no funciona".
- Sigan en la misma conversación, así no pierde el contexto.
- Si propone reescribir todo de cero, el prompt probablemente necesita **más contexto específico**, no una reescritura.
- Cuando algo funcione, **escríbanlo en el `.sql`** enseguida, con un comentario de qué pregunta responde.
