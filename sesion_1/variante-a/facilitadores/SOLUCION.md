# Solución — Sesión 1 · Variante A

> ⚠️ **Uso exclusivo de facilitadores.** No compartir esta carpeta ni su
> contenido con las escuadras. Este archivo vive fuera de los materiales que
> reciben los participantes (`CONSIGNA.md`, `TEORIA.md`, `GUIA_IA.md`, y las
> 5 páginas HTML con sus `css/` y `js/`).

El proyecto tiene 3 bugs intencionales, repartidos en distintos archivos.
Los 3 son variantes del mismo problema de fondo (depender de la *posición*
de un dato en vez de su identidad/orden real), expresado de tres formas
distintas para que las escuadras lo encuentren más de una vez y el concepto
quede instalado.

Todos los fixes de esta guía fueron probados en el navegador antes de
documentarlos acá.

---

## Bug 1 — Colores de tarjeta desalineados (`js/ui-panel.js`)

### Causa

```js
const estados = calcularEstados(sensores); // orden original: [presión, temperatura, radiación]
//                                          //        valores: [verde,   rojo,        radiación]

function renderPanel() {
  const sensoresOrdenados = [...sensores].sort((a, b) => a.nombre.localeCompare(b.nombre));
  // sensoresOrdenados queda: [radiación, presión, temperatura]

  sensoresOrdenados.forEach((sensor, i) => {
    const estado = estados[i]; // 🐛 posición del array ORDENADO usada sobre el array ORIGINAL
    ...
  });
}
```

| i | sensor mostrado (dato) | `estados[i]` usado (color) | resultado |
|---|---|---|---|
| 0 | radiación | `estados[0]` = verde (presión) | verde — coincide por casualidad |
| 1 | presión | `estados[1]` = rojo (temperatura) | presión se ve **rojo** (mal) |
| 2 | temperatura | `estados[2]` = verde (radiación) | temperatura se ve **verde** (mal) |

### Fix

```js
sensoresOrdenados.forEach((sensor) => {
  const estado = calcularEstado(sensor); // ya no depende del índice ni de "estados"
  ...
});
```

`renderResumen()` no necesita cambios para esto — el conteo de
verde/amarillo/rojo ya usaba `estados` sin ordenar, y el total siempre fue
correcto (el bug afectaba a qué tarjeta se le asignaba cada color, no la
cantidad de cada uno).

---

## Bug 2 — "Sensores monitoreados" muestra 1 en vez de 3 (`js/datos.js` + `js/logica.js`)

### Causa

Los dos archivos declaran una variable global con el mismo nombre usando
`var` (no da error, la segunda pisa a la primera en silencio):

```js
// js/datos.js
var totalSensores = sensores.length; // = 3

// js/logica.js (se carga después)
var totalSensores = sensores.filter((s) => calcularEstado(s) !== "verde").length; // = 1
```

Como `logica.js` se carga después de `datos.js` en el `<script>` de cada
HTML, su asignación es la que queda. `js/ui-panel.js` lee `totalSensores`
esperando "cantidad total de sensores" y recibe "cantidad de sensores en
alerta" (1, porque solo la temperatura está fuera de verde).

Este es el único de los 3 bugs que requiere mirar **dos archivos JS**
distintos para encontrarlo — no hay forma de verlo mirando cualquiera de
los dos por separado.

### Fix

Renombrar la variable de `logica.js` para que no colisione:

```js
// js/logica.js
var sensoresEnAlerta = sensores.filter((s) => calcularEstado(s) !== "verde").length;
```

Con esto, `totalSensores` vuelve a ser exclusivamente el de `datos.js` (= 3).
`sensoresEnAlerta` queda disponible por si algún grupo lo quiere usar en
algo (no hace falta para el fix en sí).

Variante más robusta (opcional, vale mencionarla si el grupo pregunta): en
vez de variables globales sueltas con `var`, calcular ambos valores dentro
de `renderResumen()` en el momento de usarlos, sin exponer nada a nivel
global.

---

## Bug 3 — El detalle de sensor muestra otro sensor (`js/ui-sensor.js`)

### Causa

```js
const sensoresOrdenados = [...sensores].sort((a, b) => a.nombre.localeCompare(b.nombre));
const posicion = sensoresOrdenados.findIndex((sensor) => sensor.id === idBuscado); // correcto: posición DENTRO DEL ARRAY ORDENADO
const sensor = sensores[posicion]; // 🐛 esa posición se usa sobre el array ORIGINAL (sin ordenar)
```

`findIndex` está bien usado — encuentra la posición correcta dentro de
`sensoresOrdenados`. El error es indexar `sensores` (el array sin ordenar)
con esa posición, como si los dos arrays tuvieran el mismo orden.

Como `sensoresOrdenados` = [radiación, presión, temperatura] y `sensores` =
[presión, temperatura, radiación], el resultado es una rotación: cada
sensor te lleva al "siguiente" en el orden original.

| `?id=` pedido | posición en `sensoresOrdenados` | `sensores[posición]` mostrado |
|---|---|---|
| `rad-nivel` | 0 | presión (mal) |
| `presion-primario` | 1 | temperatura (mal) |
| `temp-nucleo` | 2 | radiación (mal) |

### Fix

La forma más simple: usar esa posición sobre el array del que realmente sale
(`sensoresOrdenados`), o directamente no calcular ninguna posición y buscar
por `id`:

```js
// Opción A — usar el array correcto
const sensor = sensoresOrdenados[posicion];

// Opción B — más directa, sin ordenar nada (esta página no muestra una lista)
const sensor = sensores.find((s) => s.id === idBuscado);
```

