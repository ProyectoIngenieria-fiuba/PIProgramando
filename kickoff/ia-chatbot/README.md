# Chatbot de Soporte ARSAT — Demo "Hola, PI"

Chatbot de soporte técnico ficticio para consultas de conectividad (internet
satelital), que responde usando un LLM (Gemini) vía API.

> Nota: esta app es una ambientación ficticia con fines educativos para el
> taller "Hola, PI" (Proyecto Ingeniería, FIUBA). No representa sistemas,
> datos ni procesos reales de ARSAT ni de ninguna otra empresa.

## Stack

- **Front:** HTML/CSS/JS plano (`public/`)
- **Back:** Node + Express (`server/`), llama a la API de Gemini

## Cómo levantar el proyecto

Requiere Node 18+ y una API key de Gemini (gratis, sin tarjeta): entrá a
[Google AI Studio](https://aistudio.google.com/apikey) con una cuenta de
Google y generá una key en un par de clicks.

```bash
npm install
cp .env.example .env
```

Completá `.env` con tu API key:

```
GEMINI_API_KEY=AIza...
```

Y arrancá el servidor:

```bash
npm run dev
```

La app queda disponible en `http://localhost:3001`.

## Estructura

```
ia-chatbot/
├── server/
│   ├── index.js          # Express, sirve el front y expone POST /api/chat
│   └── systemPrompt.js   # instrucciones del asistente
├── knowledge/
│   └── base-conocimiento.md   # datos reales de planes y políticas de soporte
└── public/                # chat (HTML/CSS/JS)
```

## Cómo probar

Probá estas preguntas en el chat:

1. "¿Cuánto cuesta el plan Premium Fibra 500MB?"
2. "Si cancelo antes de los 30 días, ¿me reembolsan lo que pagué?"
3. "¿Tienen algún plan con velocidad simétrica para streaming profesional?"

## 🐛 Algo no cierra

El chatbot responde estas preguntas con total seguridad, dando precios,
condiciones y detalles concretos. El problema es que **ninguno de esos datos
existe** — podés comparar la respuesta contra `knowledge/base-conocimiento.md`,
que es la única fuente real de planes y políticas de soporte.

No se documenta acá la causa a propósito — la idea es que quien facilite la
demo pueda:

1. Reproducir el caso haciendo las preguntas de arriba.
2. Comparar la respuesta del bot contra `knowledge/base-conocimiento.md`.
3. Inspeccionar el código del back para encontrar por qué el bot no está
   usando esa información.

Pista de dónde mirar (sin más detalle): el problema está en cómo se arma el
pedido a la API en `server/`, no en el archivo de conocimiento en sí.
