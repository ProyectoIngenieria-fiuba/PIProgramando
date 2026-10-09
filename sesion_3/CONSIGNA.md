# Consigna — Sesión 3 · Alerta de tormentas severas

> ¿Nunca armaron un modelo de ML, o hace mucho que no lo hacen? Antes de arrancar, échenle un ojo a la
> [TEORIA.md](TEORIA.md): son conceptos cortos, con un ejemplo resuelto de otro caso. Y para trabajar
> con la IA, lean la [GUIA_IA.md](GUIA_IA.md).

## Objetivo del día

Trabajar en escuadra (2-4 personas, virtual, con IA) sobre un **modelo heredado que parece perfecto** y
decidir si se puede confiar en él. Esta sesión junta dos cosas: **IA** (entender cuándo un modelo
miente) y **vibecoding** (iterar con una IA para arreglar código).

La habilidad central es una sola: **no confiar en un número lindo**. Todo lo que la IA «arregle» tienen que
poder verificarlo, con métricas y con sus propias palabras.

No hace falta saber ML de antemano ni programar de memoria: la IA los puede ayudar a escribir código,
pero **no sabe qué hay en sus datos ni qué significa cada columna**. Eso lo saben ustedes.

## El escenario

Son el equipo de ciencia de datos del **Servicio Meteorológico** (ficticio, con tinte de organismo
nacional). El equipo anterior se fue y dejó un notebook que, según su nota, tiene un modelo de **alerta de
tormenta severa** con **98 % de accuracy**, listo para emitir alertas el lunes en cinco ciudades.

La jefa de pronóstico les pide:

> *«Antes de poner esto en producción necesito saber si puedo confiar en el modelo. Si no, arreglenlo.
> Y explíquenme con palabras que yo entienda qué estaba mal.»*

> **Aviso:** los datos son **ficticios**, generados para este taller. No tienen relación con los sistemas,
> modelos ni datos reales del SMN.

## Cómo empezar (3 pasos, sin instalar nada)

1. **Abran el notebook en Google Colab** (hace falta una cuenta de Google):
   [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ProyectoIngenieria-fiuba/PIProgramando/blob/main/sesion_3/alerta_tormentas_smn.ipynb)

   *Si el botón no funciona:* bajen [alerta_tormentas_smn.ipynb](alerta_tormentas_smn.ipynb) del repo, entren
   a <https://colab.research.google.com>, elijan **Subir** y seleccionen el archivo.
2. **Hagan una copia para la escuadra**: *Archivo → Guardar una copia en Drive*. Compartan el link con
   edición para que todos puedan escribir. Si cierran la pestaña sin guardar, pierden el trabajo.
3. **Armen los roles** y arranquen corriendo el notebook de arriba hacia abajo (*Entorno de ejecución → Ejecutar todas*):
   - **Piloto/a:** comparte pantalla y escribe en el notebook.
   - **Copiloto/a:** habla con la IA y lee en voz alta lo que devuelve.
   - **Escriba:** completa los checkpoints (el *prompt log*).

   Rotan los roles en cada iteración.

## Qué tienen que lograr

### Objetivo central (obligatorio)

Corregir el notebook hasta tener un modelo **que detecte tormentas de verdad**, evaluado con las métricas
que corresponden, y **explicar por escrito con sus palabras por qué el 98 % inicial era falso**.

Meta orientativa (sobre el conjunto de prueba): que el modelo detecte **al menos 6 de cada 10** tormentas
reales sin que la precisión caiga por debajo de aproximadamente 0,20. Ojo: **alcanzar números parecidos no
alcanza**: cumplir el checklist de validación de más abajo es parte del objetivo.

### Extras (en este orden)

1. **Umbral de alerta:** elegir el umbral de decisión explicando el costo de una falsa alarma frente a una
   tormenta no detectada, en términos del SMN.
2. **Segundo modelo:** probar otro tipo de modelo y compararlos con las métricas correctas.
3. **Importancia de variables:** explicar en lenguaje llano qué mira el modelo para decidir.
4. **README + prompt log:** documentar el proyecto como para mostrarlo en un portafolio.

## La regla del checkpoint

**Antes de aceptar cualquier cambio** (lo haya propuesto la IA o ustedes), anotan en el notebook con
`checkpoint(...)`:

- **Qué pidieron** (o qué cambian).
- **Qué métrica esperan que se mueva y hacia dónde.**
- **Por qué.**

Después de correr, `cerrar_checkpoint(...)`: **qué pasó realmente** y **cómo lo verificaron**.

Los facilitadores van a pasar por su sala y van a preguntar siempre lo mismo: **«¿cómo saben que esto está
bien?»** Respuestas que **no** valen: «porque lo dijo la IA», «porque corre sin errores», «porque subió el
accuracy». Respuestas que sí: números concretos, comparados contra algo, y un motivo.

Un cambio por vez. Si cambian tres cosas juntas y la métrica se mueve, no saben cuál fue.

## Checklist de validación

Antes de dar por terminado el objetivo central, tienen que poder responder **sí** a todo esto:

- [ ] Sé qué porcentaje de los casos son tormentas severas y qué accuracy tendría un modelo que **nunca** alerta.
- [ ] Reporto, como mínimo, **recall, precisión, F1 y la matriz de confusión** (no solo accuracy).
- [ ] Para **cada columna** que usa el modelo, puedo decir **cuándo se conoce ese dato respecto del momento
  en que se emite la alerta**, y **todas** están disponibles en ese momento.
- [ ] Sé explicar con mis palabras qué hace cada cambio que apliqué (no solo «la IA lo puso»).
- [ ] Cada cambio tiene su checkpoint (antes) y su cierre (después), con números.
- [ ] Evalúo siempre en datos que el modelo **no vio** al entrenar ni al decidir nada, y la separación respeta el
  orden del tiempo.
- [ ] Si un número «mejoró mucho», me pregunté **por qué** antes de festejar.
- [ ] Puedo explicarle a alguien que no sabe de ML por qué el 98 % no servía.

## Qué entregan

Al final de la sesión, cada escuadra deja:

1. El **notebook** con el código corregido, los checkpoints completos y la **conclusión escrita** del objetivo central.
2. Si llegan al extra 4: un **README.md** con resumen técnico y el **prompt log** (la plantilla está al final del
   notebook; `prompt_log_markdown()` arma la tabla con sus checkpoints).

Guárdenlo todo: en la próxima sesión arrancan el **proyecto de portafolio**, y esto es la primera pieza que
pueden mostrar.

## Cómo se evalúa

No se mide cuánto subió el número, sino **si pueden defenderlo**:

- Si encontraron los problemas y pueden explicar cómo los detectaron.
- Si cada cambio tiene una hipótesis previa y una verificación posterior.
- Si pudieron decir «esto de la IA estaba mal» (o «esto estaba bien y lo comprobé»).
- Si el relato final es claro para alguien que no es técnico.
