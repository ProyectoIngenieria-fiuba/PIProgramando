# Teoría — lo mínimo de JS para resolver el filtro

No hace falta leer esto de punta a punta antes de empezar. Úsenlo como
referencia cuando la IA les devuelva código y no entiendan alguna parte, o
cuando quieran verificar si lo que generó tiene sentido.

## 1. `.filter()` en arrays

`.filter()` es un método que tienen todos los arrays en JavaScript. Recibe
una función, la aplica a cada elemento, y devuelve un **array nuevo** solo
con los elementos para los que esa función devolvió `true`.

```js
const numeros = [1, 2, 3, 4, 5, 6];

const pares = numeros.filter(function (numero) {
  return numero % 2 === 0;
});

console.log(pares); // [2, 4, 6]
console.log(numeros); // [1, 2, 3, 4, 5, 6]  <- el original no cambia
```

Puntos clave:
- El array original (`numeros`) **no se modifica**. `.filter()` siempre
  devuelve uno nuevo.
- La función que le pasan a `.filter()` se ejecuta una vez por cada
  elemento, y decide si ese elemento "pasa el filtro" (`true`) o no
  (`false`).

Esto es exactamente lo que necesitan para `filtrarVuelosPorDestino`: recorrer
la lista de vuelos y quedarse solo con los que coincidan con la búsqueda.

## 2. Strings: comparar texto ignorando mayúsculas y tildes

### `.toLowerCase()`

Convierte todo el string a minúsculas. Sirve para que la comparación no
dependa de cómo escribió el usuario:

```js
"BARILOCHE".toLowerCase(); // "bariloche"
```

### `.includes()`

Devuelve `true` si un string contiene a otro como substring (coincidencia
parcial, no hace falta que sea igual):

```js
"Bariloche".includes("bari"); // false! "Bariloche" tiene mayúscula inicial
"bariloche".toLowerCase().includes("bari"); // true
```

Por eso conviene pasar ambos strings a minúsculas *antes* de comparar.

### Sacar tildes con `.normalize()`

Este es el truco para que `"cordoba"` encuentre `"Córdoba"`. JavaScript tiene
un método `.normalize("NFD")` que separa cada letra con tilde en dos partes:
la letra base y el "acento" como un carácter aparte (invisible). Después,
con `.replace()` y una expresión regular, se puede borrar esos acentos
sueltos:

```js
function sacarTildes(texto) {
  return texto.normalize("NFD").replace(/[̀-ͯ]/g, "");
}

sacarTildes("Córdoba"); // "Cordoba"
sacarTildes("Bariloche"); // "Bariloche" (no tiene tildes, no cambia nada)
```

No hace falta entender en detalle qué es `̀-ͯ` (son los códigos
Unicode de los acentos combinables) — alcanza con saber que esta función
"limpia" los tildes de un string. Combinando esto con `.toLowerCase()` y
`.includes()` ya tienen todo lo necesario para el básico.

## 3. Funciones flecha (`=>`)

Es una forma más corta de escribir funciones. Estas dos funciones hacen
exactamente lo mismo:

```js
// Función tradicional
function alCuadrado(numero) {
  return numero * numero;
}

// Función flecha
const alCuadrado = (numero) => {
  return numero * numero;
};

// Función flecha "corta" (cuando el cuerpo es una sola expresión con return)
const alCuadrado = (numero) => numero * numero;
```

Es muy probable que la IA les devuelva el código usando funciones flecha
(es el estilo más común hoy en JS). Si ven algo como
`vuelos.filter((vuelo) => ...)`, es lo mismo que escribir
`vuelos.filter(function (vuelo) { return ...; })`.

## 4. Ejemplo completo resuelto: filtrar por rango de precio

Este ejemplo resuelve un problema *distinto* al que tienen que resolver
ustedes (filtra por precio, no por destino), pero usa exactamente el mismo
patrón: recibe un array y un criterio, y devuelve un array nuevo filtrado.

```js
// Dado un array de productos y un precio máximo, devuelve solo
// los productos que cuestan ese precio o menos.
function filtrarPorPrecioMaximo(productos, precioMaximo) {
  return productos.filter((producto) => {
    return producto.precio <= precioMaximo;
  });
}

const productos = [
  { nombre: "Mate", precio: 8000 },
  { nombre: "Termo", precio: 25000 },
  { nombre: "Bombilla", precio: 3000 },
];

filtrarPorPrecioMaximo(productos, 10000);
// [{ nombre: "Mate", precio: 8000 }, { nombre: "Bombilla", precio: 3000 }]
```

El patrón que se repite y que van a necesitar en `filtrarVuelosPorDestino`
es:

```js
function miFiltro(lista, criterio) {
  return lista.filter((elemento) => {
    // acá va la condición que decide si "elemento" queda o no
    return /* true o false */;
  });
}
```

En su caso, `lista` son los vuelos, `criterio` es el texto de búsqueda, y la
condición tiene que comparar `elemento.destino` contra ese texto — pero
antes de comparar, van a tener que aplicarles a ambos `.toLowerCase()` y
sacarles las tildes.
