# Consigna — Sesión 2 · Variante A: Torre de control

> ¿Nunca escribieron una consulta SQL, o hace mucho que no lo hacen? Antes de arrancar,
> dense una vuelta por
> [INTRODUCCION SQL Y DATOS.pdf](../../INTRODUCCION%20SQL%20Y%20DATOS.pdf) (15-20 minutos
> con lo básico que van a necesitar). Y cuando algo puntual no les cierre, tienen la
> [TEORIA.md](TEORIA.md) para consultar.

## Objetivo del día

Trabajar en equipo (4-6 personas, virtual, con IA) sobre **datos de verdad desordenados**: hacer
preguntas de negocio, traducirlas a consultas SQL, y **no creerle ciegamente a ningún número**
(ni al propio, ni al que les devuelva la IA) hasta haberlo verificado.

No es una prueba de memoria de SQL. La IA los puede ayudar a escribir consultas, pero **no sabe
qué hay adentro de sus datos** ni qué decisiones tomaron ustedes. Lo que se evalúa es si logran
llegar a un resultado **en el que puedan confiar** y explicar de dónde sale.

## El escenario

Son el **equipo de análisis de datos de la aerolínea** (ficticia, ambientada en Aerolíneas
Argentinas). El **Director de Operaciones** les pidió un informe sobre el **2025**:

> *"Necesito saber cómo estuvo la puntualidad y la ocupación de la red durante el año, con
> especial atención a las rutas federales, las que no pasan por Buenos Aires. ¿Dónde estamos
> mal? ¿Qué me recomendarían hacer?"*

Cada escuadra es el equipo de análisis que responde ese pedido.

> **Aviso:** todos los datos son **ficticios**, inventados para este taller. No tienen ninguna
> relación con los sistemas, datos o procesos reales de Aerolíneas Argentinas.

## Cómo empezar en 3 pasos

No hace falta instalar nada. Todo corre en el navegador.

1. **Abran el SQL Lab:** [abrir el SQL Lab](LINK_AL_LAB). Es un editor de SQL con la base ya cargada.
   Tienen el esquema (las tablas y sus columnas) a la izquierda.
2. **Exploren antes de preguntar.** Hagan click en cada tabla del panel izquierdo: eso arma un
   `SELECT * … LIMIT 10;` para ver cómo son los datos. Apretar **Ctrl/⌘ + Enter** ejecuta lo que
   escribieron. Si se equivocan en algo grave (un `DELETE`, un `UPDATE`), el botón **"Reiniciar base"**
   vuelve todo al principio.
3. **Armen el equipo de trabajo.** Decidan quién comparte pantalla y quién redacta el diccionario
   de métricas y el *prompt log* (ver Entregables). Después, arranquen con la P1. Si usan IA, empiecen
   por el botón **"Copiar esquema para la IA"** (lean la [GUIA_IA.md](GUIA_IA.md)).

## Cómo ejecutar cada cosa (paso a paso)

**Qué necesitan:** una computadora con un navegador actualizado (Chrome, Edge o Firefox) y **conexión a internet**
(el Lab descarga el motor de SQL al abrirse; la base de datos ya viene adentro). No se instala nada. Para guardar
sus archivos alcanza con un editor de texto simple (Bloc de notas, VS Code, el que tengan).

### 1. Abrir el Lab

Click en el link de arriba. Si prefieren tenerlo en su compu, descarguen `lab.html` y abranlo con **doble click**
(funciona igual, siempre con internet). Esperen unos segundos hasta que arriba a la derecha diga **"Motor listo"**:
hasta entonces los botones están apagados.

### 2. Escribir y ejecutar una consulta

1. Escriban la consulta en el cuadro de texto grande (o hagan click en una tabla del panel izquierdo para arrancar con un `SELECT`).
2. Apreten **Ctrl + Enter** (en Mac, **⌘ + Enter**) o el botón **▶ Ejecutar**.
3. El resultado aparece debajo, con la cantidad de filas. Si hay un error, sale un mensaje en español; **léanlo**, casi siempre dice qué revisar.

Pueden escribir **varias consultas seguidas separadas por `;`**: se ejecutan todas y se muestra el resultado de cada una.
Las líneas que empiezan con `--` son comentarios (SQL las ignora): úsenlas para anotar a qué pregunta responde cada consulta.

### 3. Guardar su trabajo (¡importante!)

**El Lab no guarda archivos.** Solo recuerda un historial en su navegador, y eso no es un respaldo confiable
(se puede borrar o no funcionar). Entonces:

- Creen un archivo de texto llamado **`consultas.sql`** (en el Bloc de notas: *Guardar como…* → tipo *Todos los archivos* → nombre `consultas.sql`, para que no quede como `.txt`).
- Cada vez que una consulta funcione, **cópienla ahí** con un comentario, por ejemplo: `-- P3: demora promedio por aeronave`.
- Ese archivo es uno de los entregables, y es lo que los salva si cierran la pestaña sin querer.

