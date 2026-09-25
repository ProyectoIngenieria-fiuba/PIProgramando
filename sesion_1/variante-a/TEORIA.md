# Teoría — Sesión 1 · Variante A

Referencia técnica puntual para esta actividad. No hace falta leerla entera
antes de arrancar — úsenla como consulta cuando algo del código no les cierre.

## 1. `document.querySelector` y `addEventListener`

`document.querySelector("#algo")` busca en el HTML el primer elemento que
matchea ese selector (igual que en CSS) y te devuelve el elemento para poder
leerlo o modificarlo desde JS.

```js
const boton = document.querySelector("#mi-boton");
const titulo = document.querySelector("h1");
const todasLasTarjetas = document.querySelectorAll(".tarjeta"); // todas, no solo la primera
```

`addEventListener` le dice a un elemento "cuando pase esto, ejecutá esta
función":

```js
boton.addEventListener("click", () => {
  console.log("me clickearon");
});
```

En este proyecto se usa, por ejemplo, para el botón de cambiar de tema
(`js/tema.js`).

## 2. Recorrer un array de objetos y pintar una lista en el HTML

El patrón típico es: por cada objeto del array, generar un pedacito de HTML
(un `<div>`, por ejemplo) y meterlo dentro de un contenedor.

```js
const frutas = [
  { nombre: "Banana", color: "amarillo" },
  { nombre: "Manzana", color: "rojo" },
];

const contenedor = document.querySelector("#lista-frutas");
contenedor.innerHTML = "";

frutas.forEach((fruta) => {
  const item = document.createElement("div");
  item.textContent = `${fruta.nombre} (${fruta.color})`;
  contenedor.appendChild(item);
});
```

Dos formas comunes de armar el contenido de cada elemento:

- `elemento.textContent = "..."` para texto simple.
- `elemento.innerHTML = \`...\`` con un *template string* (comillas invertidas)
  cuando necesitás mezclar HTML con variables, como en las tarjetas de
  sensores de este proyecto.

## 3. Un sitio con varias páginas y varios archivos JS (sin build step)

Este proyecto no usa `import`/`export` ni un bundler. Cada página HTML carga
sus scripts con etiquetas `<script src="...">` normales, en un orden
específico:

```html
<script src="js/datos.js"></script>
<script src="js/logica.js"></script>
<script src="js/ui-panel.js"></script>
```

Dos cosas importantes de este tipo de scripts ("clásicos", no módulos):

- **Se ejecutan en el orden en que aparecen en el HTML.** Si `ui-panel.js`
  usa algo definido en `datos.js`, `datos.js` tiene que estar en un
  `<script>` *anterior*. Si el orden estuviera invertido, el código fallaría
  con algo como `Uncaught ReferenceError: sensores is not defined`.
- **Comparten el mismo scope global.** Una variable declarada con `var` en
  un archivo es visible (y modificable) desde cualquier otro archivo
  cargado en la misma página. Esto es distinto a cuando cada archivo tiene
  su propio módulo — acá todos "viven en la misma habitación".

Eso segundo tiene una trampa: si **dos archivos distintos** declaran una
variable global con el mismo nombre usando `var`, no da ningún error — el
segundo valor simplemente pisa al primero, en silencio:

```js
// archivo-a.js
var contador = 10;

// archivo-b.js (cargado después)
var contador = 99; // 🐛 pisó el valor de archivo-a.js sin avisar

console.log(contador); // 99, y no hay forma de saberlo mirando un solo archivo
```

Con `let` o `const` en cambio, declarar la misma variable dos veces a nivel
global sí tira error (`Identifier 'contador' has already been declared`) —
molesto porque rompe la página, pero al menos te avisa altiro de que hay un
choque de nombres. Con `var`, el bug queda escondido hasta que alguien nota
que un valor no es el esperado.

Moraleja práctica para este proyecto: si un dato no cambia entre archivos,
busquen si ese mismo nombre de variable está declarado en más de un lugar.

## 4. Por qué emparejar por `id` es más seguro que por posición

Es común calcular algo a partir de un array (por ejemplo, un estado por cada
elemento) y guardarlo en un array paralelo, o guardar la *posición* de un
elemento para usarla después, asumiendo que esa posición sigue significando
lo mismo en otro array o en otro momento.

El problema es que esa suposición se rompe apenas **el orden de alguno de
los arrays cambia** (por ejemplo, si armás una copia ordenada
alfabéticamente para mostrarla, pero seguís usando una posición pensada para
el array original). El índice sigue siendo un número válido, así que no van
a ver ningún error en la consola — simplemente van a estar leyendo el dato
de **otro elemento**.

Ejemplo genérico (no es ningún bug real del proyecto, pero es el mismo
mecanismo):

```js
const estudiantes = [
  { id: "e1", nombre: "Juan" },
  { id: "e2", nombre: "Ana" },
  { id: "e3", nombre: "Beto" },
];

// Calculado en el orden ORIGINAL del array:
const aprobado = [true, false, true]; // e1: true, e2: false, e3: true

// Copia ordenada alfabéticamente para mostrar en pantalla:
const ordenados = [...estudiantes].sort((a, b) => a.nombre.localeCompare(b.nombre));
// ordenados queda: Ana, Beto, Juan

// 🐛 Usar el índice de "ordenados" para leer "aprobado" está mal:
ordenados.forEach((est, i) => {
  console.log(est.nombre, aprobado[i]); // Ana -> true (¡debería ser false!)
});
```

