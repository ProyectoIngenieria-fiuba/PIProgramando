// Test de humo del dashboard base. Correr con el runner browser-automation:
//   node <skill>/browser.mjs file:///.../variante-a/dashboard_base.html --script ./test_dashboard.mjs
export default async function run(page) {
  const r = [];
  const ok = (n, c, x = "") => r.push({ n, ok: !!c, x: String(x) });
  const main = async (expr) => {
    await page.addScriptTag({ content: "document.documentElement.dataset.out = JSON.stringify((function(){ return " + expr + "; })());" });
    return JSON.parse(await page.evaluate(() => document.documentElement.dataset.out));
  };
  await page.waitForSelector("canvas", { timeout: 30000 });
  await page.waitForTimeout(800);
  ok("3 canvas dibujados", (await page.locator("canvas").count()) === 3);
  ok("3 KPIs", (await page.locator(".kpi").count()) === 3);
  ok("KPI formateado es-AR", (await page.locator(".kpi .valor").first().innerText()) === "1.234", await page.locator(".kpi .valor").first().innerText());
  ok("carteles EJEMPLO en todo (3 KPI + 3 gráficos + conclusión)", (await page.locator(".cartel").count()) === 7, await page.locator(".cartel").count());
  ok("hay vista de tabla por gráfico", (await page.locator("details.tabla-datos").count()) === 3);
  const dibujado = await main("Chart.getChart(document.querySelector('#tarjeta-barras canvas')).data.datasets[0].data.length");
  ok("barras con 6 datos", dibujado === 6, dibujado);
  const leyenda = await main("[Chart.getChart(document.querySelector('#tarjeta-linea canvas')).options.plugins.legend.display, Chart.getChart(document.querySelector('#tarjeta-barras canvas')).options.plugins.legend.display]");
  ok("leyenda: sí en 2 series, no en 1", leyenda[0] === true && leyenda[1] === false, leyenda);
  // errores amigables
  await page.addScriptTag({ content: "DATA.barras.campoValor='no_existe'; dibujarBarras(); DATA.linea.datos=[]; dibujarLinea(); DATA.torta.datos=[1,2,3,4,5,6].map(i=>({grupo:'g'+i,total:i})); dibujarTorta();" });
  const errs = await page.locator(".error").allInnerTexts();
  ok("columna inexistente: mensaje en español con columnas disponibles", errs.some(t => /«barras».*"no_existe".*ruta, valor/.test(t)), errs[0]);
  ok("datos vacíos: mensaje", errs.some(t => /«linea».*al menos una fila/.test(t)));
  ok("torta con >5 partes: mensaje", errs.some(t => /«torta».*más de 5/.test(t)));
  // tema
  await page.addScriptTag({ content: "location.reload()" }); await page.waitForSelector("canvas"); await page.waitForTimeout(600);
  await page.click("#btn-tema"); await page.click("#btn-tema"); await page.waitForTimeout(500);
  ok("tema oscuro aplicado", (await page.getAttribute("html", "data-tema")) === "oscuro");
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  ok("fondo oscuro", bg === "rgb(13, 13, 13)", bg);
  ok("sigue habiendo 3 canvas tras cambiar tema", (await page.locator("canvas").count()) === 3);
  const bad = r.filter(x => !x.ok);
  return { pasaron: r.length - bad.length, fallaron: bad.length, detalle: bad.length ? bad : "todas OK" };
}
