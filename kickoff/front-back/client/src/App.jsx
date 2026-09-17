import { useEffect, useState } from "react";
import EstacionCard from "./components/EstacionCard.jsx";
import "./App.css";

export default function App() {
  const [estaciones, setEstaciones] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/estaciones")
      .then((res) => res.json())
      .then((data) => {
        setEstaciones(data);
        setCargando(false);
      })
      .catch((err) => {
        setError(err.message);
        setCargando(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="app__header">
        <h1>Panel de Gestión de Estaciones de Servicio</h1>
        <p>Monitoreo de stock de combustible en tiempo real</p>
      </header>

      {cargando && <p className="app__estado">Cargando estaciones...</p>}
      {error && <p className="app__estado app__estado--error">Error: {error}</p>}

      <main className="estaciones-grid">
        {estaciones.map((estacion) => (
          <EstacionCard key={estacion.id} estacion={estacion} />
        ))}
      </main>
    </div>
  );
}
