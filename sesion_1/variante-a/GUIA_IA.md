# Guía de uso de IA — Sesión 1 · Variante A

Van a resolver este ejercicio con ayuda de una IA (ChatGPT, Claude, Copilot,
la que tengan a mano). Esta guía es para que la usen bien, no para que les
resuelva todo sin que entiendan qué pasó.

## Cómo armar un buen prompt

Un prompt vago ("arreglá el bug") le da a la IA casi nada para trabajar, y
lo más probable es que reescriba cosas que no hacía falta tocar. Denle
contexto real:

1. **Qué archivos están involucrados.** Este proyecto tiene varias páginas
   y varios archivos JS que se llaman entre sí (revisen las etiquetas
   `<script src="...">` de la página donde ven el problema, en ese orden
   están cargados los archivos). Un bug puede estar en un solo archivo, o
   puede depender de cómo se conectan dos. Péguenle a la IA **todos los
   archivos relevantes**, no solo el que les parece sospechoso — si el
   problema aparece en `panel.html`, probablemente necesite ver
   `js/datos.js`, `js/logica.js` y `js/ui-panel.js` juntos, no uno solo.
2. **Qué síntoma ven**, con datos concretos. No es lo mismo decir "los
   colores están mal" que decir "el sensor de Presión (151 bar, rango verde
   140-160) se muestra en rojo" o "el detalle de sensor.html muestra
   Temperatura del núcleo cuando entré desde la tarjeta de Presión".
3. **Qué NO tiene que tocar.** Sean explícitos: no cambiar los valores de
   los sensores, no cambiar la lógica de `calcularEstado`, no reescribir un
   archivo entero ni cambiar el diseño visual. Esto evita que la IA "de
   paso" te cambie diez cosas más.

Ejemplo de prompt razonable:

> Te paso tres archivos de mi proyecto: `js/datos.js`, `js/logica.js` y
> `js/ui-panel.js`, que se cargan en ese orden en `panel.html`. El sensor
> "Presión circuito primario" tiene `valorActual: 151` y rango verde
> 140-160, pero en la página se muestra con el color de estado rojo. No
> quiero que cambies los valores de los sensores ni la función
> `calcularEstado`, esa lógica está bien. Necesito que encuentres por qué
> el color mostrado no corresponde al sensor correcto.

## Checklist para leer el código que te devuelve la IA

Antes de aceptar un cambio, revisen:

- [ ] **¿Tocó solo lo necesario?** Miren el diff (o comparen a ojo) — si
      cambió funciones o archivos que no tenían nada que ver con el bug,
      pregunten por qué, o pídanle que deshaga esa parte.
- [ ] **¿Los nombres tienen sentido?** Si la IA metió una variable con un
      nombre que no dice nada (`temp2`, `x`, `data2`), pídanle que lo
      renombre a algo descriptivo antes de aceptarlo.
- [ ] **¿Hay algo que no entendés?** Si no pueden explicarle a un compañero
      qué hace una línea que agregó la IA, pregúntenle a la IA misma que se
      las explique antes de seguir. No hay que aceptar código que nadie del
      equipo entiende.
- [ ] **¿Se rompió algo que antes andaba?** Prueben las otras páginas, el
      resumen y las otras tarjetas después de cada cambio, no solo el
      sensor que estaban arreglando. Como los archivos comparten variables
      globales, un cambio en `js/datos.js` puede afectar a `sensor.html`
      aunque ustedes solo hayan estado mirando `panel.html`.

## Cómo iterar sin dar vueltas en círculo

- Si el primer intento no resuelve el síntoma, **describan qué ven ahora**
  (con datos concretos, como en el prompt inicial) en vez de repetir
  "no funcionó, arreglalo".
- Sigan la misma conversación con la IA en vez de arrancar un chat nuevo
  cada vez — así no pierden el contexto de lo que ya probaron y descartaron.
- Si la IA propone reescribir todo el proyecto de cero para un bug puntual,
  es una señal de que el prompt necesita más contexto específico (qué
  archivos, qué síntoma exacto), no de que haga falta una reescritura
  completa.
