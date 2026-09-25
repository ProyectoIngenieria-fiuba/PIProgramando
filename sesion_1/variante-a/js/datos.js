// ---------- Datos de los sensores ----------

const sensores = [
  {
    id: "presion-primario",
    nombre: "Presión circuito primario",
    unidad: "bar",
    valorActual: 151,
    verdeMin: 140, verdeMax: 160,
    rojoMin: 120, rojoMax: 180
  },
  {
    id: "temp-nucleo",
    nombre: "Temperatura del núcleo",
    unidad: "°C",
    valorActual: 387,
    verdeMin: 250, verdeMax: 320,
    rojoMin: 200, rojoMax: 340
  },
  {
    id: "rad-nivel",
    nombre: "Nivel de radiación",
    unidad: "mSv/h",
    valorActual: 0.6,
    verdeMin: 0, verdeMax: 1.0,
    rojoMin: 0, rojoMax: 1.4
  },
];

// Descripciones e íconos fijos por sensor (no forman parte de la config de rangos).
const descripciones = {
  "presion-primario": "Mide la presión del circuito primario de refrigeración del reactor.",
  "temp-nucleo": "Mide la temperatura del núcleo del reactor.",
  "rad-nivel": "Mide el nivel de radiación ambiental en la sala de control.",
};

const iconos = {
  "presion-primario": "🧭",
  "temp-nucleo": "🌡️",
  "rad-nivel": "☢️",
};

// Cantidad total de sensores monitoreados, para mostrarla en el resumen del panel.
var totalSensores = sensores.length;
