// ---------- Cálculo de estados ----------

function calcularEstado(sensor) {
  const { valorActual, verdeMin, verdeMax, rojoMin, rojoMax } = sensor;
  if (valorActual >= verdeMin && valorActual <= verdeMax) return "verde";
  if (valorActual < rojoMin || valorActual > rojoMax) return "rojo";
  return "amarillo";
}

function calcularEstados(listaSensores) {
  return listaSensores.map(calcularEstado);
}

function sensorMasCritico(listaSensores) {
  const prioridad = { rojo: 0, amarillo: 1, verde: 2 };
  return [...listaSensores].sort(
    (a, b) => prioridad[calcularEstado(a)] - prioridad[calcularEstado(b)]
  )[0];
}

// Cantidad de sensores que no están en verde, para mostrarla en el resumen del panel.
var totalSensores = sensores.filter((sensor) => calcularEstado(sensor) !== "verde").length;