### 4. La base vive en el navegador de cada persona

- Cada integrante del equipo tiene **su propia copia** de la base. Lo que una persona cree o modifique (por ejemplo, las tablas de E5) **no lo ven los demás**.
- Si **recargan la página (F5)** o cierran la pestaña, la base **vuelve al principio**: se pierden las tablas que hayan creado y los `INSERT`, `UPDATE` o `DELETE` que hayan hecho. (El historial de consultas sí suele quedar.)
- Por eso, si llegan a E5, **guarden todo lo que ejecuten en `normalizacion.sql`**: si la base se reinicia, pegan el archivo y lo corren de nuevo.
- Para trabajar en equipo: que **una persona comparta pantalla y escriba**, y el resto proponga y revise; o que cada uno pruebe en su navegador y pasen al `consultas.sql` común lo que funcione.

### 5. Copiar resultados

En la barra **"Resultado"** (justo arriba de la tabla) hay tres botones: **Copiar JSON / CSV / Markdown**. Sirven para pegar un resultado en un chat con la IA o en el dashboard.
**"Copiar esquema para la IA"** (arriba) copia el esquema de la base listo para pegar en un prompt.

### 6. Armar el dashboard (extra E3)

1. Descarguen [dashboard_base.html](dashboard_base.html) y ábranlo con un editor de texto.
2. Busquen el bloque que empieza con `const DATA = {`. **Es lo único que hay que editar** (los comentarios del archivo explican cada campo).
3. En el Lab, ejecuten la consulta del gráfico y apreten **Copiar JSON**.
4. En el dashboard, **peguen ese JSON** en el campo `datos:` del gráfico que corresponda, reemplazando el de ejemplo. Después indiquen cómo se llaman *sus* columnas (`campoX`, `campoValor`, `series`…) y borren la línea `ejemplo: true`.
5. Para los 3 KPIs, escriban los números en `kpis` y la recomendación en `conclusion`.
6. **Guarden el archivo como `dashboard.html`** y ábranlo con doble click en el navegador (necesita internet para dibujar los gráficos).
7. Si una tarjeta aparece en rojo, no se rompió nada: el mensaje dice qué columna no encuentra. Revisen los nombres.

### 7. Entregar

Junten sus archivos (`consultas.sql`, el diccionario de métricas, el prompt log, `dashboard.html` y, si llegaron a E5,
el diccionario de normalización y `normalizacion.sql`) en una carpeta y entréguenla **como les indique su facilitador**
(por ejemplo, subiéndola a una carpeta compartida o comprimida en un `.zip`).

## Qué hay en la base

El esquema completo lo ven en el Lab. Este es el diccionario de datos:

| Tabla | Qué representa | Columnas |
|---|---|---|
| `aeropuertos` | Los aeropuertos de la red | `id`, `codigo_iata`, `nombre`, `ciudad`, `provincia`, `region` |
| `aeronaves` | Los aviones de la flota | `id`, `matricula`, `modelo`, `capacidad_asientos`, `anio_incorporacion` |
| `rutas` | Cada ruta es **un sentido** de un trayecto (la ida y la vuelta son rutas distintas) | `id`, `origen_id`, `destino_id` (los dos apuntan a `aeropuertos`), `distancia_km` |
| `vuelos` | Cada vuelo programado durante 2025 | `id`, `ruta_id`, `aeronave_id`, `fecha_programada`, `estado`, `minutos_demora`, `pasajeros` |
| `incidencias` | Los motivos registrados de una demora o cancelación (un vuelo puede tener más de una, o ninguna) | `id`, `vuelo_id`, `causa_id`, `minutos_imputados` |
| `causas_demora` | El catálogo de motivos | `id`, `descripcion`, `area_responsable` (Propia o Externa) |
| `reporte_legacy` | Un export de un **sistema anterior** de reportes (año 2024). **Solo se usa en el extra E5** | ver E5 |

Las fechas están guardadas como texto `AAAA-MM-DD`. Las columnas con `_id` son referencias a otra tabla
(las conectan los `JOIN`).

## Las preguntas

Tienen que responderlas con consultas SQL, y **dejar guardada cada consulta**. Las preguntas están
formuladas como las haría el Director; traducirlas a SQL es parte del trabajo.

**P1 · Reconozcan la base.** ¿Cuántos vuelos, rutas y aeronaves hay? ¿Qué estados de vuelo existen? ¿Qué período cubre?

**P2 · Los 10 vuelos con peor demora.** Y justifiquen qué hacen con los vuelos cancelados.

