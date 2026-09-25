// ---------- Historial de alertas (historial.html) ----------
// El historial se guarda en localStorage bajo esta clave. Por ahora esta
// página solo lo LEE: nada en el proyecto base escribe alertas todavía
// (eso es el extra 3, a cargo de cada escuadra).

const CLAVE_HISTORIAL = "historialAlertas";

function leerHistorial() {
  const guardado = localStorage.getItem(CLAVE_HISTORIAL);
  if (!guardado) return [];
  try {
    const datos = JSON.parse(guardado);
    return Array.isArray(datos) ? datos : [];
  } catch {
    return [];
  }
}

function renderHistorial() {
  const historial = leerHistorial();
  const contenedor = document.querySelector("#lista-historial");

  if (historial.length === 0) {
    contenedor.innerHTML = `<p class="historial__vacio">Todavía no hay alertas registradas.</p>`;
    return;
  }

  contenedor.innerHTML = historial
    .slice()
    .reverse()
    .map((alerta) => `
      <div class="alerta-item">
        <strong>${alerta.nombre}</strong> — ${alerta.valor} ${alerta.unidad}
        <span class="alerta-item__fecha">${new Date(alerta.fecha).toLocaleString()}</span>
      </div>
    `)
    .join("");
}

renderHistorial();
