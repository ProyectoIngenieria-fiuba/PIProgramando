// ---------- Render del detalle de un lanzamiento (lanzamiento.html?id=...) ----------

const parametros = new URLSearchParams(window.location.search);
const idBuscado = parametros.get("id");
const lanzamiento = lanzamientos.find((l) => l.id === idBuscado);

let intervaloDetalle = null;

function actualizarCountdownDetalle() {
  const ahora = new Date();
  const diferenciaMs = lanzamientos[0].fechaHora - ahora;

  if (diferenciaMs <= 0) {
    document.querySelector("#detalle-countdown").textContent = "0d 00h 00m 00s";
    clearInterval(intervaloDetalle);
    return;
  }

  document.querySelector("#detalle-countdown").textContent = formatearTiempo(diferenciaMs);
}

function renderDetalle() {
  const contenedor = document.querySelector("#detalle-lanzamiento");

  if (!lanzamiento) {
    contenedor.innerHTML = `<p class="detalle__no-encontrado">No se encontró ningún lanzamiento con ese id.</p>`;
    return;
  }

  contenedor.innerHTML = `
    <h2>${lanzamiento.mision}</h2>
    <p class="detalle__fecha">Fecha programada: ${lanzamiento.fechaHora.toLocaleString()}</p>
    <p class="detalle__descripcion">${descripciones[lanzamiento.id]}</p>
    <p class="detalle__etiqueta">Cuenta regresiva</p>
    <p class="detalle__countdown" id="detalle-countdown">—</p>
    <a class="detalle__volver" href="lanzamientos.html">← Volver a lanzamientos</a>
  `;
}

renderDetalle();

if (lanzamiento) {
  actualizarCountdownDetalle();
  intervaloDetalle = setInterval(actualizarCountdownDetalle, 1000);
}
