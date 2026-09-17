import express from "express";
import cors from "cors";
import { estaciones } from "./data/estaciones.js";

const app = express();
const PORT = 4000;

app.use(cors());

app.get("/api/estaciones", (req, res) => {
  res.json(estaciones);
});

app.listen(PORT, () => {
  console.log(`API escuchando en http://localhost:${PORT}`);
});
