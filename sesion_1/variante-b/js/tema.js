// ---------- Tema claro/oscuro + resaltado de navegación ----------

const CLAVE_TEMA = "tema-lanzamientos";

function aplicarTema(tema) {
  document.documentElement.dataset.tema = tema;
  localStorage.setItem(CLAVE_TEMA, tema);
}

function inicializarTema() {
  const guardado = localStorage.getItem(CLAVE_TEMA) || "oscuro";
  aplicarTema(guardado);

  const boton = document.querySelector("#toggle-tema");
  if (boton) {
    boton.addEventListener("click", () => {
      const actual = document.documentElement.dataset.tema;
      aplicarTema(actual === "oscuro" ? "claro" : "oscuro");
    });
  }
}

function resaltarNavActual() {
  const pagina = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav__link").forEach((link) => {
    link.classList.toggle("nav__link--activo", link.getAttribute("href") === pagina);
  });
}

inicializarTema();
resaltarNavActual();
