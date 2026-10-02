// Test de humo del SQL Lab (se corre con el runner browser-automation).
//   node <skill>/browser.mjs file:///.../dist/a-aerolineas/lab.html --script ./test_lab.mjs
// Devuelve { pasaron, fallaron, detalle }. No toca nada fuera del navegador headless.
export default async function run(page) {
  const resultados = [];
  const check = (nombre, ok, extra = "") => resultados.push({ nombre, ok: !!ok, extra: String(extra) });

  const ejecutar = async (sql) => {
    await page.fill("#editor", sql);
    await page.keyboard.press("Control+Enter");
    await page.waitForTimeout(150);
  };
  // Corre una expresión en el contexto PRINCIPAL de la página (page.evaluate usa un mundo aislado):
  // se inyecta un <script> y el resultado vuelve por el DOM.
  const enPagina = async (expr) => {
    await page.addScriptTag({ content: "document.documentElement.dataset.out = JSON.stringify((function(){ return " + expr + "; })());" });
    return JSON.parse(await page.evaluate(() => document.documentElement.dataset.out));
  };
  const resultadoTexto = () => page.locator("#resultados").innerText();
  const nombresTablas = () => page.locator(".tabla-nombre").evaluateAll((els) => els.map((e) => e.firstChild.textContent.trim()));

  // 1. El motor carga y el esquema aparece
  await page.waitForFunction(() => !document.getElementById("btn-ejecutar").disabled, null, { timeout: 30000 });
  const estado = await page.locator("#estado-motor").innerText();
  check("motor sql.js cargado", /Motor listo/.test(estado), estado);
  let tablas = await nombresTablas();
  check("esquema lista las 7 tablas", tablas.length === 7, tablas.join(","));
  check("esquema muestra PK y FK", (await page.locator(".tag.pk").count()) === 7 && (await page.locator(".tag.fk").count()) === 6);
  check("panel de relaciones", /rutas\.origen_id → aeropuertos\.id/.test(await page.locator("#relaciones").innerText()));

  // 2. Click en una tabla inserta el SELECT
  await page.fill("#editor", "");
  await page.locator(".tabla-nombre", { hasText: "vuelos" }).first().click();
  check("click en tabla inserta SELECT * ... LIMIT 10", (await page.inputValue("#editor")).trim() === "SELECT * FROM vuelos LIMIT 10;");

  // 3. Consulta con Ctrl+Enter
  await ejecutar("SELECT COUNT(*) AS total FROM vuelos;");
  let txt = await resultadoTexto();
  check("Ctrl+Enter ejecuta y muestra 1 fila", /1 fila/.test(txt) && /5\.?211/.test(txt), txt.replace(/\s+/g, " ").slice(0, 80));
  check("muestra el tiempo de ejecución", /ms/.test(txt));

  // 4. Límite de 500 filas con aviso
  await ejecutar("SELECT * FROM vuelos;");
  txt = await resultadoTexto();
  check("más de 500 filas: avisa", /primeras 500 de/.test(txt));
  check("solo pinta 500 filas", (await page.locator("table.res tbody tr").count()) === 500);

  // 5. Varias sentencias
  await ejecutar("SELECT 1 AS a; SELECT 2 AS b;");
  check("varias sentencias: 2 resultados", (await page.locator("table.res").count()) === 2);

  // 6. Errores en español + mensaje original
  await ejecutar("SELECT * FROM tabla_que_no_existe;");
  txt = await resultadoTexto();
  check("error traducido a español", /No existe la tabla "tabla_que_no_existe"/.test(txt), txt.slice(0, 100));
  check("error incluye el mensaje original de SQLite", /Mensaje original de SQLite: no such table/.test(txt));
  await ejecutar("SELEC 1;");
  check("error de sintaxis traducido", /error de sintaxis cerca de "SELEC"/.test(await resultadoTexto()));
  await ejecutar("SELECT COUNT(*) FROM vuelos WHERE COUNT(*) > 1;");
  check("uso indebido de agregación traducido", /función de agregación/.test(await resultadoTexto()));

  // 7. CREATE TABLE actualiza el esquema solo
  await ejecutar("CREATE TABLE prueba_alumno (id INTEGER PRIMARY KEY, aeropuerto_id INTEGER REFERENCES aeropuertos(id), nota TEXT);");
  tablas = await nombresTablas();
  check("CREATE TABLE aparece en el esquema sin recargar", tablas.includes("prueba_alumno") && tablas.length === 8, tablas.join(","));
  check("la FK de la tabla nueva se ve", /prueba_alumno\.aeropuerto_id → aeropuertos\.id/.test(await page.locator("#relaciones").innerText()));

  // 8. Claves foráneas activas
  await ejecutar("INSERT INTO prueba_alumno (id, aeropuerto_id, nota) VALUES (1, 9999, 'x');");
  check("FOREIGN KEY se hace cumplir", /clave foránea/.test(await resultadoTexto()));
  await ejecutar("INSERT INTO prueba_alumno (id, aeropuerto_id, nota) VALUES (1, 1, 'ok');");
  await ejecutar("SELECT * FROM prueba_alumno;");
  check("INSERT válido funciona", /1 fila/.test(await resultadoTexto()));

  // 9. DROP también refresca
  await ejecutar("DROP TABLE prueba_alumno;");
  check("DROP TABLE desaparece del esquema", !(await nombresTablas()).includes("prueba_alumno"));

  // 10. Reiniciar base (con UPDATE destructivo de por medio)
  await ejecutar("DELETE FROM incidencias;");
  await ejecutar("SELECT COUNT(*) AS n FROM incidencias;");
  check("DELETE efectivamente vació la tabla", /\b0\b/.test(await resultadoTexto()));
  await ejecutar("CREATE TABLE otra (x INTEGER);");
  page.once("dialog", (d) => d.accept());
  await page.click("#btn-reiniciar");
  await page.waitForTimeout(300);
  check("reiniciar: vuelve a las 7 tablas", (await nombresTablas()).length === 7);
  await ejecutar("SELECT COUNT(*) AS n FROM incidencias;");
  check("reiniciar: los datos borrados volvieron", /1\.?375/.test(await resultadoTexto()), (await resultadoTexto()).replace(/\s+/g, " ").slice(0, 60));

  // 11. Reiniciar y cancelar el diálogo no cambia nada
  await ejecutar("CREATE TABLE otra2 (x INTEGER);");
  page.once("dialog", (d) => d.dismiss());
  await page.click("#btn-reiniciar");
  check("cancelar el diálogo conserva los cambios", (await nombresTablas()).includes("otra2"));
  page.once("dialog", (d) => d.accept());
  await page.click("#btn-reiniciar");

  // 12. Copiar resultado: contenido de JSON / CSV / Markdown
  await ejecutar("SELECT codigo_iata, ciudad, NULL AS vacio FROM aeropuertos ORDER BY id LIMIT 2;");
  const formatos = await enPagina("({ json: aJSON(ultimoResultado), csv: aCSV(ultimoResultado), md: aMarkdown(ultimoResultado) })");
  const j = JSON.parse(formatos.json);
  check("JSON: array de objetos con null", Array.isArray(j) && j.length === 2 && j[0].codigo_iata === "AEP" && j[0].vacio === null, formatos.json.replace(/\s+/g, " ").slice(0, 80));
  check("CSV: encabezado y filas", formatos.csv.split("\n")[0] === "codigo_iata,ciudad,vacio" && formatos.csv.split("\n").length === 3, formatos.csv.replace(/\n/g, " / "));
  check("Markdown: tabla con separador", /^\| codigo_iata \| ciudad \| vacio \|\n\| --- \| --- \| --- \|\n\| AEP /.test(formatos.md));
  await page.click("#btn-json");
  await page.waitForTimeout(200);
  check("botón copiar da aviso de éxito", /JSON copiado/.test(await page.locator("#aviso-copia").innerText()), await page.locator("#aviso-copia").innerText());

  // 13. Copiar esquema para la IA
  const esq = await enPagina("textoEsquemaParaIA()");
  check("esquema IA: aclara SQLite", /SQLite/.test(esq));
  check("esquema IA: trae los 7 CREATE TABLE", (esq.match(/CREATE TABLE/g) || []).length === 7);
  check("esquema IA: trae 3 filas de ejemplo por tabla", (esq.match(/-- 3 filas de ejemplo de/g) || []).length === 7 && /-- 1 \| AEP \|/.test(esq));
  await page.click("#btn-esquema-ia");
  await page.waitForTimeout(200);
  check("botón esquema IA da aviso de éxito", /Esquema copiado/.test(await page.locator("#aviso-copia").innerText()));

  // 14. Historial (y que funcione aunque localStorage falle)
  check("historial registra consultas", (await page.locator("#historial .item").count()) >= 5);
  await page.addScriptTag({ content: 'Object.defineProperty(window, "localStorage", { get() { throw new Error("storage bloqueado"); }, configurable: true });' });
  await ejecutar("SELECT 'sin storage' AS prueba;");
  check("sin localStorage: la consulta corre igual", /sin storage/.test(await resultadoTexto()));
  check("sin localStorage: el historial sigue en memoria", (await page.locator("#historial .item").first().innerText()).includes("sin storage"));
  await page.click("#btn-borrar-historial");
  check("borrar historial", (await page.locator("#historial .item").count()) === 0);

  // 15. Un SELECT con función de ventana (SQLite del navegador debe soportarlo)
  await ejecutar("SELECT id, RANK() OVER (ORDER BY id DESC) AS r FROM aeropuertos LIMIT 1;");
  check("funciones de ventana disponibles", /\b28\b/.test(await resultadoTexto()) && !/Mensaje original/.test(await resultadoTexto()));

  const fallaron = resultados.filter((r) => !r.ok);
  return { pasaron: resultados.length - fallaron.length, fallaron: fallaron.length, detalle: fallaron.length ? fallaron : "todas OK" };
}
