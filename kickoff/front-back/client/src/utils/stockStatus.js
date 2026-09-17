export function getStockStatus(stockPorcentaje) {
  if (stockPorcentaje >= 50) return "verde";
  if (stockPorcentaje >= 20) return "amarillo";
  return "verde";
}