La forma segura es no depender de la posición, sino de un dato estable que
identifique a cada elemento — típicamente su `id`:

```js
// Alternativa 1: buscar por id cada vez
ordenados.forEach((est) => {
  const i = estudiantes.findIndex((e) => e.id === est.id);
  console.log(est.nombre, aprobado[i]);
});

// Alternativa 2: no depender de ningún array paralelo
function estaAprobado(estudiante) {
  // calculado directo sobre el objeto, sin importar en qué posición esté
}
```

Esta misma idea se puede colar en lugares donde no hay ningún "sort" a la
vista — por ejemplo, al usar una posición calculada en un array para buscar
algo en *otro* array que tiene un orden distinto. El mecanismo es el mismo:
una posición que tiene sentido en un array, usada por error sobre otro.

## 5. Leer datos de la URL con `URLSearchParams` (útil para `sensor.html`)

Cuando una página recibe parámetros en la URL (por ejemplo
`sensor.html?id=temp-nucleo`), se pueden leer así:

```js
const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id"); // "temp-nucleo"
```

Esto reemplaza a parsear el `location.search` a mano (partir por `?` y por
`=`), que es más propenso a errores.

## 6. `localStorage` (útil para el extra 3)

`localStorage` guarda datos en el navegador que **sobreviven a que
recargues la página o navegues a otra página del mismo sitio** (a
diferencia de una variable normal de JS, que se pierde apenas cambiás de
página). Por eso es la herramienta indicada cuando el historial de alertas
tiene que verse en `historial.html` después de haberse generado en
`panel.html`.

Solo guarda **strings**, así que para guardar objetos o arrays hay que
convertirlos con `JSON.stringify` al guardar y `JSON.parse` al leer:

```js
// Guardar
const historial = [{ sensor: "temp-nucleo", valor: 387 }];
localStorage.setItem("historialAlertas", JSON.stringify(historial));

// Leer (en cualquier página del mismo sitio, incluso después de recargar)
const guardado = localStorage.getItem("historialAlertas");
const historialLeido = guardado ? JSON.parse(guardado) : [];
```

Ojo con dos cosas:

- Si la clave no existe todavía, `getItem` devuelve `null`, no `[]` — hay
  que contemplarlo (como en el ejemplo de arriba).
- `localStorage` es por navegador y por sitio. No es una base de datos
  compartida: cada persona que abra el proyecto en su propia compu va a
  tener su propio historial guardado localmente.

Ya hay un ejemplo funcionando en el proyecto: `js/tema.js` usa
`localStorage` para recordar el tema claro/oscuro elegido. Es un buen lugar
para mirar un caso real y simple antes de escribir el del extra 3.

## 7. `setInterval` y `clearInterval` (útil para el extra 2)

`setInterval(funcion, milisegundos)` ejecuta `funcion` repetidamente cada
tantos milisegundos, y devuelve un identificador que sirve para detenerlo
después con `clearInterval`.

```js
let intervaloId = null;

function empezarSimulacion() {
  intervaloId = setInterval(() => {
    console.log("tick");
  }, 2000); // cada 2 segundos
}

function pararSimulacion() {
  clearInterval(intervaloId);
  intervaloId = null;
}
```

Un patrón común para un botón de "play/pause" es guardar el id del intervalo
en una variable de afuera, y usar `if (intervaloId)` para decidir si hay que
arrancar o frenar.

## 8. Mini-ejemplo completo: categorías de producto

Este ejemplo es un caso **distinto** al de este proyecto, pero usa el mismo
patrón de datos + render, para que puedan ver la solución aplicada a otro
problema y adaptar la idea (no copiar/pegar).

```js
const productos = [
  { id: "p1", nombre: "Taladro", categoria: "Herramientas", stock: 2 },
  { id: "p2", nombre: "Alambre", categoria: "Ferretería", stock: 40 },
  { id: "p3", nombre: "Guantes", categoria: "Seguridad", stock: 5 },
];

function calcularPocoStock(producto) {
  return producto.stock <= 5;
}
```

**Versión con el mismo tipo de bug** (calcula el estado en el orden
original, pero renderiza una copia ordenada por categoría, y empareja por
índice):

```js
function renderProductosConBug() {
  const pocoStock = productos.map(calcularPocoStock); // orden original: [p1, p2, p3]
  const ordenados = [...productos].sort((a, b) => a.categoria.localeCompare(b.categoria));
  // ordenados queda: Ferretería (p2), Herramientas (p1), Seguridad (p3)

  ordenados.forEach((producto, i) => {
    console.log(producto.nombre, pocoStock[i]); // 🐛 desalineado
  });
}
```

**Versión arreglada** (cada producto trae su propio estado, sin depender de
la posición en ningún array):

```js
function renderProductosBien() {
  const ordenados = [...productos].sort((a, b) => a.categoria.localeCompare(b.categoria));

  ordenados.forEach((producto) => {
    const esPocoStock = calcularPocoStock(producto); // se calcula sobre el objeto real, no por índice
    console.log(producto.nombre, esPocoStock);
  });
}
```

La clave del fix es que `calcularPocoStock(producto)` no necesita ningún
array paralelo ni ningún índice: recibe el objeto y devuelve su resultado
directamente, así que da lo mismo en qué orden lo recorras.
