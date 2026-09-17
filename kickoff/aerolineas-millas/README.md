# Calculadora de Millas — Demo "Hola, PI"

Mini-app ficticia que calcula las millas que gana un pasajero según su
categoría (Económica, Plata, Oro, Platino) y la distancia del vuelo. Fue
vibecodeada a partir del prompt que está en [PROMPT_ORIGINAL.md](./PROMPT_ORIGINAL.md).

> Nota: esta app es una ambientación ficticia con fines educativos para el
> taller "Hola, PI" (Proyecto Ingeniería, FIUBA). No representa sistemas,
> datos ni procesos reales de Aerolíneas Argentinas ni de ninguna otra
> empresa.

## Stack

HTML/CSS/JS plano, sin backend ni dependencias (`millas.js`).

## Cómo levantar el proyecto

Alcanza con abrir `index.html` directo en el navegador. Si preferís servirlo:

```bash
npx serve .
```

## Cómo probar

Cargá el mismo vuelo (por ejemplo, 1500 km) dos veces, cambiando solo la
categoría:

1. Categoría **Económica**, 1500 km → anotá el resultado.
2. Categoría **Platino**, 1500 km → anotá el resultado.

Comparalos.

## 🐛 Algo no cierra

Un pasajero Platino debería ganar **más** millas que uno Económico en el
mismo vuelo, no menos. Compará los dos resultados del punto anterior.

No se documenta acá la causa a propósito — la idea es que quien facilite la
demo pueda:

1. Reproducir el caso con los dos cálculos de arriba.
2. Inspeccionar `millas.js` (es corto, una sola función) para encontrar por
   qué las categorías más altas dan menos millas.
3. Corregirlo en vivo.

Pista de dónde mirar (sin más detalle): la función de cálculo está en un
único archivo, `millas.js`, y el problema tiene que ver con cómo se relaciona
cada categoría con su multiplicador.
