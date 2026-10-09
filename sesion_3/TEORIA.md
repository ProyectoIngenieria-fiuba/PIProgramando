# Teoría — Sesión 3 · Modelos que mienten

No necesitan saber ML para esta sesión. Necesitan estos cinco conceptos, que se explican mejor con otro
caso: **un modelo que detecta una enfermedad rara** (lo vamos a usar como ejemplo resuelto). Vuelvan acá
cuando algo no les cierre.

## 1. Clasificación y datos desbalanceados

Un **clasificador** recibe columnas (variables) y devuelve una categoría: «sí/no». Se **entrena** con casos
cuya respuesta ya conocemos y se **evalúa** con casos que nunca vio.

Los datos están **desbalanceados** cuando una categoría es mucho más rara que otra. Pasa justo con lo que nos
importa: fraudes, enfermedades raras, fallas, tormentas severas. Si el 99 % de los casos son «no», un modelo
que siempre contesta «no» acierta el 99 %… y no sirve para nada.

**Cómo detectarlo:** contar cuántos casos hay de cada clase *antes* de entrenar (`y.value_counts()`).

**Qué se puede hacer:** darle más peso a la clase rara al entrenar (`class_weight`), sobre-muestrearla (SMOTE),
o mover el umbral de decisión (sección 5). Ninguna de las tres arregla problemas **en los datos** (ver 3).

## 2. Accuracy, recall, precisión y F1

Todo sale de cuatro números (la **matriz de confusión**), donde «positivo» es el caso raro que buscamos:

|  | El modelo dice «sí» | El modelo dice «no» |
|---|---|---|
| **Era «sí»** | Verdadero positivo (**VP**): lo detectó | Falso negativo (**FN**): se le escapó |
| **Era «no»** | Falso positivo (**FP**): falsa alarma | Verdadero negativo (**VN**) |

- **Accuracy** = (VP + VN) / total. «¿Qué porcentaje acierta?» Engaña con clases desbalanceadas.
- **Recall** (sensibilidad) = VP / (VP + FN). «De los casos reales, ¿cuántos detectó?»
- **Precisión** = VP / (VP + FP). «De las veces que dijo “sí”, ¿cuántas tenía razón?»
- **F1** = promedio armónico de precisión y recall. Un solo número que castiga que alguno sea muy bajo.

En scikit-learn:

```python
from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, digits=3))
```

### Ejemplo resuelto: detección de una enfermedad rara

Un hospital prueba un modelo para detectar una enfermedad que tiene **1 de cada 100** pacientes. Evalúan con 10.000
pacientes: 100 enfermos y 9.900 sanos. El modelo dice «sano» para todos.

| | Dice «enfermo» | Dice «sano» |
|---|---|---|
| **Enfermos (100)** | VP = 0 | FN = 100 |
| **Sanos (9.900)** | FP = 0 | VN = 9.900 |

- Accuracy = 9.900 / 10.000 = **99 %** (¡excelente!).
- Recall = 0 / 100 = **0 %** (no detecta a ningún enfermo).
- Precisión: indefinida (nunca dijo «enfermo»).

Ahora el equipo le da más peso a los enfermos y el modelo mejora:

| | Dice «enfermo» | Dice «sano» |
|---|---|---|
| **Enfermos (100)** | VP = 80 | FN = 20 |
| **Sanos (9.900)** | FP = 400 | VN = 9.500 |

- Accuracy = (80 + 9.500) / 10.000 = **95,8 %** (¡**bajó**, y el modelo es muchísimo mejor!).
- Recall = 80 / 100 = **80 %**.
- Precisión = 80 / (80 + 400) = **16,7 %**: de cada 6 pacientes marcados, solo 1 está enfermo.
- F1 = 2 · 0,167 · 0,80 / (0,167 + 0,80) ≈ **0,28**.

Moraleja: el accuracy cayó y el modelo mejoró. Lo que importa depende de **qué cuesta más equivocarse**:
no detectar a un enfermo (FN) o hacer un estudio de más a un sano (FP).

## 3. Fuga de datos (*data leakage*)

