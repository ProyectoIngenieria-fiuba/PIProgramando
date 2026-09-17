import Semaforo from "./Semaforo.jsx";
import { getStockStatus } from "../utils/stockStatus.js";

export default function EstacionCard({ estacion }) {
  const estado = getStockStatus(estacion.stockPorcentaje);

  return (
    <div className={`estacion-card estacion-card--${estado}`}>
      <div className="estacion-card__header">
        <h3>{estacion.nombre}</h3>
        <Semaforo estado={estado} />
      </div>
      <dl className="estacion-card__detalles">
        <div>
          <dt>Provincia</dt>
          <dd>{estacion.provincia}</dd>
        </div>
        <div>
          <dt>Combustible</dt>
          <dd>{estacion.combustible}</dd>
        </div>
        <div>
          <dt>Stock</dt>
          <dd>{estacion.stockPorcentaje}%</dd>
        </div>
      </dl>
    </div>
  );
}
