# Teoría — Sesión 1 · Variante B

Referencia técnica puntual para esta actividad. No hace falta leerla entera
antes de arrancar — úsenla como consulta cuando algo del código no les cierre.

## 1. `document.querySelector` y `addEventListener`

`document.querySelector("#algo")` busca en el HTML el primer elemento que
matchea ese selector (igual que en CSS) y te devuelve el elemento para poder
leerlo o modificarlo desde JS.

```js
const titulo = document.querySelector("h1");
const todosLosItems = document.querySelectorAll(".item"); // todos, no solo el primero
```

`addEventListener` le dice a un elemento "cuando pase esto, ejecutá esta
función":

```js
boton.addEventListener("click", () => {
  console.log("me clickearon");
});
```

Van a necesitar esto, por ejemplo, para el extra 2 (marcar un lanzamiento
como favorito con un click) y para el toggle de tema (`js/tema.js`).

## 2. Recorrer un array de objetos y pintar una lista en el HTML

El patrón típico es: por cada objeto del array, generar un pedacito de HTML
y meterlo dentro de un contenedor.

```js
const lanzamientos = [
  { mision: "Ceibo-1", fechaHora: new Date() },
  { mision: "Jacarandá-2", fechaHora: new Date() },
];

const contenedor = document.querySelector("#lista-lanzamientos");
contenedor.innerHTML = "";

lanzamientos.forEach((lanzamiento) => {
  const item = document.createElement("li");
  item.textContent = lanzamiento.mision;
  contenedor.appendChild(item);
});
```

## 3. Un sitio con varias páginas y varios archivos JS (sin build step)

Este proyecto no usa `import`/`export` ni un bundler. Cada página HTML carga
sus scripts con etiquetas `<script src="...">` normales, en un orden
específico:

```html
<script src="js/datos.js"></script>
<script src="js/logica.js"></script>
<script src="js/ui-lanzamientos.js"></script>
```

Dos cosas importantes de este tipo de scripts ("clásicos", no módulos):

- **Se ejecutan en el orden en que aparecen en el HTML.** Si
  `ui-lanzamientos.js` usa algo definido en `datos.js`, `datos.js` tiene
  que estar en un `<script>` *anterior*.
- **Comparten el mismo scope global.** Una variable declarada con `var` en
  un archivo es visible (y modificable) desde cualquier otro archivo
  cargado en la misma página — todos "viven en la misma habitación".

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
molesto porque rompe la página, pero al menos avisa altiro de que hay un
choque de nombres. Con `var`, el bug queda escondido hasta que alguien nota
que un valor no es el esperado. Moraleja práctica: si un dato no cambia
entre archivos, busquen si ese mismo nombre de variable está declarado en
más de un lugar.

## 4. `setInterval` y `clearInterval`

Este es el concepto central del bug principal de esta variante, no solo de
un extra.

`setInterval(funcion, milisegundos)` ejecuta `funcion` repetidamente cada
tantos milisegundos, y devuelve un identificador que sirve para detenerlo
después con `clearInterval`.

```js
let intervaloId = null;

intervaloId = setInterval(() => {
  console.log("tick"); // se ejecuta cada 1000ms, para siempre
}, 1000);

clearInterval(intervaloId); // en algún momento, cuando corresponda parar
```

Un punto clave: **`setInterval` no sabe cuándo tiene que parar por sí
solo**. Alguien tiene que revisar, en cada tick, si ya se cumplió la
condición de corte, y llamar a `clearInterval` en ese momento. Si esa
condición nunca se cumple (por ejemplo, porque compara contra algo que no
es lo que debería), el intervalo sigue disparando para siempre, aunque ya
no tenga sentido.

Un error común es calcular bien el valor que se muestra en pantalla, pero
chequear la condición de corte contra **otra cosa** — por ejemplo, contra
un texto ya formateado para mostrar, en vez de contra el número del que
salió ese texto:

```js
const texto = `Faltan ${segundos}s`; // pensado solo para mostrar en pantalla

if (texto === "Faltan 0s") { // 🐛 frágil: depende de que el string arme EXACTO ese texto
  clearInterval(intervaloId);
}
```

Formatear un número para mostrarlo y decidir la lógica en base a ese mismo
número son dos cosas distintas — el texto es para el usuario, la condición
de corte debería apoyarse en el número de origen.

## 5. Trabajar con `Date` en JS

`new Date()` te da la fecha y hora actual. Restar dos objetos `Date` te da
la diferencia entre ellos **en milisegundos** (como si fueran números):

```js
const ahora = new Date();
const fechaFutura = new Date(ahora.getTime() + 5000); // 5 segundos después

const diferenciaMs = fechaFutura - ahora; // 5000 (aproximadamente)
```

