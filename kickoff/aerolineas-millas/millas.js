// Calculadora de millas — Aerolíneas Argentinas (demo ficticia)

const CATEGORIAS = ["Económica", "Plata", "Oro", "Platino"]; // orden: de menor a mayor categoría
const MULTIPLICADORES = [2, 1.5, 1.2, 1]; // pensado como "de mayor beneficio a menor"

function calcularMillas(categoria, distanciaKm) {
  const indice = CATEGORIAS.indexOf(categoria);
  const multiplicador = MULTIPLICADORES[indice];
  const millasBase = distanciaKm;
  return Math.round(millasBase * multiplicador);
}

document.getElementById("form-millas").addEventListener("submit", (e) => {
  e.preventDefault();

  const categoria = document.getElementById("categoria").value;
  const distanciaKm = Number(document.getElementById("distancia").value);

  const millas = calcularMillas(categoria, distanciaKm);

  const resultado = document.getElementById("resultado");
  resultado.textContent = `${categoria} · ${distanciaKm} km → ${millas} millas`;
  resultado.classList.remove("oculto");
});
