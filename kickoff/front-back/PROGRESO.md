# Progreso — Demo PIP (Panel de Estaciones de Servicio)

Resumen de lo armado hasta ahora en `taller-pip/kickoff/front-back/`.

## Qué se construyó

App full-stack para una demo en vivo de 15 minutos:

- **Back** (`server/`): API Express en `:4000`, un único endpoint
  `GET /api/estaciones` que devuelve 12 estaciones de servicio ficticias
  (nombre, provincia, combustible, `stockPorcentaje`) desde
  `server/data/estaciones.js` (datos en memoria, sin base de datos).
- **Front** (`client/`): React + Vite en `:5173`, con proxy a la API.
  Muestra las estaciones en tarjetas (`EstacionCard.jsx`) con un semáforo
  visual (`Semaforo.jsx`) según el estado de stock.
- **Monorepo simple**: `package.json` raíz con `npm workspaces`, así
  `npm install && npm run dev` levanta back y front juntos (via
  `concurrently`).

## El bug intencional

En `client/src/utils/stockStatus.js`, la función `getStockStatus` tiene un
caso por defecto mal puesto: cuando el stock es crítico (<20%), devuelve
`"verde"` en vez de `"rojo"`. Efecto: ninguna estación puede mostrar rojo
nunca (ej. "Estación Río Grande" con 5% de stock aparece en verde, "Stock
OK"). Es un bug de una sola línea, en un archivo chico y aislado, pensado
para que un facilitador con conocimientos medios de React/JS lo encuentre y
corrija en 8-10 minutos en vivo.

## Documentación agregada

- **README.md**: cómo levantar el proyecto (`npm install && npm run dev`),
  stack, estructura de carpetas, y descripción del bug **sin** revelar la
  causa ni la solución.
- **SOLUCION.md** (gitignored, uso exclusivo del facilitador): causa raíz
  exacta, código del fix esperado, y pistas sugeridas para guiar la
  búsqueda sin spoilear de entrada.
- **ESTRUCTURA.md**: guía de onboarding para quien se suma al kickoff,
  explicando la organización estándar de un proyecto front+back (por qué
  se separan `client/`/`server/`, para qué sirven `components/` vs
  `utils/`, convención de puntos de entrada, etc.), usando este mismo repo
  como ejemplo.

## Verificación hecha

- `npm install` corrido con éxito (workspaces `server` + `client`).
- `npm run dev` levanta ambos procesos sin errores.
- Probado con navegador headless: la app carga sin errores de consola, y
  se confirmó en el DOM que "Estación Río Grande" (5% de stock) efectivamente
  muestra el semáforo en verde — el bug se reproduce como se esperaba.

## Pendiente / a decidir

- Todavía no se hizo commit de nada de esto al repo (`taller-pip/` está sin
  trackear en git según el último estado revisado).
- No se validó todavía con un "facilitador de prueba" que el bug sea
  encontrable en 8-10 minutos reales (solo se verificó que es reproducible
  y que el fix es correcto).
