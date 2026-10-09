# Guía de uso de IA — Sesión 3 · Modelos que mienten

Van a trabajar con la IA que tengan a mano (ChatGPT, Claude, Gemini, Copilot, la que sea, en su versión
gratuita). Esta guía vale para cualquiera.

En esta sesión la IA **no es solo una ayuda**: es parte de lo que se evalúa. Lo que se mira es cómo
la usan: si piden bien, si leen lo que devuelve y si **verifican** antes de aceptar.

La idea central: **la IA escribe código muy rápido, pero no sabe qué significan sus columnas ni qué es
verdad en su problema.** Todo lo que devuelva es una **hipótesis que hay que verificar**, no una respuesta.

## 1. Pedir bien

### Un prompt malo

> *Arreglame este notebook para que el modelo ande mejor.*

No dice qué significa «mejor», no da contexto y le deja a la IA decidir todo. Va a devolver algo que
«parece» razonable (casi seguro: agregar `class_weight`) y a presentarlo con seguridad.

### Un prompt bueno

> *Tengo un clasificador (regresión logística de scikit-learn) que predice si habrá una tormenta severa en
> las próximas 3 horas, para emitir una alerta. Solo el 3 % de los casos son tormentas. Estas son mis
> columnas y qué mide cada una:* `[pegar el diccionario de datos]`.
>
> *Mi accuracy es 98 %, pero sospecho que no detecta tormentas. Antes de escribir código: (1) decime qué
> métricas deberíamos mirar y por qué, y (2) listame qué cosas podrían estar mal en el planteo, incluyendo los
> datos. Después proponeme UN cambio por vez, y decime qué número esperás que se mueva.*

Por qué anda mejor:
- **Contexto:** problema real, qué se predice, **cuándo se emite la alerta**.
- **Diccionario de datos:** la IA no puede razonar sobre cuándo se conoce un dato si no sabe qué es.
- **Pide diagnóstico antes que código.**
- **Un cambio por vez + qué esperar:** es exactamente lo que piden los checkpoints.

### Otras fórmulas útiles

- *«¿Qué supuestos estás haciendo sobre mis datos?»*
- *«Explicame línea por línea qué hace este código.»*
- *«¿Qué podría salir mal con este cambio? ¿Cómo lo verifico?»*
- *«Hacé de abogado del diablo: ¿por qué este resultado podría ser demasiado bueno?»*

## 2. Leer lo que devuelve

Antes de copiar y pegar:

1. **¿Entiendo qué hace cada línea?** Si no, pregunten hasta entender. Si no pueden explicarlo, no lo aceptan.
2. **¿Cambió una sola cosa o varias?** Las IA suelen reescribir de más. Pídanle cambios mínimos.
3. **¿Cambió el conjunto de prueba, el split o la métrica sin avisar?** Si cambia cómo se mide, el antes y el
   después ya no son comparables.
4. **¿Los números que menciona los calculó o los inventó?** Una IA que no ejecuta código **no puede saber** qué
   métrica va a dar. Los números salen de **correr el notebook**, no de la respuesta.

## 3. Errores típicos de la IA en esta tarea

| Qué hace la IA | Por qué es un problema | Qué hacer |
|---|---|---|
| **«Arregla» sin mejorar nada:** reescribe el código, dice «ahora debería funcionar mejor» | No hay evidencia de mejora | Comparen **antes y después con las mismas métricas** |
| **Propone `class_weight` o SMOTE enseguida**, sin preguntar nada sobre los datos | Atacan el desbalance, pero el desbalance no es la única causa posible de un resultado raro | Pregunten qué *más* podría estar mal; revisen las columnas |
| **No revisa si alguna columna trae información del futuro** | Los números suben y nadie se pregunta por qué | Aplíquenle a cada columna la pregunta: *¿lo sé cuando tengo que decidir?* |
| **Aplica SMOTE antes de separar entrenamiento y prueba**, o mezcla las filas al azar | Contamina la evaluación con información de la prueba (¡otra fuga!) | Todo lo que «aprende» de los datos se hace **solo con entrenamiento** |
| **Inventa métricas** («este cambio sube el recall a 0,92») | No ejecutó nada | Ejecuten ustedes y miren su propio número |
| **Celebra un número demasiado lindo** | Un salto grande es sospechoso, no un premio | Pregúntense qué lo explica antes de aceptarlo |
| **Cambia una columna por otra de nombre parecido** | Puede sacar la legítima y dejar la problemática | Compárenla con el diccionario, no con el nombre |
| **Elige el umbral mirando el conjunto de prueba** | La prueba deja de ser prueba | Elijan con un tramo de validación aparte |
| **Optimiza solo accuracy**, o F1 sin pensar el costo de cada error | No refleja qué importa en el problema | Definan primero cuál error es más caro |
| **Responde con mucha seguridad** aunque se equivoque | El tono no es evidencia | Verifiquen igual, siempre |

## 4. Cómo verificar lo que la IA hace

La receta de cada iteración (es lo que piden los checkpoints):

1. **Antes de aplicar:** anoten qué métrica esperan que se mueva y hacia dónde.
2. **Apliquen un solo cambio** y corran.
3. **Comparen** con la corrida anterior (mismo split, mismas métricas).
4. **Si se movió distinto a lo esperado**, no sigan: entiendan por qué. Ese es el momento que más se aprende.
5. **Si se movió «demasiado bien»**, sospechen. Pregunten qué lo explicaría.

Y siempre pueden **contraargumentar**: pregúntenle a la IA *«¿por qué crees que esto funciona?»* y fíjense si
su explicación coincide con lo que ven en los números.

## 5. Cómo llevar el prompt log

El **prompt log** es la tabla que arman con los checkpoints. Sirve para que otra persona (o ustedes en
un mes) entienda **cómo** llegaron al resultado. Es una de las cosas que van a poder mostrar en su portafolio.

Un renglón se ve así:

| Qué pedí | Qué esperaba ver mover y por qué | Qué pasó | Cómo verifiqué |
|---|---|---|---|
| *(ejemplo con otro caso)* Que aplique `class_weight='balanced'` en el modelo de fraude | El recall sube y la precisión baja: el modelo se anima más a marcar fraude | Recall 0,31 → 0,84; precisión 0,70 → 0,22 | Reviso la matriz de confusión y comparé contra el baseline en el mismo conjunto de prueba |

Reglas:
- **Resuman el pedido**, no peguen conversaciones enteras (pueden guardar el chat aparte).
- **Escriban qué esperaban ANTES de correr.** Si lo escriben después, no sirve.
- **Los números, con números.** «Mejoró» no es una verificación.
- **Anoten también las veces que la IA se equivocó**: ese renglón vale más que uno que salió bien.

## 6. Si no usan IA en algún momento

Está bien. El checkpoint se llena igual: en «qué pedí» escriban *«lo hicimos a mano: …»*. La regla es la
misma: hipótesis antes, verificación después.

## Una última advertencia

Si terminan en diez minutos con un modelo que «anda perfecto» y no pueden explicar por qué, **probablemente
la IA les resolvió el ejercicio equivocado**. Cuando la sesión parece fácil, es hora de desconfiar.
