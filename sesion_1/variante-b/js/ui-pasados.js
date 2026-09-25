// ---------- Lanzamientos pasados (pasados.html) ----------
// Se guardan en localStorage bajo esta clave. Por ahora esta página solo LOS
// LEE: nada en el proyecto base escribe lanzamientos pasados todavía (eso es
// el extra 3, a cargo de cada escuadra).

const CLAVE_PASADOS = "lanzamientosPasados";

function leerPasados() {
  const guardado = localStorage.getItem(CLAVE_PASADOS);
  if (!guardado) return [];
  try {
    const datos = JSON.parse(guardado);
    return Array.isArray(datos) ? datos : [];
  } catch {
    return [];
  }
}

function renderPasados() {
  const pasados = leerPasados();
  const contenedor = document.querySelector("#lista-pasados");

  if (pasados.length === 0) {
    contenedor.innerHTML = `<p class="lista-vacia">Todavía no hay lanzamientos pasados.</p>`;
    return;
  }

  contenedor.innerHTML = pasados
    .slice()
    .reverse()
    .map((lanzamiento) => `
      <div class="lanzamiento-item">
        <div>
          <span class="lanzamiento-item__mision">${lanzamiento.mision}</span>
          <span class="lanzamiento-item__fecha">Lanzado: ${new Date(lanzamiento.fechaHora).toLocaleString()}</span>
        </div>
      </div>
    `)
    .join("");
}

renderPasados();
