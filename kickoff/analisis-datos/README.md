# Rendimiento de Cultivos por Provincia — Demo "Hola, PI"

Análisis de un dataset de rendimiento de soja y maíz por provincia y campaña
agrícola, ambientado en el mundo del agro argentino.

> Nota: este dataset es una ambientación ficticia con fines educativos para
> el taller "Hola, PI" (Proyecto Ingeniería, FIUBA). No representa datos
> reales del INTA ni de ningún organismo.

## Objetivo del análisis

Calcular el **rendimiento promedio de cultivos por provincia**, a partir de
un dataset que viene de una carga real y trae algunos problemas de calidad
de datos típicos de este tipo de fuentes.

## Cómo levantar el proyecto

Requiere Python 3.10+.

```bash
pip install -r requirements.txt
jupyter notebook analisis_ingenuo.ipynb
```

## Estructura

```
analisis-datos/
├── data/
│   └── rendimiento_cultivos.csv   # dataset
└── analisis_ingenuo.ipynb          # primer análisis
```

## 🐛 Algo no cierra

El notebook `analisis_ingenuo.ipynb` hace un primer cálculo del rendimiento
promedio por provincia y arroja un resultado que no tiene ningún sentido
agronómico: una provincia aparece con un promedio varios órdenes de magnitud
por encima de las demás, y además hay más "provincias" en la tabla de las
8 que debería haber.

No se documenta acá la causa a propósito — la idea es que quien facilite la
demo pueda:

1. Correr el notebook y ver el resultado erróneo.
2. Inspeccionar el CSV (`value_counts()`, `describe()`, `isna().sum()`,
   mirar filas puntuales) para encontrar qué está mal.
3. Corregirlo en vivo y volver a calcular el promedio.

Pistas de dónde mirar (sin más detalle): hay más de un problema, y no son
solo numéricos — conviene mirar también los valores de texto de alguna
columna.
