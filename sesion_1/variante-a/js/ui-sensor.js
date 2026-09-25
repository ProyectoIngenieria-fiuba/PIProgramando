// ---------- Render del detalle de un sensor (sensor.html?id=...) ----------

const parametros = new URLSearchParams(window.location.search);
const idBuscado = parametros.get("id");

// Se reordena alfabéticamente igual que en panel.html, para ubicar la
// posición del sensor buscado dentro de esa vista ordenada.
const sensoresOrdenados = [...sensores].sort((a, b) => a.nombre.localeCompare(b.nombre));
const posicion = sensoresOrdenados.findIndex((sensor) => sensor.id === idBuscado);
const sensor = sensores[posicion];

function renderDetalle() {
  const contenedor = document.querySelector("#detalle-sensor");

  if (!sensor) {
    contenedor.innerHTML = `<p class="detalle__no-encontrado">No se encontró ningún sensor con ese id.</p>`;
    return;
  }

  const estado = calcularEstado(sensor);
  const icono = iconos[sensor.id];
  const descripcion = descripciones[sensor.id];

  const rango = sensor.rojoMax - sensor.rojoMin;
  const inicioVerde = ((sensor.verdeMin - sensor.rojoMin) / rango) * 100;
  const finVerde = ((sensor.verdeMax - sensor.rojoMin) / rango) * 100;
  const posicionMarcador = Math.min(100, Math.max(0,
    ((sensor.valorActual - sensor.rojoMin) / rango) * 100
  ));

  contenedor.innerHTML = `
    <div class="detalle__header">
      <span class="detalle__icono">${icono}</span>
      <h2>${sensor.nombre}</h2>
    </div>
    <p class="detalle__valor estado-${estado}">${sensor.valorActual} ${sensor.unidad}</p>
    <p class="detalle__descripcion">${descripcion}</p>

    <div class="gauge">
      <div class="gauge__zona gauge__zona--amarillo" style="width: ${inicioVerde}%"></div>
      <div class="gauge__zona gauge__zona--verde" style="width: ${finVerde - inicioVerde}%"></div>
      <div class="gauge__zona gauge__zona--amarillo" style="width: ${100 - finVerde}%"></div>
      <div class="gauge__marcador" style="left: ${posicionMarcador}%"></div>
    </div>
    <div class="gauge__etiquetas">
      <span>${sensor.rojoMin} ${sensor.unidad}</span>
      <span>${sensor.rojoMax} ${sensor.unidad}</span>
    </div>

    <a class="detalle__volver" href="panel.html">← Volver al panel</a>
  `;
}

renderDetalle();
