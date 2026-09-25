// ---------- Render del panel de lanzamientos (lanzamientos.html) ----------

let intervaloId = null;
let tiempoRestanteTexto = "";

function actualizarCountdown() {
  const proximo = lanzamientos[0];
  const ahora = new Date();
  const diferenciaMs = proximo.fechaHora - ahora;

  tiempoRestanteTexto = formatearTiempo(diferenciaMs);
  document.querySelector("#countdown-tiempo").textContent = tiempoRestanteTexto;

  if (tiempoRestanteTexto === "00d 00h 00m 00s") {
    clearInterval(intervaloId);
    document.querySelector("#countdown-estado").textContent = "¡Lanzado! 🚀";
    document.querySelector("#countdown").classList.add("countdown--lanzado");
  }
}

function renderResumen() {
  document.querySelector("#contador-total").textContent = totalLanzamientos;
  document.querySelector("#proxima-mision").textContent = lanzamientos[0].mision;
}

function renderLista() {
  const contenedor = document.querySelector("#lista-lanzamientos");
  contenedor.innerHTML = "";

  lanzamientos.forEach((lanzamiento) => {
    const item = document.createElement("li");
    item.className = "lanzamiento-item";
    item.innerHTML = `
      <div>
        <span class="lanzamiento-item__mision">${lanzamiento.mision}</span>
        <span class="lanzamiento-item__fecha">${lanzamiento.fechaHora.toLocaleString()}</span>
      </div>
      <a class="lanzamiento-item__link" href="lanzamiento.html?id=${lanzamiento.id}">Ver detalle →</a>
    `;
    contenedor.appendChild(item);
  });
}

// ---------- Inicialización ----------

document.querySelector("#countdown-mision").textContent = lanzamientos[0].mision;
renderResumen();
renderLista();
actualizarCountdown();
intervaloId = setInterval(actualizarCountdown, 1000);
