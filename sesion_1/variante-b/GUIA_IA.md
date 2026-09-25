# Guía de uso de IA — Sesión 1 · Variante B

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
   archivos relevantes** — si el problema aparece en `lanzamientos.html`,
   probablemente necesite ver `js/datos.js`, `js/logica.js` y
   `js/ui-lanzamientos.js` juntos, no uno solo.
2. **Qué síntoma ven**, con datos concretos. No es lo mismo decir "el
   countdown está roto" que decir "cuando el countdown de Ceibo-1 llega a
   cero, en vez de mostrar '¡Lanzado!' sigue corriendo en negativo, tipo
   '-0d 00h 00m 12s'" o "en el detalle de Copihue Austral, la fecha dice
   19/10 pero el countdown marca minutos, no días".
3. **Qué NO tiene que tocar.** Sean explícitos: no cambiar las fechas de
   los lanzamientos, no cambiar cómo se calculan (`dentroDe`), no cambiar
   el formato del texto que se muestra, no reescribir un archivo entero.
   Esto evita que la IA "de paso" te cambie diez cosas más.

Ejemplo de prompt razonable:

> Te paso tres archivos de mi proyecto: `js/datos.js`, `js/logica.js` y
> `js/ui-lanzamientos.js`, que se cargan en ese orden en
> `lanzamientos.html`. Cuando el countdown del lanzamiento más próximo
> llega a cero, en vez de detenerse y mostrar "¡Lanzado!", sigue corriendo
> en negativo indefinidamente (por ejemplo, "-0d 00h 00m 12s" y sigue
> bajando). No quiero que cambies las fechas de los lanzamientos ni el
> formato del texto que se muestra en pantalla. Necesito que encuentres
> por qué la condición que debería frenar el `setInterval` nunca se
> cumple.

## Checklist para leer el código que te devuelve la IA

Antes de aceptar un cambio, revisen:

- [ ] **¿Tocó solo lo necesario?** Miren el diff (o comparen a ojo) — si
      cambió funciones o archivos que no tenían nada que ver con el bug,
      pregunten por qué, o pídanle que deshaga esa parte.
- [ ] **¿Los nombres tienen sentido?** Si la IA metió una variable con un
      nombre que no dice nada (`x`, `temp`, `data2`), pídanle que lo
      renombre a algo descriptivo antes de aceptarlo.
- [ ] **¿Hay algo que no entendés?** Si no pueden explicarle a un compañero
      qué hace una línea que agregó la IA (sobre todo si tocó cuentas con
      `Date` o milisegundos), pregúntenle a la IA misma que se las explique
      antes de seguir.
- [ ] **¿Se rompió algo que antes andaba?** Prueben las otras páginas y los
      otros lanzamientos de la lista después de cada cambio, no solo el que
      estaban arreglando. Como los archivos comparten variables globales,
      un cambio en `js/datos.js` puede afectar a `lanzamiento.html` aunque
      ustedes solo hayan estado mirando `lanzamientos.html`.

## Cómo iterar sin dar vueltas en círculo

- Si el primer intento no resuelve el síntoma, **describan qué ven ahora**
  (con datos concretos, como en el prompt inicial) en vez de repetir "no
  funcionó, arreglalo".
- Sigan la misma conversación con la IA en vez de arrancar un chat nuevo
  cada vez — así no pierden el contexto de lo que ya probaron y descartaron.
- Si la IA propone reescribir todo el proyecto de cero para un bug
  puntual, es una señal de que el prompt necesita más contexto específico
  (qué archivos, qué síntoma exacto), no de que haga falta una reescritura
  completa.
- Tengan paciencia con el tiempo real: para confirmar que el fix del
  countdown principal funciona, tienen que esperar a que el countdown de
  Ceibo-1 llegue efectivamente a cero (menos de dos minutos desde que
  entraron a "Lanzamientos") — no se puede verificar de un vistazo al
  código.