Para armar un countdown de días/horas/minutos/segundos a partir de una
diferencia en milisegundos, se va dividiendo:

```js
function formatear(diferenciaMs) {
  const totalSegundos = Math.floor(diferenciaMs / 1000);
  const dias = Math.floor(totalSegundos / 86400);
  const horas = Math.floor((totalSegundos % 86400) / 3600);
  const minutos = Math.floor((totalSegundos % 3600) / 60);
  const segundos = totalSegundos % 60;
  return { dias, horas, minutos, segundos };
}
```

Ojo con los negativos: si `diferenciaMs` ya es negativo, `Math.floor` sobre
un número negativo redondea hacia "más negativo todavía" (`Math.floor(-0.5)`
da `-1`, no `0`), así que conviene sacar el signo aparte y trabajar con el
valor absoluto si necesitan mostrar un negativo prolijo.

## 6. Leer datos de la URL con `URLSearchParams` (útil para `lanzamiento.html`)

Cuando una página recibe parámetros en la URL (por ejemplo
`lanzamiento.html?id=ceibo-1`), se pueden leer así:

```js
const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id"); // "ceibo-1"
```

Una vez que tienen el `id`, hay que usar **ese objeto específico** para
cualquier cálculo relacionado (por ejemplo, su propia fecha) — no otro
objeto que tengan a mano en el archivo, aunque el nombre de esa otra
variable se parezca. Dos variables con nombres parecidos
(`lanzamiento` y `lanzamientos[0]`, por ejemplo) pueden representar cosas
completamente distintas, y el motor de JS no va a avisarles si usan la que
no corresponde — ambas son válidas, solo que una no es la que el usuario
pidió.

## 7. `localStorage` (útil para los extras 2 y 3)

`localStorage` guarda datos en el navegador que **sobreviven a que
recargues la página o navegues a otra página del mismo sitio** (a
diferencia de una variable normal de JS, que se pierde apenas cambiás de
página). Por eso es la herramienta indicada para el lanzamiento favorito
(extra 2) y para que `pasados.html` pueda mostrar lanzamientos que se
movieron desde `lanzamientos.html` (extra 3).

Solo guarda **strings**, así que para guardar objetos o arrays hay que
convertirlos con `JSON.stringify` al guardar y `JSON.parse` al leer:

```js
// Guardar
const favorito = "ceibo-1";
localStorage.setItem("lanzamientoFavorito", favorito);

// Leer (incluso después de recargar la página o cambiar de página)
const guardado = localStorage.getItem("lanzamientoFavorito"); // "ceibo-1" o null
```

Para algo más complejo que un string suelto (por ejemplo, la lista de
lanzamientos pasados):

```js
const pasados = [{ mision: "Ceibo-1", fechaHora: "2026-09-24T23:30:00.000Z" }];
localStorage.setItem("lanzamientosPasados", JSON.stringify(pasados));

const guardado = localStorage.getItem("lanzamientosPasados");
const pasadosLeidos = guardado ? JSON.parse(guardado) : [];
```

Si la clave no existe todavía, `getItem` devuelve `null`, no `[]` — siempre
hay que contemplar ese caso antes de hacer `JSON.parse`. Ya hay un ejemplo
funcionando en el proyecto: `js/tema.js` usa `localStorage` para recordar
el tema claro/oscuro elegido.

## 8. Mini-ejemplo completo: cierre de inscripción

Este ejemplo es un caso **distinto** al de este proyecto, pero usa el mismo
patrón completo de countdown + corte de intervalo, para que puedan ver la
solución aplicada a otro problema y adaptar la idea (no copiar/pegar).

```js
const cierreInscripcion = new Date(Date.now() + 8000); // en 8 segundos, de ejemplo
let intervaloInscripcion = null;

function actualizarCierre() {
  const ahora = new Date();
  const diferenciaMs = cierreInscripcion - ahora;

  if (diferenciaMs <= 0) {
    document.querySelector("#estado-inscripcion").textContent = "Inscripción cerrada";
    clearInterval(intervaloInscripcion);
    return;
  }

  const segundosRestantes = Math.ceil(diferenciaMs / 1000);
  document.querySelector("#estado-inscripcion").textContent =
    `Cierra en ${segundosRestantes} segundos`;
}

intervaloInscripcion = setInterval(actualizarCierre, 1000);
actualizarCierre();
```

La clave del patrón: la condición que decide si hay que parar
(`diferenciaMs <= 0`) se calcula **directo sobre el número** (la diferencia
en milisegundos), no sobre el texto que se arma después para mostrarlo en
pantalla. El texto es solo para el usuario; la lógica se apoya en el
número.
