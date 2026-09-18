# Guía para trabajar con IA en esta posta

Esta actividad se resuelve combinando código propio y ayuda de un chatbot de
IA (Claude, ChatGPT, Gemini, lo que tengan a mano). No es "pedirle a la IA
que lo haga todo": es escribir un buen pedido, leer lo que devuelve, probarlo,
y si algo no anda, iterar con información concreta.

## 1. Cómo armar un buen prompt

Un prompt vago da un resultado vago. Cuanto más contexto le den, mejor va a
ser lo que devuelva a la primera. Para esta función en particular, traten de
incluir:

- **Qué recibe la función y qué tiene que devolver.** Nombre exacto de la
  función (`filtrarVuelosPorDestino`), sus parámetros (`vuelos`,
  `textoBusqueda`) y qué tiene que devolver (un array nuevo, filtrado).
- **La forma de los datos.** Pegale un ejemplo de un objeto vuelo, así sabe
  contra qué campo comparar (`destino`).
- **Los casos borde, explícitos.** No alcanza con decir "que filtre por
  destino". Hay que aclarar:
  - que tiene que ser coincidencia parcial (no exacta),
  - que no debe importar mayúsculas/minúsculas,
  - que no debe importar los tildes,
  - qué tiene que pasar si no hay resultados.

### Ejemplo de prompt flojo

> "Hacé una función que filtre vuelos por destino."

Con esto la IA tiene que adivinar todo lo demás, y es fácil que se olvide de
tildes o mayúsculas — exactamente los casos que van a testear en el
checklist.

### Ejemplo de prompt mejor armado

> Tengo esta función en JavaScript, que por ahora no hace nada:
>
> ```js
> function filtrarVuelosPorDestino(vuelos, textoBusqueda) {
>   return vuelos;
> }
> ```
>
> `vuelos` es un array de objetos con esta forma:
> `{ destino: "Bariloche", fecha: "2026-10-05", precio: 45000, duracion: "2h10" }`
>
> Necesito que devuelva un array nuevo con los vuelos cuyo `destino` coincida
> con `textoBusqueda`, cumpliendo:
> - Coincidencia parcial (buscar "bari" debe encontrar "Bariloche").
> - Que no importen mayúsculas ni minúsculas.
> - Que no importen los tildes (buscar "cordoba" debe encontrar "Córdoba").
> - Si `textoBusqueda` está vacío, debe devolver todos los vuelos.
>
> No quiero que modifique el array original.

Noten que ninguno de los dos prompts "da la solución": el segundo simplemente
no deja ambigüedad sobre los requisitos.

## 2. Cómo leer el código que te devuelve la IA (mini code review)

Antes de pegar el código en `app.js` y asumir que ya está, revisen:

- **¿Hace *solo* lo que pediste?** Si le pediste el filtro por destino y
  también reordenó la lista o cambió otra función que no le pediste tocar,
  pregunten por qué o pídanle que devuelva solo lo necesario.
- **¿Los nombres de variables tienen sentido?** Si ven algo como
  `const a = vuelos.filter(x => ...)`, está bien pedirle que use nombres más
  claros (`vuelo`, `destinoNormalizado`, etc.) — no hace falta convivir con
  código que no se entiende.
- **¿Hay algo que no entendés?** Si aparece algo como `.normalize("NFD")` y
  no tienen ni idea de qué hace (está explicado en
  [`TEORIA.md`](./TEORIA.md), pero igual pueden preguntarle a la IA
  directamente): "¿Qué hace esta línea?, explicámela como si nunca hubiera
  visto `.normalize()`". Entender el código que van a entregar es parte de
  la consigna, no un extra.
- **Pruébenlo con el checklist de [`CONSIGNA.md`](./CONSIGNA.md) antes de
  darlo por terminado.** Que "compile" o no tire error no significa que esté
  bien.

## 3. Qué hacer cuando algo no anda

Cuando un caso del checklist falla, el prompt que más ayuda no es "arreglalo"
ni "no funciona" — es describir el síntoma con datos concretos: qué
escribieron, qué esperaban ver, y qué vieron en realidad.

### Prompt flojo cuando algo falla

> "No funciona, arreglalo."

La IA no tiene forma de saber qué probaste ni qué esperabas, así que va a
tener que adivinar o reescribir todo de cero (y a veces rompe algo que sí
andaba).

### Prompt mejor armado cuando algo falla

> Busco "bari" en el buscador y no aparece ningún vuelo, pero debería
> aparecer "Bariloche" (coincidencia parcial). Esta es la función actual:
>
> ```js
> [pegar la función tal cual está ahora]
> ```
>
> ¿Por qué no está encontrando la coincidencia parcial?

Con esto la IA puede razonar sobre el código real y el caso real, en vez de
reinventar la función desde cero. Además, así van entendiendo ustedes mismos
dónde estaba el problema — no solo confiando en que "ahora sí anda".

**Regla general:** antes de pedir un cambio, prueben poder completar esta
frase: *"Escribí ___, esperaba ver ___, pero vi ___."* Si pueden llenarla,
ya tienen un prompt de arreglo mucho mejor que "no anda".
