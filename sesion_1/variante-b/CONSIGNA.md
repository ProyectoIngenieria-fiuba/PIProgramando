# Consigna — Sesión 1 · Variante B: Próximos Lanzamientos

> ¿Primera vez con HTML/CSS/JS, o hace mucho que no tocás nada de esto?
> Antes de arrancar, date una vuelta por
> [INTRODUCCION FRONT BACK.pdf](../INTRODUCCION%20FRONT%20BACK.pdf), acá al
> lado en `sesion_1/` (15-20 minutos con lo básico que vas a necesitar acá),
> y de paso probá [introduccion-practica/](../introduccion-practica/) para
> verlo funcionando en un proyecto de verdad.

## Objetivo del día

Trabajar en equipo (4-6 personas, virtual, con IA) sobre un proyecto ya
armado que tiene varios problemas repartidos en distintos archivos y
páginas. El objetivo no es escribir código desde cero, sino **leer un
proyecto que ya existe, entender cómo están conectadas sus partes, y
encontrar por qué se comporta mal**, arreglándolo con ayuda de una IA que
revisen antes de aceptar.

Esta vez el proyecto tiene varias páginas HTML, varios archivos CSS y varios
archivos JS que se llaman entre sí. **No alcanza con mirar un solo archivo**
para entender ni para arreglar cada problema.

Después de resolver los bugs, si les queda tiempo, hay 4 extras opcionales
para seguir practicando sobre el mismo proyecto.

## El escenario

Este es un panel de seguimiento de lanzamientos satelitales, ambientado en
CONAE (Comisión Nacional de Actividades Espaciales), pero **completamente
ficticio** — sin ninguna relación con sistemas, datos o procesos reales de
la institución.

El panel muestra un **countdown en vivo** para el lanzamiento más próximo
(días, horas, minutos y segundos restantes), que debería detenerse y pasar
al estado **"¡Lanzado! 🚀"** cuando llega a cero.

## Cómo abrir el proyecto

No hace falta instalar nada ni levantar un servidor:

- **Opción 1**: doble click en `index.html` (o abrirlo desde el navegador
  con `Ctrl+O`). Ahí arranca la página de inicio del sitio; desde el menú de
  arriba se navega a "Lanzamientos", "Nosotros" y "Lanzamientos pasados".
- **Opción 2**: si prefieren editar en el navegador, suban toda la carpeta
  del proyecto a [CodeSandbox](https://codesandbox.io) o
  [StackBlitz](https://stackblitz.com) — ambos permiten forkear/crear sin
  necesidad de loguearse.

> Nota: las fechas de los lanzamientos se calculan en relación al momento
> en que se abre la página (no son fechas fijas de calendario), así que el
> lanzamiento más próximo ("Ceibo-1") va a estar a menos de dos minutos de
> distancia apenas entren a "Lanzamientos" — no hace falta esperar horas
> para ver los problemas.

## Mapa del proyecto

```
index.html              → Inicio (landing del sitio, sin bugs)
acerca.html             → Nosotros (info del proyecto, sin lógica)
lanzamientos.html       → Panel de lanzamientos: countdown + lista
lanzamiento.html        → Detalle de un lanzamiento (se llega con "Ver detalle")
pasados.html            → Lanzamientos pasados

css/variables.css       → colores y tema
css/base.css            → reset y tipografía
css/layout.css          → navbar, footer, headers de página
css/componentes.css     → hero, countdown, tarjetas, listas, etc.

js/datos.js             → los lanzamientos y su información
js/logica.js            → cómo se calcula y formatea el countdown
js/tema.js              → tema claro/oscuro (compartido en todas las páginas)
js/ui-lanzamientos.js   → arma lo que se ve en lanzamientos.html
js/ui-lanzamiento.js    → arma lo que se ve en lanzamiento.html
js/ui-pasados.js        → arma lo que se ve en pasados.html
```

Los archivos `.js` se cargan con `<script src="...">` normales (no son
módulos), en un orden específico dentro de cada HTML — ese orden importa,
préstenle atención.

## El problema

Hay más de un problema para encontrar, y no están todos en el mismo lugar.
"Inicio" y "Nosotros" no tienen ninguna lógica rota — no hace falta
tocarlas.

### 1. En el panel de lanzamientos (`lanzamientos.html`)

Dejen la página abierta y observen el countdown del lanzamiento más
próximo (Ceibo-1) hasta que llegue a cero. **Algo no cierra**: en vez de
detenerse y mostrar "¡Lanzado! 🚀", el countdown sigue corriendo **en
negativo** indefinidamente (algo como `-0d 00h 00m 15s`, cada vez más
negativo).

Además, miren el número de **"Lanzamientos programados"** en el resumen de
arriba. ¿Coincide con la cantidad de lanzamientos que ven en la lista de
abajo?

### 2. En el detalle de un lanzamiento (`lanzamiento.html`)

Desde la lista de "Lanzamientos", clickeen "Ver detalle →" en un
lanzamiento que **no** sea el más próximo (por ejemplo, "Copihue Austral").
Comparen la fecha programada que se muestra contra el countdown de esa
misma página. ¿Tiene sentido ese countdown para esa fecha?

> Aclaración: no hay que tocar las fechas de los lanzamientos, cómo se
> calculan (`dentroDe`), ni el formato de días/horas/minutos/segundos que
> se muestra en pantalla — eso está bien. Los problemas están en otro lado.

**No son bugs que se noten "a simple vista" leyendo una sola línea.** Van a
requerir rastrear de dónde sale exactamente cada valor, y en algún caso
comparar dos archivos JS distintos que se cargan en la misma página.

## Checklist para validar que lo resolvieron

En el panel de lanzamientos (`lanzamientos.html`):

- [ ] El countdown de Ceibo-1 llega a cero y se **detiene** (deja de
      actualizarse), mostrando **"¡Lanzado! 🚀"**.
- [ ] El countdown **no queda mostrando números negativos** en ningún
      momento, ni siquiera un instante.
- [ ] **"Lanzamientos programados"** muestra **5**, no otro número.
- [ ] Los demás lanzamientos de la lista siguen mostrándose sin cambios.

En el detalle de un lanzamiento (`lanzamiento.html`):

- [ ] Al entrar al detalle de **cada uno** de los 5 lanzamientos, el
      countdown que se muestra corresponde a la fecha programada de **esa**
      misión, no a la del lanzamiento más próximo en general.

## Extras (opcionales, en este orden)

Encaren estos extras en orden — cada uno se apoya un poco en el anterior.
No hace falta llegar al final para que la actividad haya servido.

1. **Lanzamiento nuevo**: agregar un lanzamiento más a la lista, con su
   propia fecha, que aparezca correctamente en el panel y en su propia
   página de detalle.
2. **Lanzamiento favorito**: dejar que el usuario marque un lanzamiento
   como favorito (por ejemplo con una estrella), guardando ese estado en
   `localStorage` para que sobreviva a un refresh de la página.
3. **Panel de lanzamientos pasados**: cuando el countdown de un lanzamiento
   llega a cero, que se mueva automáticamente de "próximos" a la lista de
   `pasados.html` (van a necesitar guardar ese cambio en `localStorage`
   para que sobreviva a la navegación entre páginas).
4. **Filtro/orden de la lista**: poder ordenar o filtrar los lanzamientos
   por fecha o por estado (próximo/pasado).
