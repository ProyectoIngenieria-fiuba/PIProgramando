// Lista de tareas — proyecto de práctica del taller PIP.
//
// Este archivo tiene más comentarios de lo normal a propósito: la idea es
// que lo leas junto con INTRODUCCION_FRONT_BACK.pdf, no que lo depures.
// El patrón de fondo es el mismo que vas a encontrar en los ejercicios con
// bugs: datos en un array -> función que pinta el HTML a partir de esos
// datos -> evento que modifica los datos -> se vuelve a pintar todo.

// ---------- Datos ----------
// Un array de objetos: cada tarea es un objeto con id, texto y si está hecha.

let tareas = [
  { id: 1, texto: "Leer la introducción de Front y Back", hecha: true },
  { id: 2, texto: "Abrir este proyecto en el navegador", hecha: true },
  { id: 3, texto: "Tocar el código y ver qué pasa", hecha: false },
];

let siguienteId = 4; // para que cada tarea nueva tenga un id distinto

// ---------- Render ----------
// "Render" acá significa: mirar el array `tareas` y generar el HTML que
// le corresponde. Se llama después de CUALQUIER cambio en los datos.

function renderTareas() {
  const contenedor = document.querySelector("#lista-tareas");
  contenedor.innerHTML = ""; // se limpia antes de volver a pintar todo

  if (tareas.length === 0) {
    contenedor.innerHTML = `<p class="lista-vacia">No hay tareas. ¡Agregá una!</p>`;
    renderContador();
    return;
  }

  tareas.forEach((tarea) => {
    const item = document.createElement("li");
    item.className = "tarea" + (tarea.hecha ? " tarea--hecha" : "");
    item.dataset.id = tarea.id;

    item.innerHTML = `
      <span class="tarea__texto">${tarea.texto}</span>
      <button class="tarea__borrar" aria-label="Borrar tarea">✕</button>
    `;

    contenedor.appendChild(item);
  });

  renderContador();
}

function renderContador() {
  const hechas = tareas.filter((tarea) => tarea.hecha).length;
  document.querySelector("#contador").textContent =
    `${hechas} de ${tareas.length} completadas`;
}

// ---------- Cambios en los datos ----------

function agregarTarea(texto) {
  tareas.push({ id: siguienteId, texto, hecha: false });
  siguienteId++;
}

function alternarTarea(id) {
  const tarea = tareas.find((tarea) => tarea.id === id);
  if (tarea) {
    tarea.hecha = !tarea.hecha;
  }
}

function borrarTarea(id) {
  tareas = tareas.filter((tarea) => tarea.id !== id);
}

// ---------- Eventos ----------

document.querySelector("#form-nueva-tarea").addEventListener("submit", (evento) => {
  evento.preventDefault(); // sin esto, el navegador recargaría la página al enviar el form

  const input = document.querySelector("#nueva-tarea");
  const texto = input.value.trim();
  if (texto === "") return; // no agregamos tareas vacías

  agregarTarea(texto);
  input.value = "";
  renderTareas();
});

// Un solo listener en el contenedor (no uno por tarea) que revisa QUÉ se
// clickeó. Esto se llama "delegación de eventos": hace falta acá porque
// `renderTareas()` borra y vuelve a crear los elementos con `innerHTML`,
// así que cualquier listener puesto directamente en un <li> se perdería
// apenas se vuelve a pintar la lista.
document.querySelector("#lista-tareas").addEventListener("click", (evento) => {
  const item = evento.target.closest(".tarea");
  if (!item) return;

  const id = Number(item.dataset.id);

  if (evento.target.matches(".tarea__borrar")) {
    borrarTarea(id);
    renderTareas();
  } else if (evento.target.matches(".tarea__texto")) {
    alternarTarea(id);
    renderTareas();
  }
});

// ---------- Arranque ----------

renderTareas();
