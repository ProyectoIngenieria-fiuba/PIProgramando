require('dotenv').config();
const path = require('path');
const fs = require('fs');
const express = require('express');
const { GoogleGenAI } = require('@google/genai');
const { SYSTEM_PROMPT } = require('./systemPrompt');

const knowledgeBase = fs.readFileSync(
  path.join(__dirname, '../knowledge/base-conocimiento.md'),
  'utf-8'
);

const ai = new GoogleGenAI({});
const MODEL_ID = process.env.GEMINI_MODEL || 'gemini-2.5-flash';

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

app.post('/api/chat', async (req, res) => {
  const { message, history = [] } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Falta el mensaje' });
  }

  try {
    const response = await ai.models.generateContent({
      model: MODEL_ID,
      contents: [...history, { role: 'user', parts: [{ text: message }] }],
      config: {
        systemInstruction: SYSTEM_PROMPT,
        thinkingConfig: { thinkingBudget: 0 },
      },
    });

    res.json({ reply: response.text });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error al consultar el asistente' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Chatbot de soporte ARSAT corriendo en http://localhost:${PORT}`);
});
