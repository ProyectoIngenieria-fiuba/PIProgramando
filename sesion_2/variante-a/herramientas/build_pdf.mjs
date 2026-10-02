// Imprime introduccion_sql.html a PDF (A4) usando el runner de browser-automation.
//   node <skill>/browser.mjs file:///.../variante-a/herramientas/introduccion_sql.html --script ./build_pdf.mjs
// Escribe ../INTRODUCCION SQL Y DATOS.pdf (dentro de variante-a/).
import { fileURLToPath } from "node:url";

export default async function run(page) {
  const salida = fileURLToPath(new URL("../INTRODUCCION SQL Y DATOS.pdf", import.meta.url));
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: salida,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="width:100%;font:8px system-ui,sans-serif;color:#94a3b8;text-align:center;">' +
      'Introducción a SQL y análisis de datos — Taller PIP · página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
  });
  return { pdf: salida };
}
