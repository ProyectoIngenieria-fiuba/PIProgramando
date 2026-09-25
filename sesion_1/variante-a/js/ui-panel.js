// ---------- Render del panel de sensores (panel.html) ----------

const estados = calcularEstados(sensores);

function renderPanel() {
  // Se ordena una copia alfabéticamente para que el panel se vea prolijo.
  const sensoresOrdenados = [...sensores].sort((a, b) => a.nombre.localeCompare(b.nombre));

  const contenedor = document.querySelector("#lista-sensores");
  contenedor.innerHTML = "";

  sensoresOrdenados.forEach((sensor, i) => {
    const estado = estados[i];
    const icono = iconos[sensor.id];
    const descripcion = descripciones[sensor.id];

    const card = document.createElement("div");
    card.className = `sensor-card estado-${estado}`;
    card.innerHTML = `
      <div class="sensor-card__header">
        <span class="sensor-card__icono">${icono}</span>
        <h3 class="sensor-card__nombre">${sensor.nombre}</h3>
      </div>
      <p class="sensor-card__valor">${sensor.valorActual} ${sensor.unidad}</p>
      <p class="sensor-card__descripcion">${descripcion}</p>
      <a class="sensor-card__link" href="sensor.html?id=${sensor.id}">Ver detalle →</a>
    `;
    contenedor.appendChild(card);
  });

  renderResumen();
}

function renderResumen() {
  const conteo = { verde: 0, amarillo: 0, rojo: 0 };
  estados.forEach((estado) => conteo[estado]++);

  document.querySelector("#contador-total").textContent = totalSensores;
  document.querySelector("#contador-verde").textContent = conteo.verde;
  document.querySelector("#contador-amarillo").textContent = conteo.amarillo;
  document.querySelector("#contador-rojo").textContent = conteo.rojo;
}

renderPanel();
