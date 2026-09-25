# Solución — Sesión 1 · Variante B

> ⚠️ **Uso exclusivo de facilitadores.** No compartir esta carpeta ni su
> contenido con las escuadras. Este archivo vive fuera de los materiales que
> reciben los participantes (`CONSIGNA.md`, `TEORIA.md`, `GUIA_IA.md`, y las
> 5 páginas HTML con sus `css/` y `js/`).

El proyecto tiene 3 bugs intencionales, repartidos en distintos archivos.
Los 3 comparten la misma idea de fondo (una parte del código usa un valor
"parecido" al correcto, pero no el correcto), expresada de tres formas
distintas. Todos los fixes de esta guía fueron probados en el navegador
antes de documentarlos acá.

---

## Bug 1 — El countdown nunca se detiene (`js/ui-lanzamientos.js`)

### Causa

```js
function formatearTiempo(diferenciaMs) {
  ...
  const dias = Math.floor(totalSegundos / 86400); // sin padding: "0d", "1d", "2d"...
  return `${signo}${dias}d ${pad(horas)}h ${pad(minutos)}m ${pad(segundos)}s`;
}

function actualizarCountdown() {
  ...
  tiempoRestanteTexto = formatearTiempo(diferenciaMs);
  document.querySelector("#countdown-tiempo").textContent = tiempoRestanteTexto;

  if (tiempoRestanteTexto === "00d 00h 00m 00s") { // 🐛 "00d" con dos ceros
    clearInterval(intervaloId);
    ...
  }
}
```

`dias` nunca se formatea con `pad()`, así que cuando faltan cero días el
string real que se produce es `"0d 00h 00m 00s"` (un solo cero). La
condición de corte compara contra `"00d 00h 00m 00s"` (dos ceros) — un
string que `formatearTiempo` **nunca** produce. La comparación `===` nunca
es `true`, `clearInterval` nunca se ejecuta, y el countdown sigue
actualizándose para siempre, cada vez más negativo.

Es un bug determinista (no depende de timing): probado en el navegador con
un lanzamiento a pocos segundos, el contador pasa de `"0d 00h 00m 00s"` a
`"-0d 00h 00m 01s"` y sigue bajando indefinidamente, siempre.

### Fix

Comparar la diferencia numérica contra `0`, no el texto formateado:

```js
function actualizarCountdown() {
  const proximo = lanzamientos[0];
  const ahora = new Date();
  const diferenciaMs = proximo.fechaHora - ahora;

  if (diferenciaMs <= 0) {
    document.querySelector("#countdown-tiempo").textContent = "0d 00h 00m 00s";
    document.querySelector("#countdown-estado").textContent = "¡Lanzado! 🚀";
    document.querySelector("#countdown").classList.add("countdown--lanzado");
    clearInterval(intervaloId);
    return;
  }

  tiempoRestanteTexto = formatearTiempo(diferenciaMs);
  document.querySelector("#countdown-tiempo").textContent = tiempoRestanteTexto;
}
```

Probado en el navegador: con este cambio, el countdown llega a
`"0d 00h 00m 00s"`, se congela ahí, y el estado cambia a "¡Lanzado! 🚀" de
forma consistente en cada corrida.

---

## Bug 2 — "Lanzamientos programados" muestra 3 en vez de 5 (`js/datos.js` + `js/logica.js`)

### Causa

Los dos archivos declaran una variable global con el mismo nombre usando
`var` (no da error, la segunda pisa a la primera en silencio):

```js
// js/datos.js
var totalLanzamientos = lanzamientos.length; // = 5

// js/logica.js (se carga después)
var totalLanzamientos = lanzamientos.filter(
  (l) => l.fechaHora - new Date() < 7 * 24 * 60 * 60 * 1000
).length; // = 3 (con las fechas por defecto: Ceibo-1, Jacarandá-2 y Aconcagua Sat caen dentro de los 7 días)
```

Como `logica.js` se carga después de `datos.js`, su asignación es la que
queda. `js/ui-lanzamientos.js` lee `totalLanzamientos` esperando "cantidad
total de lanzamientos" y recibe "cantidad de lanzamientos en los próximos 7
días". Requiere mirar **dos archivos JS** distintos para encontrarlo — no
hay forma de verlo mirando cualquiera de los dos por separado.

### Fix

Renombrar la variable de `logica.js` para que no colisione:

```js
// js/logica.js
var lanzamientosProximaSemana = lanzamientos.filter(
  (l) => l.fechaHora - new Date() < 7 * 24 * 60 * 60 * 1000
).length;
```

Con esto, `totalLanzamientos` vuelve a ser exclusivamente el de `datos.js`
(= 5). Probado en el navegador: el resumen pasa a mostrar "5".

---

## Bug 3 — El countdown del detalle no corresponde al lanzamiento (`js/ui-lanzamiento.js`)

### Causa

```js
const idBuscado = parametros.get("id");
const lanzamiento = lanzamientos.find((l) => l.id === idBuscado); // esto está bien: encuentra el lanzamiento correcto

function actualizarCountdownDetalle() {
  const ahora = new Date();
  const diferenciaMs = lanzamientos[0].fechaHora - ahora; // 🐛 usa el próximo lanzamiento GLOBAL, no el de esta página
  ...
}
```

`lanzamiento` (el objeto correcto, encontrado por `id`) y `lanzamientos[0]`
(el próximo lanzamiento en general, casi siempre otro) son dos variables
con nombres muy parecidos que representan cosas distintas. El nombre de la
misión y la fecha programada que se muestran en pantalla usan `lanzamiento`
(están bien), pero el countdown en vivo de esa misma página usa
`lanzamientos[0]` por error.

