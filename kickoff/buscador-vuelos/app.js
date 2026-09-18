// Buscador de Vuelos — Aerolíneas Argentinas (demo ficticia)
// Actividad de cierre · taller PIP (FIUBA)

// ============================================
// DATOS (no hay que tocar esto)
// ============================================
const VUELOS = [
  { destino: "Bariloche", fecha: "2026-10-05", precio: 45000, duracion: "2h10" },
  { destino: "Bariloche", fecha: "2026-10-12", precio: 52000, duracion: "2h05" },
  { destino: "Córdoba", fecha: "2026-10-06", precio: 28000, duracion: "1h20" },
  { destino: "Córdoba", fecha: "2026-10-09", precio: 31000, duracion: "1h15" },
  { destino: "Mendoza", fecha: "2026-10-07", precio: 34000, duracion: "1h50" },
  { destino: "Mendoza", fecha: "2026-10-15", precio: 39500, duracion: "1h45" },
  { destino: "Salta", fecha: "2026-10-08", precio: 41000, duracion: "2h05" },
  { destino: "Ushuaia", fecha: "2026-10-10", precio: 68000, duracion: "3h35" },
  { destino: "Iguazú", fecha: "2026-10-11", precio: 47000, duracion: "1h55" },
  { destino: "Neuquén", fecha: "2026-10-13", precio: 36000, duracion: "2h00" },
  { destino: "Puerto Madryn", fecha: "2026-10-14", precio: 50000, duracion: "2h20" },
  { destino: "Tucumán", fecha: "2026-10-16", precio: 33000, duracion: "1h40" },
  { destino: "Mar del Plata", fecha: "2026-10-06", precio: 22000, duracion: "0h55" },
  { destino: "El Calafate", fecha: "2026-10-18", precio: 72000, duracion: "3h10" },
  { destino: "San Salvador de Jujuy", fecha: "2026-10-09", precio: 38000, duracion: "1h55" },
];

// ============================================
// TODO — ACÁ VA TU CÓDIGO (ver CONSIGNA.md)
// ============================================
// Esta función recibe la lista completa de vuelos y el texto que el usuario
// escribió en el buscador, y tiene que devolver un array nuevo con SOLO los
// vuelos cuyo destino coincida con ese texto.
//
// Requisitos del básico (están detallados con ejemplos en CONSIGNA.md):
//   - Coincidencia parcial: "bari" debe encontrar "Bariloche".
//   - No debe importar mayúsculas/minúsculas: "BARILOCHE" también debe
//     encontrar "Bariloche".
//   - No debe importar los tildes: "cordoba" debe encontrar "Córdoba".
//
// Mientras no la completes, esta función devuelve TODOS los vuelos sin
// filtrar (a propósito), para que veas la lista completa al cargar la
// página y confirmes que se está llamando correctamente cada vez que
// escribís en el buscador.
function filtrarVuelosPorDestino(vuelos, textoBusqueda) {
  // TODO: reemplazar esta línea por la lógica de filtrado.
  return vuelos;
}

// ============================================
// RENDER (no hay que tocar esto para el básico)
// ============================================
const formateadorPrecio = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  maximumFractionDigits: 0,
});

function formatearFecha(fechaISO) {
  const [anio, mes, dia] = fechaISO.split("-");
  return `${dia}/${mes}/${anio}`;
}

function renderizarVuelos(vuelos) {
  const contenedor = document.getElementById("lista-vuelos");
  const mensajeVacio = document.getElementById("mensaje-vacio");

  if (vuelos.length === 0) {
    contenedor.innerHTML = "";
    mensajeVacio.textContent =
      "No se encontraron vuelos para ese destino. Probá con otra búsqueda.";
    mensajeVacio.classList.remove("oculto");
    return;
  }

  mensajeVacio.classList.add("oculto");
  contenedor.innerHTML = vuelos
    .map(
      (vuelo) => `
      <div class="vuelo">
        <div class="vuelo-info">
          <h2>Buenos Aires → ${vuelo.destino}</h2>
          <p>${formatearFecha(vuelo.fecha)}</p>
        </div>
        <div class="vuelo-precio">
          <span class="precio">${formateadorPrecio.format(vuelo.precio)}</span>
          <span class="duracion">${vuelo.duracion}</span>
        </div>
      </div>`
    )
    .join("");
}

// ============================================
// CONEXIÓN CON LA UI (no hay que tocar esto)
// ============================================
const inputBuscador = document.getElementById("buscador");

inputBuscador.addEventListener("input", (e) => {
  const vuelosFiltrados = filtrarVuelosPorDestino(VUELOS, e.target.value);
  renderizarVuelos(vuelosFiltrados);
});

renderizarVuelos(VUELOS);
