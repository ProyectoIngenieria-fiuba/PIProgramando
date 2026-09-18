# Consigna — Buscador de Vuelos

> Esta app es una ambientación ficticia con fines educativos para el taller
> PIP (Proyecto Ingeniería, FIUBA). No representa sistemas, datos ni
> procesos reales de Aerolíneas Argentinas ni de ninguna otra empresa.

## El objetivo

Tienen una mini-app de búsqueda de vuelos ya armada: la lista de vuelos está
cargada, el input de búsqueda está en pantalla y conectado, y la página
renderiza. Lo único que falta es la función que hace el filtrado.

Esa función se llama `filtrarVuelosPorDestino` y está en
[`app.js`](./app.js), marcada con un comentario `TODO`. Ahora mismo devuelve
todos los vuelos sin filtrar — por eso, si abren la app, van a ver la lista
completa sin importar lo que escriban en el buscador. Su trabajo es
completarla, ayudándose de un chatbot de IA (Claude, ChatGPT, Gemini, el que
tengan a mano) y de [`TEORIA.md`](./TEORIA.md).

Antes de escribir el primer prompt, lean [`GUIA_IA.md`](./GUIA_IA.md): tiene
tips concretos para pedirle bien las cosas a la IA y para revisar lo que les
devuelva.

## Básico (tiene que cumplirse sí o sí)

La función recibe la lista completa de vuelos y el texto que escribió el
usuario, y tiene que devolver solo los vuelos que correspondan. Concretamente:

1. **Coincidencia parcial.** No hace falta escribir el destino completo:
   escribir `"bari"` tiene que mostrar los vuelos a Bariloche.
2. **Insensible a mayúsculas/minúsculas.** Da lo mismo escribir `"salta"`,
   `"Salta"` o `"SALTA"`.
3. **Insensible a tildes.** Escribir `"cordoba"` (sin tilde) tiene que
   encontrar los vuelos a **Córdoba**.
4. **Sin resultados = mensaje, no lista vacía.** Si ninguna búsqueda
   coincide, tiene que verse un mensaje claro (por ejemplo "No se
   encontraron vuelos..."), nunca una lista en blanco sin explicación. Ese
   mensaje ya está resuelto en el `render` — si el filtro devuelve un array
   vacío, el mensaje aparece solo.

## Checklist de casos de prueba

Prueben estos casos en el buscador y confirmen que el resultado sea el
esperado. Si alguno falla, ese es el próximo bug a resolver.

| # | Escriben en el buscador | Resultado esperado |
|---|--------------------------|---------------------|
| 1 | `bari` | 2 vuelos a Bariloche |
| 2 | `BARILOCHE` | los mismos 2 vuelos a Bariloche |
| 3 | `cordoba` (sin tilde) | 2 vuelos a Córdoba |
| 4 | `Córdoba` (con tilde) | los mismos 2 vuelos a Córdoba |
| 5 | `mendoza` | 2 vuelos a Mendoza |
| 6 | `xyz` (algo que no existe) | mensaje de "no se encontraron vuelos", no una lista vacía |
| 7 | dejar el buscador vacío | los 15 vuelos completos |

Si los 7 casos andan, el básico está listo.

## Extras (opcionales, en orden de dificultad creciente)

Para las escuadras que terminen el básico con tiempo de sobra. No hace falta
hacerlos todos ni en orden — elijan por dónde seguir.

1. **Filtro combinado por destino y rango de fechas.** Agregar dos inputs de
   fecha ("desde" / "hasta") y que la búsqueda combine destino + fecha.
2. **Ordenar resultados.** Agregar un selector para ordenar la lista
   filtrada por precio (menor a mayor) o por duración.
3. **Múltiples destinos a la vez.** Si escriben `"bariloche, salta"`
   (separados por coma), mostrar los vuelos que coincidan con cualquiera de
   los dos.
4. **Resumen de resultados.** Mostrar arriba de la lista un texto tipo
   "Se encontraron 2 vuelos a bari".

## Cómo correr el proyecto

**Opción A — Sandbox (recomendada para el taller):**
Abran esta carpeta en CodeSandbox o StackBlitz importando el repo de GitHub
del taller. No hace falta instalar nada: es HTML/CSS/JS plano.

**Opción B — Local:**

```bash
git clone https://github.com/ProyectoIngenieria-fiuba/PIProgramando.git
cd PIProgramando/kickoff/buscador-vuelos
```

Y después abran `index.html` directo en el navegador (doble click, o
"Open with Live Server" si usan VS Code). También sirve:

```bash
npx serve .
```

No hay instalación de dependencias ni servidor backend: todo corre en el
navegador.
