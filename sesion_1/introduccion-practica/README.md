# Proyecto de práctica — Lista de tareas

Este proyecto **no forma parte de ningún ejercicio del taller** (no es la
variante A ni la B de ninguna sesión, y no tiene ningún bug escondido). Es
un acompañamiento para `INTRODUCCION_FRONT_BACK.pdf`: el mismo ejemplo de
"lista de tareas" que aparece ahí, pero corriendo de verdad, para que lo
abras, lo toques y veas en vivo lo que describe el documento.

## Cómo abrirlo

Doble click en `index.html` (o abrilo desde el navegador con `Ctrl+O`). No
hace falta instalar nada.

## Qué hace

- Agregar una tarea nueva (input + botón "Agregar").
- Marcar una tarea como hecha clickeando su texto (se tacha).
- Borrar una tarea (botón ✕).
- Un contador de "X de Y completadas" que se actualiza solo.

## Cómo está armado

- `index.html` — la estructura: el formulario para agregar tareas y el
  contenedor donde se pintan.
- `style.css` — el estilo visual.
- `script.js` — toda la lógica, con comentarios de más a propósito para que
  lo puedas leer en paralelo con el PDF de introducción.

## Cosas para probar

No hace falta que sepas programar para intentar esto — es justamente para
perderle el miedo a tocar código y ver qué pasa. Abrí `script.js` en un
editor de texto (o incluso en el Bloc de notas) y probá:

1. **Cambiar un texto**: cambiá el `texto` de alguna de las tareas
   iniciales (arriba del todo, en el array `tareas`) y volvé a abrir
   `index.html` en el navegador — ¿aparece el cambio?
2. **Agregar una cuarta tarea inicial**: copiá una de las líneas del array
   `tareas` y agregale una más, con otro `id`. ¿Aparece en la lista?
3. **Cambiar el color de las tareas completadas**: en `style.css`, buscá
   `.tarea--hecha .tarea__texto` y cambiá el `color`.
4. **Romper algo a propósito**: borrá la línea `contenedor.innerHTML = "";`
   dentro de `renderTareas()` en `script.js`, guardá, y volvé a abrir la
   página. Agregá un par de tareas — ¿qué pasa? Abrí la consola del
   navegador (`F12` o clic derecho → "Inspeccionar" → pestaña "Console")
   para ver si hay algún error. Después deshacé el cambio.
5. **Agregar un botón "Vaciar todo"**: pensá cómo lo harías usando lo que
   ya está en el archivo (`tareas = []` y volver a llamar a
   `renderTareas()`). Si te trabás, pedile ayuda a una IA — pero primero
   intentalo vos.

Ninguna de estas es obligatoria ni se corrige en ningún lado. Es para
agarrar confianza antes de la sesión.