**P3 · Demora promedio y cantidad de vuelos de cada aeronave.** Por ahora alcanza con identificar a la aeronave por su `id`.

**P4 · Rehagan P3** mostrando la matrícula y el modelo en lugar del id. Después, calculen la **ocupación promedio por modelo** de avión.

**P5 · Las 10 rutas más ocupadas.** Mostrando el nombre del aeropuerto de origen y el de destino, y considerando solo las rutas que tengan **al menos 40 vuelos operados**.

**P6 · Puntualidad y causas.** ¿Qué porcentaje de puntualidad tiene cada región de origen? Y: ¿cuáles son las 3 causas que más minutos de demora acumulan?, separando las **propias** de las **externas**.

> **Importante: las definiciones las ponen ustedes.** No existe una única forma correcta de definir "puntual",
> ni de decidir qué pasa con los vuelos cancelados o desviados al calcular un promedio. Elijan una,
> **escríbanla en su diccionario de métricas** y úsenla **igual en todas las consultas**.
> La *ocupación* es el porcentaje de los asientos que se ocuparon.

## Extras (opcionales, en este orden)

Encaren los extras en orden. No hace falta llegar al final para que la actividad haya servido.

- **E1 · Evolución mensual.** Cantidad de vuelos operados, puntualidad y ocupación, mes por mes.
- **E2 · Rutas críticas.** Las rutas con una ocupación **por encima** del promedio general y una puntualidad **por debajo**. ¿Qué tienen en común?
- **E3 · Dashboard.** Armen el tablero con el [dashboard base](dashboard_base.html): 3 KPIs, línea mensual, barras con el top 10 de rutas críticas, causas propias vs externas, y una **recomendación de 3 líneas para el Director**. Los números del tablero **tienen que coincidir con los de sus consultas**.
- **E4 · (bonus) Funciones de ventana.** La peor ruta de cada región usando `RANK() OVER (PARTITION BY …)`.
- **E5 · (bonus) Normalización**, con la tabla `reporte_legacy`:
  - (a) Detecten y limpien los valores inconsistentes (la misma cosa escrita de distintas formas).
  - (b) Diagnostiquen qué formas normales se rompen (1FN, 2FN, 3FN) y por qué.
  - (c) Diseñen el esquema normalizado y créenlo con `CREATE TABLE`, con sus claves primarias y foráneas.
  - (d) Migren los datos con `INSERT INTO … SELECT DISTINCT …`.
  - (e) Validen que, con un `JOIN`, se reconstruye la tabla original ya limpia.

## Ritmo sugerido

Es una referencia, no una regla. Si se trabaron en algo, pidan ayuda al facilitador.

| Bloque | Tiempo |
|---|---|
| Explorar el Lab y la base | 10 min |
| P1 a P6 | ≈ 45 min |
| E1 + E2 | ≈ 20 min |
| E3 (dashboard y recomendación) | ≈ 20 min |
| E4 o E5 | 25-30 min c/u |

## Qué tienen que entregar

1. **Un archivo `.sql`** con todas sus consultas, cada una con un comentario que diga a qué pregunta responde.
2. **Un diccionario de métricas**: las decisiones que tomaron (qué es "puntual", qué hacen con los cancelados, qué hacen con los desviados, cómo calculan la ocupación) y por qué.
3. **El prompt log**: una copia de los prompts que usaron con la IA, y qué hicieron con la respuesta (la plantilla está en la [GUIA_IA.md](GUIA_IA.md)).
4. **El `dashboard.html`** (si llegaron a E3).
5. **Solo si llegaron a E5:** un **diccionario de normalización** (valor original → valor normalizado, y el criterio) y un archivo `normalizacion.sql`.

## Checklist de validación

Antes de entregar, comprueben cada punto. Si alguno no cierra, **hay un error en sus consultas
o en sus datos**, y encontrarlo es lo más valioso de la actividad.

- [ ] La **suma de vuelos por estado** coincide con el total de la tabla `vuelos`.
- [ ] **Ninguna ocupación** pasa del 100 %.
- [ ] Si el **total de minutos de demora** que calcularon (después de hacer un `JOIN`) da **más** que la suma directa sobre `vuelos`, el `JOIN` duplicó filas.
- [ ] Las rutas del ranking aparecen con **nombres**, no con números de id.
- [ ] La **definición de "puntual"** está escrita en el diccionario de métricas y **se aplica igual en todas las consultas**.
- [ ] Cada número del dashboard (E3) se puede **reproducir** con una de sus consultas.
- [ ] *(Solo E5)* Después de limpiar, **no quedan valores que difieran solamente en mayúsculas o en espacios**.
- [ ] *(Solo E5)* La **reconstrucción por `JOIN`** devuelve la misma cantidad de filas y los mismos minutos totales que la tabla original (ya limpia).
