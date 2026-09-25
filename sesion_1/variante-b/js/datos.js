// ---------- Datos de los lanzamientos ----------
// Las fechas se calculan relativas al momento en que se abre la página, para
// que el countdown del más próximo siempre sea corto de probar en vivo,
// sin importar qué día se corra el taller.

const AHORA = new Date();

function dentroDe(minutos) {
  return new Date(AHORA.getTime() + minutos * 60000);
}

const lanzamientos = [
  { id: "ceibo-1", mision: "Ceibo-1", fechaHora: dentroDe(1.5) },
  { id: "jacaranda-2", mision: "Jacarandá-2", fechaHora: dentroDe(2 * 24 * 60) },
  { id: "aconcagua-sat", mision: "Aconcagua Sat", fechaHora: dentroDe(5 * 24 * 60) },
  { id: "yastay-3", mision: "Yastay-3", fechaHora: dentroDe(12 * 24 * 60) },
  { id: "copihue-austral", mision: "Copihue Austral", fechaHora: dentroDe(25 * 24 * 60) },
];

const descripciones = {
  "ceibo-1": "Satélite ficticio de observación terrestre en órbita baja, con foco en monitoreo agrícola.",
  "jacaranda-2": "Satélite ficticio de comunicaciones para conectividad en zonas rurales.",
  "aconcagua-sat": "Satélite ficticio de estudio climático en regiones de alta montaña.",
  "yastay-3": "Satélite ficticio de monitoreo de recursos hídricos.",
  "copihue-austral": "Satélite ficticio de observación de la Patagonia y el Atlántico Sur.",
};

// Cantidad total de lanzamientos programados, para mostrarla en el resumen del panel.
var totalLanzamientos = lanzamientos.length;
