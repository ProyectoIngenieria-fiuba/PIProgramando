# Panel de Estaciones de Servicio — Demo "Hola, PI"

Panel interno ficticio para gestionar el stock de combustible de una red de
estaciones de servicio. Cada estación se muestra con un semáforo de estado:

- 🟢 Verde: stock OK
- 🟡 Amarillo: stock bajo
- 🔴 Rojo: stock crítico

> Nota: esta app es una ambientación ficticia con fines educativos para el
> taller "Hola, PI" (Proyecto Ingeniería, FIUBA). No representa sistemas,
> datos ni procesos reales de ninguna empresa.

## Stack

- **Front:** React + Vite (`client/`)
- **Back:** Node + Express, datos mockeados en memoria (`server/`)

## Cómo levantar el proyecto

Requiere Node 18+.

```bash
npm install
npm run dev
```

Esto instala las dependencias de `server/` y `client/` (vía npm workspaces) y
levanta ambos procesos en paralelo:

- API en `http://localhost:4000`
- Front en `http://localhost:5173`

El front consume la API a través de un proxy configurado en Vite
(`/api` → `http://localhost:4000`), así que no hace falta configurar nada
extra.

## Estructura

```
front-back/
├── server/        # API Express — GET /api/estaciones
└── client/        # React + Vite — panel visual
    └── src/
        ├── components/   # EstacionCard, Semaforo
        └── utils/        # lógica de estado del semáforo
```

Si es la primera vez que ves la organización de carpetas de un proyecto
front+back, en [ESTRUCTURA.md](./ESTRUCTURA.md) está explicado qué hay en
cada carpeta y por qué, a modo de pantallazo general de cómo se arma un
proyecto de desarrollo estándar.

## 🐛 Bug conocido

Hay un bug intencional en la lógica que decide el color del semáforo según
el porcentaje de stock. En algunos casos, una estación con stock **crítico**
aparece en el panel como si estuviera **todo bien (verde)**.

No se documenta acá la causa ni la solución a propósito — la idea es que
quien facilite la demo pueda:

1. Reproducir el caso en la app corriendo.
2. Inspeccionar el código relevante (front) para encontrar dónde se decide
   el color del semáforo.
3. Identificar la causa y corregirla en vivo.

Pista de dónde mirar (sin más detalle): la decisión de color vive en un
único archivo, chico, dentro de `client/src/utils/`.