Síntoma: entrar al detalle de cualquier lanzamiento que no sea el más
próximo (por ejemplo, Copihue Austral, a ~25 días) muestra su fecha
correcta, pero un countdown que corre como si faltaran un par de minutos —
el de Ceibo-1. Probado en el navegador: con el bug, `lanzamiento.html?id=copihue-austral`
muestra la fecha de Copihue pero un countdown de `"0d 00h 01m 29s"`.

### Fix

Usar `lanzamiento` (el que corresponde al `id` de la URL), no
`lanzamientos[0]`:

```js
function actualizarCountdownDetalle() {
  const ahora = new Date();
  const diferenciaMs = lanzamiento.fechaHora - ahora;
  ...
}
```

Probado en el navegador: con este cambio, el countdown de Copihue Austral
pasa a mostrar algo del orden de `"24d 23h 59m ..."`, consistente con su
fecha programada.

### Resultado esperado tras los 3 fixes

- `lanzamientos.html`: el countdown de Ceibo-1 se congela en cero y muestra
  "¡Lanzado! 🚀"; "Lanzamientos programados" muestra 5.
- `lanzamiento.html`: el countdown de cada lanzamiento corresponde a su
  propia fecha.

---

## Implementación esperada de los 4 extras

Referencia para evaluar lo que entreguen los grupos — no es la única
solución válida. Todo esto asume que los 3 bugs ya están arreglados.

### Extra 1 — Lanzamiento nuevo

Agregar un objeto más al array `lanzamientos` en `js/datos.js`:

```js
{ id: "huemul-4", mision: "Huemul-4", fechaHora: dentroDe(18 * 24 * 60) }
```

Y su descripción en el diccionario `descripciones`. Con los bugs ya
arreglados, debería aparecer solo en la lista de `lanzamientos.html` y
funcionar en su propia `lanzamiento.html?id=huemul-4` sin tocar nada más.

### Extra 2 — Lanzamiento favorito con `localStorage` (`lanzamientos.html`)

```js
const CLAVE_FAVORITO = "lanzamientoFavorito";

function alternarFavorito(id) {
  const actual = localStorage.getItem(CLAVE_FAVORITO);
  if (actual === id) {
    localStorage.removeItem(CLAVE_FAVORITO);
  } else {
    localStorage.setItem(CLAVE_FAVORITO, id);
  }
  renderLista();
}
```

En `renderLista`, agregar un botón/estrella por ítem y usar **delegación de
eventos** (un solo listener en el contenedor, porque la lista se
re-renderiza con `innerHTML =` y los listeners viejos se pierden):

```js
document.querySelector("#lista-lanzamientos").addEventListener("click", (e) => {
  if (e.target.matches(".lanzamiento-item__favorito")) {
    alternarFavorito(e.target.dataset.id);
  }
});
```

Punto a revisar: que el favorito **sobreviva a un F5** — esa es la prueba
real de que están usando `localStorage` y no solo una variable de JS.

### Extra 3 — Panel de lanzamientos pasados (reutiliza el fix del bug 1)

Como `lanzamientos.html` (donde se detecta que un countdown llegó a cero) y
`pasados.html` (donde se muestra) son páginas distintas, hay que persistir
en `localStorage`, usando la misma clave que ya lee `js/ui-pasados.js`:

```js
// en js/ui-lanzamientos.js
const CLAVE_PASADOS = "lanzamientosPasados"; // debe coincidir con js/ui-pasados.js

function moverAPasados(lanzamiento) {
  const pasados = JSON.parse(localStorage.getItem(CLAVE_PASADOS) || "[]");
  pasados.push(lanzamiento);
  localStorage.setItem(CLAVE_PASADOS, JSON.stringify(pasados));
}

function actualizarCountdown() {
  const proximo = lanzamientos[0];
  if (!proximo) {
    document.querySelector("#countdown-mision").textContent = "No hay más lanzamientos próximos";
    document.querySelector("#countdown-tiempo").textContent = "";
    clearInterval(intervaloId);
    return;
  }

  const ahora = new Date();
  const diferenciaMs = proximo.fechaHora - ahora;

  if (diferenciaMs <= 0) { // la misma condición del fix del bug 1
    moverAPasados(lanzamientos.shift());
    renderLista();
    document.querySelector("#countdown-mision").textContent =
      lanzamientos[0]?.mision ?? "No hay más lanzamientos próximos";
    return;
  }

  tiempoRestanteTexto = formatearTiempo(diferenciaMs);
  document.querySelector("#countdown-tiempo").textContent = tiempoRestanteTexto;
}
```

Buena señal de si el grupo entendió el fix del bug 1: si resuelven este
extra reusando `diferenciaMs <= 0` en vez de reinventar una comparación por
string, probablemente internalizaron por qué fallaba.

### Extra 4 — Filtro/orden de la lista

Extra deliberadamente abierto. Dos implementaciones razonables:

**Opción simple**: un link o botón en `lanzamientos.html` que lleve a
`pasados.html` (ya cumple "separar por estado", apoyándose en el extra 3).

**Opción más completa**: un `<select>` en `lanzamientos.html` para elegir
entre "por fecha" (el orden natural del array) y "por estado", re-ordenando
`lista-lanzamientos` según la opción elegida. Cualquiera de las dos cumple
el objetivo del extra.