Cualquiera de las dos resuelve el síntoma. La opción B es más simple porque
esta página no necesita ordenar nada — el `sort` estaba de más acá, copiado
del patrón de `panel.html` donde sí hace falta.

### Resultado esperado tras los 3 fixes

- Panel de sensores: Presión → verde, Temperatura → rojo, Radiación → verde,
  "Sensores monitoreados" → 3.
- Detalle de sensor: cada tarjeta lleva al sensor correcto.

---

## Implementación esperada de los 4 extras

Referencia para evaluar lo que entreguen los grupos — no es la única
solución válida. Todo esto asume que los 3 bugs ya están arreglados.

### Extra 1 — Sensor nuevo: Nivel de refrigerante

En `js/datos.js`, agregar al array `sensores`:

```js
{
  id: "nivel-refrigerante",
  nombre: "Nivel de refrigerante",
  unidad: "%",
  valorActual: 92,
  verdeMin: 85, verdeMax: 100,
  rojoMin: 60, rojoMax: 100
}
```

Y sus entradas en los diccionarios:

```js
descripciones["nivel-refrigerante"] = "Mide el nivel de refrigerante disponible en el circuito de enfriamiento.";
iconos["nivel-refrigerante"] = "💧";
```

Con los bugs ya arreglados, el sensor nuevo debería aparecer solo en
`panel.html` **y** funcionar en su propia `sensor.html?id=nivel-refrigerante`
sin tocar nada más — esa es la señal de que entendieron el patrón.

### Extra 2 — Simulación en vivo (`js/ui-panel.js`)

Botón en `panel.html`, por ejemplo arriba de `#lista-sensores`:

```html
<button id="btn-simular">Simular lecturas</button>
```

En `js/ui-panel.js`, cambiar `estados` de `const` a reasignable y agregar el
toggle:

```js
let estados = calcularEstados(sensores);

let intervaloSimulacion = null;

function variarValor(sensor) {
  const rango = sensor.rojoMax - sensor.rojoMin;
  const variacion = (Math.random() - 0.5) * rango * 0.1;
  sensor.valorActual = +(sensor.valorActual + variacion).toFixed(2);
}

function simularLecturas() {
  sensores.forEach(variarValor);
  estados = calcularEstados(sensores);
  renderPanel();
}

function toggleSimulacion() {
  const boton = document.querySelector("#btn-simular");
  if (intervaloSimulacion) {
    clearInterval(intervaloSimulacion);
    intervaloSimulacion = null;
    boton.textContent = "Simular lecturas";
  } else {
    intervaloSimulacion = setInterval(simularLecturas, 3000);
    boton.textContent = "Detener simulación";
  }
}

document.querySelector("#btn-simular").addEventListener("click", toggleSimulacion);
```

Puntos a revisar: que el botón pueda detener la simulación (no solo
arrancarla), y que no se acumulen intervalos si lo clickean varias veces
seguidas.

### Extra 3 — Historial de alertas con `localStorage`

Como `panel.html` (donde se detectan las alertas) y `historial.html` (donde
se muestran) son páginas distintas, un array en memoria no alcanza — hay que
persistir en `localStorage`, usando la misma clave que ya lee
`js/ui-historial.js`:

```js
// en js/ui-panel.js
const CLAVE_HISTORIAL = "historialAlertas"; // debe coincidir con js/ui-historial.js
const estadosPrevios = {};

function registrarAlertas() {
  const historial = JSON.parse(localStorage.getItem(CLAVE_HISTORIAL) || "[]");

  sensores.forEach((sensor) => {
    const estadoActual = calcularEstado(sensor);
    if (estadoActual === "rojo" && estadosPrevios[sensor.id] !== "rojo") {
      historial.push({
        fecha: new Date().toISOString(),
        nombre: sensor.nombre,
        valor: sensor.valorActual,
        unidad: sensor.unidad,
      });
    }
    estadosPrevios[sensor.id] = estadoActual;
  });

  localStorage.setItem(CLAVE_HISTORIAL, JSON.stringify(historial));
}
```

Llamar `registrarAlertas()` tanto al iniciar el panel (así queda registrada
la alerta de Temperatura del núcleo, que arranca en rojo) como dentro de
`simularLecturas()` si ya hicieron el extra 2.

Variantes aceptables: registrar cada tick en rojo (sin trackear transición
con `estadosPrevios`) también es razonable para este nivel, aunque genere
una lista más ruidosa. Sacar `CLAVE_HISTORIAL` y esta lógica a un archivo
compartido (en vez de duplicar la clave en dos archivos) es un plus, no un
requisito.

### Extra 4 — Filtro de estado (`js/ui-panel.js`)

Checkbox en `panel.html`, por ejemplo junto al resumen:

```html
<label>
  <input type="checkbox" id="filtro-alertas">
  Mostrar solo sensores en alerta
</label>
```

En `js/ui-panel.js`:

```js
let soloAlertas = false;

document.querySelector("#filtro-alertas").addEventListener("change", (e) => {
  soloAlertas = e.target.checked;
  renderPanel();
});
```

Y en `renderPanel`, filtrar antes de recorrer:

```js
sensoresOrdenados
  .filter((sensor) => !soloAlertas || calcularEstado(sensor) !== "verde")
  .forEach((sensor) => { ... });
```

"En alerta" se puede interpretar como "no verde" (amarillo + rojo) o "solo
rojo" — cualquiera de las dos es válida siempre que el grupo lo explique;
la consigna no lo especifica a propósito.
