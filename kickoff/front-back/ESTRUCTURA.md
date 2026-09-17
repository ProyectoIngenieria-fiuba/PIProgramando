# Estructura de un proyecto Front + Back

Esta guía es para quien se suma al equipo y nunca vio la organización de
carpetas de un proyecto de desarrollo "estándar". Usamos este mismo repo
como ejemplo: la lógica de carpetas que ves acá se repite, con pequeñas
variantes, en la mayoría de los proyectos profesionales con front y back.

## La idea de fondo: separar front y back

Un **front** (lo que corre en el navegador del usuario) y un **back** (lo
que corre en un servidor) son dos programas distintos, que hablan entre sí
por HTTP (peticiones a una API). Por eso viven en carpetas separadas, cada
una con su propio `package.json` y sus propias dependencias:

- `server/` no sabe nada de React, HTML ni CSS — solo expone datos.
- `client/` no sabe nada de bases de datos ni de cómo se guardan los
  datos — solo los pide y los muestra.

Esta separación permite, por ejemplo, deployar el front y el back en
lugares distintos, o reemplazar uno sin tocar el otro, siempre que la
"forma" de la API no cambie.

## Mapa de carpetas

```
front-back/
├── package.json          # raíz: junta client+server como "workspaces" de npm,
│                          #   así "npm install" y "npm run dev" alcanzan para todo
│
├── server/                # ── BACK ──
│   ├── package.json       # dependencias propias del back (Express, etc.)
│   ├── index.js            # punto de entrada: arranca el servidor y define
│   │                        #   los endpoints (ej. GET /api/estaciones)
│   └── data/                # datos. Acá están mockeados en un array de JS;
│       └── estaciones.js    #   en un proyecto real, esto sería una base de datos
│
└── client/                # ── FRONT ──
    ├── package.json        # dependencias propias del front (React, Vite, etc.)
    ├── index.html            # HTML base donde Vite monta la app
    ├── vite.config.js        # config del bundler/dev server (puerto, proxy a la API)
    └── src/                   # código fuente de la app
        ├── main.jsx            # punto de entrada: monta <App /> en el <div id="root">
        ├── App.jsx              # componente raíz: pide los datos a la API y
        │                        #   decide qué mostrar
        ├── App.css               # estilos
        ├── components/            # piezas de UI reutilizables, cada una con
        │   ├── EstacionCard.jsx    #   una sola responsabilidad visual
        │   └── Semaforo.jsx
        └── utils/                  # lógica "de negocio" sin JSX ni estilos —
            └── stockStatus.js       #   funciones puras, fáciles de leer y testear
```

## Por qué se organiza así

- **`package.json` en la raíz + `workspaces`**: patrón de "monorepo" liviano.
  Sin esto, habría que hacer `npm install` y levantar el server y el client
  por separado, en dos terminales. Con `workspaces`, un solo `npm install` y
  un solo `npm run dev` alcanzan.
- **`index.js` / `index.html` / `main.jsx` como puntos de entrada**: es una
  convención muy extendida (no solo de este proyecto) que el archivo
  "por donde arranca todo" se llame `index` o `main`, para que cualquiera
  que abra el proyecto sepa dónde empezar a leer.
- **`components/` separado de `utils/`**: separa "cómo se ve" (JSX, HTML,
  estilos) de "cómo se decide" (lógica pura, sin interfaz). Esto hace que la
  lógica se pueda leer, testear y corregir sin tener que entender React —
  por eso el bug de esta demo vive justamente en `utils/`.
- **`data/` en el back en vez de datos hardcodeados en el endpoint**:
  aísla los datos de la lógica del servidor, para que el día de mañana
  reemplazar el mock por una base de datos real sea cambiar un solo archivo.

## Cómo se conecta todo

1. El navegador carga `client/index.html`, que ejecuta `main.jsx`.
2. `main.jsx` monta `App.jsx`, que hace un `fetch("/api/estaciones")`.
3. Vite (`vite.config.js`) redirige ese `/api/...` al server real en el
   puerto 4000.
4. `server/index.js` responde con los datos de `server/data/estaciones.js`.
5. `App.jsx` reparte esos datos entre varias `EstacionCard.jsx`, y cada una
   usa `utils/stockStatus.js` para decidir qué color de `Semaforo.jsx`
   mostrar.
