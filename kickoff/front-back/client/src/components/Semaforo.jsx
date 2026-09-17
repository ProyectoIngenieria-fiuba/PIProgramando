const COLORES = {
  verde: "#22c55e",
  amarillo: "#eab308",
  rojo: "#ef4444",
};

const ETIQUETAS = {
  verde: "Stock OK",
  amarillo: "Stock bajo",
  rojo: "Stock crítico",
};

export default function Semaforo({ estado }) {
  return (
    <div className="semaforo">
      <span className="semaforo-luz" style={{ backgroundColor: COLORES[estado] }} />
      <span className="semaforo-etiqueta">{ETIQUETAS[estado]}</span>
    </div>
  );
}