Hay **fuga de datos** cuando el modelo usa información que, en el momento real de tomar la decisión,
**todavía no existiría**. El modelo «hace trampa»: en el notebook saca notas excelentes, pero en producción
no tiene esa información y falla.

Se parece a rendir un examen con la hoja de respuestas al lado. La nota es buenísima, y no dice nada de lo
que sabés.

**La pregunta que lo detecta:** para cada columna, *«¿en el momento exacto en que hay que decidir, ya tengo
este dato?»*. Una columna puede traer la respuesta de forma obvia o disfrazada: un resultado posterior, un
dato que se carga **después**, algo calculado con información del futuro.

### Ejemplo resuelto: detección de fraude

Un banco quiere predecir si una transacción con tarjeta es fraudulenta **en el momento en que se intenta
pagar**, para aprobarla o frenarla. Columnas del dataset:

| Columna | ¿Se conoce al decidir? |
|---|---|
| `monto` | Sí, es lo que se está intentando pagar |
| `pais_comercio` | Sí |
| `hora` | Sí |
| `cantidad_compras_ult_24h` | Sí, es historia de la tarjeta |
| `reclamo_del_cliente` | **No:** el cliente reclama días después, *cuando ya vio el cargo* |

`reclamo_del_cliente` es casi una copia de la respuesta: casi todos los fraudes terminan en reclamo. El modelo
saca 99 % de recall en la prueba… y en producción, donde la columna está vacía en el momento de pagar, no
detecta casi nada. Ninguna métrica de la prueba lo hubiera dicho: **hay que razonar sobre el momento en que se
conoce cada dato**.

**Pistas de que hay fuga:** resultados «demasiado buenos»; una variable que domina todo lo demás; un nombre
o una descripción que habla de algo que pasa *después* o *durante* lo que queremos predecir.

> Ojo: dos columnas con nombres parecidos pueden ser una legítima y otra no. Lean qué mide cada una.

## 4. Separar datos de entrenamiento y de prueba (y el tiempo)

Para saber si el modelo sirve hay que probarlo con datos que **no vio**. Si los datos tienen **fechas** y el
modelo va a predecir el futuro, la separación tiene que respetar el tiempo: se entrena con lo viejo y se
prueba con lo nuevo. Si se mezclan al azar, el modelo «espía» el futuro a través de casos vecinos.

Si además van a elegir cosas (un umbral, un modelo), no las elijan mirando la prueba: reserven un tramo
aparte (**validación**) para decidir, y usen la prueba **una sola vez al final** para informar.

## 5. El umbral de decisión

Un modelo no dice «sí/no»: calcula una **probabilidad**, y nosotros decidimos desde qué valor decimos «sí».
Ese valor es el **umbral** (por defecto, 0,5).

- Umbral **bajo** → alerta fácil: sube el recall, bajan la precisión y el accuracy (más falsas alarmas).
- Umbral **alto** → alerta difícil: sube la precisión, baja el recall (se escapan casos).

No hay un umbral «correcto» en abstracto: depende del **costo de cada error**. Una forma de decidir es
asignarle un costo a cada tipo de error y elegir el umbral que minimiza el costo total.

```python
pred = (modelo.predict_proba(X)[:, 1] >= 0.30).astype(int)
```

### Continuación del ejemplo de la enfermedad rara

Con el umbral 0,5 el modelo marcaba 480 pacientes (80 enfermos). Si se baja a 0,2, marca 900 (95 enfermos):
el recall sube a 95 %, pero la precisión cae a ~10 %. Si cada estudio extra cuesta poco y un enfermo sin
detectar cuesta mucho, conviene el umbral bajo. Si los estudios extra son riesgosos o carísimos, no.

## Mini glosario

- **Variable / feature:** una columna de entrada. **Target:** lo que se predice.
- **Overfitting:** el modelo memoriza el entrenamiento y falla con casos nuevos.
- **Baseline:** la «solución tonta» contra la que hay que comparar (por ejemplo, «siempre digo no»).
- **Importancia de variables:** cuánto empeora el modelo si «desordenamos» una columna
  (`sklearn.inspection.permutation_importance`).
