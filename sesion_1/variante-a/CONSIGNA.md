# Consigna — Sesión 1 · Variante A: Panel de Monitoreo del Reactor

> ¿Primera vez con HTML/CSS/JS, o hace mucho que no tocás nada de esto?
> Antes de arrancar, date una vuelta por
> [INTRODUCCION FRONT BACK.pdf](../INTRODUCCION%20FRONT%20BACK.pdf), acá al
> lado en `sesion_1/` (15-20 minutos con lo básico que vas a necesitar acá),
> y de paso probá [introduccion-practica/](../introduccion-practica/) para
> verlo funcionando en un proyecto de verdad.

## Objetivo del día

Trabajar en equipo (4-6 personas, virtual, con IA) sobre un proyecto ya armado
que tiene varios problemas repartidos en distintos archivos y páginas. El
objetivo no es escribir código desde cero, sino **leer un proyecto que ya
existe, entender cómo están conectadas sus partes, y encontrar por qué se
comporta mal**, arreglándolo con ayuda de una IA que revisen antes de
aceptar.

Esta vez el proyecto tiene varias páginas HTML, varios archivos CSS y varios
archivos JS que se llaman entre sí. **No alcanza con mirar un solo archivo**
para entender ni para arreglar cada problema.

Después de resolver los bugs, si les queda tiempo, hay 4 extras opcionales
para seguir practicando sobre el mismo proyecto.

## El escenario

Este es el panel de monitoreo de un reactor de investigación **ficticio**,
ambientado en INVAP (empresa nacional de tecnología argentina), pero sin
ninguna relación con sistemas, datos o procesos reales de la empresa.

El panel muestra tres sensores, cada uno con un semáforo de estado:

- 🟢 **Verde**: valor dentro del rango normal.
- 🟡 **Amarillo**: valor en una zona intermedia, para vigilar.
- 🔴 **Rojo**: valor fuera del rango seguro, requiere atención.

## Cómo abrir el proyecto

No hace falta instalar nada ni levantar un servidor:

- **Opción 1**: doble click en `index.html` (o abrirlo desde el navegador
  con `Ctrl+O`). Ahí arranca la página de inicio del sitio; desde el menú de
  arriba se navega a "Panel de sensores", "Nosotros" e "Historial de
  alertas".
- **Opción 2**: si prefieren editar en el navegador, suban toda la carpeta
  del proyecto a [CodeSandbox](https://codesandbox.io) o
  [StackBlitz](https://stackblitz.com) — ambos permiten forkear/crear sin
  necesidad de loguearse.

## Mapa del proyecto

```
index.html            → Inicio (landing del sitio, sin bugs)
acerca.html           → Nosotros (info del proyecto, sin lógica)
panel.html            → Panel de sensores (resumen + tarjetas)
sensor.html           → Detalle de un sensor (se llega clickeando "Ver detalle")
historial.html        → Historial de alertas

css/variables.css     → colores y tema
css/base.css          → reset y tipografía
css/layout.css        → navbar, footer, headers de página
css/componentes.css   → hero, tarjetas, resumen, gauge, etc.

js/datos.js           → los sensores y su información
js/logica.js          → cómo se calcula el estado (verde/amarillo/rojo)
js/tema.js            → tema claro/oscuro (compartido en todas las páginas)
js/ui-panel.js        → arma lo que se ve en panel.html
js/ui-sensor.js       → arma lo que se ve en sensor.html
js/ui-historial.js    → arma lo que se ve en historial.html
```

Los archivos `.js` se cargan con `<script src="...">` normales (no son
módulos), en un orden específico dentro de cada HTML — ese orden importa,
préstenle atención.

## El problema

Hay más de un problema para encontrar, y no están todos en el mismo lugar.

### 1. En el panel de sensores (`panel.html`)

Comparen lo que muestra cada tarjeta con los datos reales del sensor (el
valor y su unidad están en la misma tarjeta). Presten atención en particular
a las tarjetas de **Presión circuito primario** y **Temperatura del
núcleo**: una se ve más grave de lo que es, y la otra más tranquila de lo
que debería.

Además, miren el número de **"Sensores monitoreados"** en el resumen de
arriba. ¿Coincide con la cantidad de tarjetas que están viendo?

### 2. En el detalle de un sensor (`sensor.html`)

Desde cualquier tarjeta del panel, clickeen "Ver detalle →". Comparen el
sensor que aparece en la página de detalle contra la tarjeta desde la que
vinieron. ¿Es el mismo?

> Aclaración: no hay que tocar los valores de los sensores
> (`valorActual`, `verdeMin`, `verdeMax`, `rojoMin`, `rojoMax`) ni la
> función que calcula el estado (`calcularEstado`) — esa lógica es
> correcta tal cual está. Los problemas están en otro lado.

**No son bugs que se noten "a simple vista" leyendo una sola función.** Van
a requerir rastrear cómo viajan los datos entre archivos, y en algún caso
entre dos archivos JS distintos que se cargan en la misma página.

## Checklist para validar que lo resolvieron

En el panel de sensores (`panel.html`):

- [ ] **Presión circuito primario** (151 bar) se muestra en **verde**.
- [ ] **Temperatura del núcleo** (387 °C) se muestra en **rojo**.
- [ ] **Nivel de radiación** (0.6 mSv/h) se sigue mostrando en **verde**.
- [ ] **"Sensores monitoreados"** muestra **3**, no otro número.
- [ ] Prueba extra: cambien el `valorActual` de un sensor en `js/datos.js`
      (por ejemplo, bajen la temperatura del núcleo a 280) y confirmen que
      el color que cambia es el de **ese sensor**, no el de otro.

En el detalle de sensor (`sensor.html`):

- [ ] Al clickear "Ver detalle →" desde **cada una** de las 3 tarjetas, la
      página de detalle muestra el sensor correcto (mismo nombre, mismo
      valor que la tarjeta de origen).

## Extras (opcionales, en este orden)

Encaren estos extras en orden — cada uno se apoya un poco en el anterior.
No hace falta llegar al final para que la actividad haya servido.

1. **Sensor nuevo**: agregar un sensor de "Nivel de refrigerante" (unidad:
   `%`), con su propia configuración de rangos en `js/datos.js`, que
   aparezca correctamente tanto en el panel como en su propia página de
   detalle.
2. **Simulación en vivo**: un botón "Simular lecturas" que, con
   `setInterval`, vaya cambiando los valores de los sensores cada pocos
   segundos, para ver el panel reaccionar solo.
3. **Historial de alertas**: cada vez que un sensor entre en estado
   crítico (rojo), guardar un registro en `localStorage` (para que
   sobreviva a la navegación entre páginas) y mostrarlo en
   `historial.html`.
4. **Filtro de estado**: un selector o checkbox en el panel para mostrar
   solo los sensores que están en alerta (ocultando los que están en
   verde).
