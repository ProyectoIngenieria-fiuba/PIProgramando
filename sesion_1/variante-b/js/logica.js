// ---------- Cálculo y formato del countdown ----------

function pad(numero) {
  return String(numero).padStart(2, "0");
}

function formatearTiempo(diferenciaMs) {
  const signo = diferenciaMs < 0 ? "-" : "";
  const totalSegundos = Math.floor(Math.abs(diferenciaMs) / 1000);
  const dias = Math.floor(totalSegundos / 86400);
  const horas = Math.floor((totalSegundos % 86400) / 3600);
  const minutos = Math.floor((totalSegundos % 3600) / 60);
  const segundos = totalSegundos % 60;
  return `${signo}${dias}d ${pad(horas)}h ${pad(minutos)}m ${pad(segundos)}s`;
}

// Cantidad de lanzamientos programados para los próximos 7 días, para mostrarla en el resumen del panel.
var totalLanzamientos = lanzamientos.filter(
  (lanzamiento) => lanzamiento.fechaHora - new Date() < 7 * 24 * 60 * 60 * 1000
).length;
