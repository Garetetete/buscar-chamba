# Manukora — qué construimos y por qué

Referencia para defender cada decisión. Números verificados el 12 de agosto:
**77 pruebas · 18 commits · 12 requisitos · 7 módulos · CI en 3 sistemas × 2 versiones de Python.**

---

## Fase 0 — leer el brief contra los datos, antes de escribir código

Fue la hora más valiosa y cambió el diseño tres veces.

**Encontramos que sus reglas contradicen su propia tabla.** El brief dice que los Bioactive Blends
lanzaron a mediados de enero (mitad de M2), pero el CSV registra ventas en diciembre para los tres.
Ambas cosas no pueden ser ciertas.

**Encontramos que la tensión que ellos anticipan no existe.** Piden señalar un SKU con alta
oportunidad de ingreso y demanda claramente cayendo. Ningún SKU cae: todos crecen entre 3,9% y
13,2% mensual.

**Y encontramos que la cobertura estática engaña.** Con la demanda creciendo así, dividir stock
entre demanda del último mes no describe el riesgo real.

**Por qué importa:** las tres son cosas que solo aparecen si contrastas el enunciado con los datos
en vez de tragarte el CSV. Es exactamente lo que el brief llamó *"turns the data into a decision"*.

---

## Decisión 1 · La tesis: la aritmética es Python determinista, el modelo solo redacta

**Qué:** cada cifra —cobertura, ingreso, cantidades, prioridad— se calcula en Python probado. El
modelo recibe números ya validados y su único trabajo es escribir prosa ejecutiva.

**Por qué:** si el modelo hace la aritmética, nadie puede verificar el briefing sin repetir las
cuentas. Y un número equivocado dentro de un párrafo seguro es peor que no tener briefing.

**Tres consecuencias, y son el argumento completo:**
- **Verificable** — cada cifra rastrea a una fórmula con prueba.
- **Funciona sin modelo** — el análisis corre sin API key ni red.
- **Degrada en vez de romperse** — si el modelo falla, sale el mismo briefing por plantilla.

**Es lo que Nadeem elogió por escrito.**

---

## Decisión 2 · La cobertura se simula, no se divide

**Qué:** se camina el stock mes a mes, descontando demanda proyectada y sumando las órdenes en
camino **solo en el mes en que llegan**.

**Por qué:** las dos fórmulas obvias fallan en direcciones opuestas.
- `stock / demanda` ignora el stock en tránsito.
- `(stock + en_orden) / demanda` lo acredita como si ya estuviera en bodega hoy.
- Y ambas asumen demanda plana cuando todo crece.

**El caso que lo demuestra — MGO 1700+ 100g:**

| Método | Resultado | Decisión |
|---|---|---|
| Solo stock: 840 / 300 | 2,80 meses | Reponer (objetivo es 3) |
| Stock + orden: 1240 / 300 | 4,13 meses | No reponer, y esconde el riesgo |
| **Simulación por fases** | **3,35 meses** | **No reponer, pero vigilar** |

Las 400 unidades llegan en el mes dos. **El cálculo estático habría disparado una orden de compra
innecesaria en la línea más cara del catálogo.** Está como prueba con nombre propio.

---

## Decisión 3 · Las cinco trampas del brief, tratadas como requisitos

No como comentarios: como cosas que el sistema **debe** hacer, cada una con su prueba.

| Trampa | Cómo la resolvimos |
|---|---|
| `Order_Arrival_Months = 0` significa **sin orden**, no llegada inmediata. Seis filas la tienen | `has_open_order` exige unidades **y** mes de llegada. Hay prueba de contraste: la fórmula ingenua da 52 meses donde la honesta da menos de 3 |
| MGO 1700+ tiene objetivo de **3 meses**, no 2 | El objetivo se lee por SKU del CSV. Una prueba verifica que el objetivo realmente cambia la decisión |
| Propolis se descontinúa: solo reponer si baja de 30 días | Está en 1,20 meses → **se señala, no se repone**. Política declarativa en `policy.py` |
| Bioactive: tendencia desde M2, no M1 | Ventana de tendencia por SKU |
| Inventario común | Demanda = Shopify + Amazon en todo cálculo |

---

## Decisión 4 · La proyección tiene techo de 3 meses

**Qué:** se proyecta con el crecimiento promedio propio de cada SKU, **máximo 3 meses**, y más allá
la demanda se mantiene plana en vez de componerse.

**Por qué:** cuatro observaciones no sostienen componer 13% mensual indefinidamente. A seis meses
daría 2,1× — una cifra que parece precisa y no lo es. **Reconocer dónde tu propio modelo deja de
ser confiable vale más que proyectar con seguridad falsa.**

**Y un hallazgo que vale citar:** el ranking por oportunidad de ingreso es **idéntico** con M4 fijo
o con proyección — las doce posiciones sin moverse. Así que la priorización es robusta al supuesto;
la proyección cambia *cuándo* algo es urgente, no *qué* importa más.

---

## Decisión 5 · La watch list — lo que agregamos sin que lo pidieran

**El problema que descubrimos:** el SKU con más ingreso en juego de todo el catálogo —MGO 263+
500g, **40.308 dólares al mes**— no aparecía en ninguna parte del briefing. Cumple su objetivo de
cobertura hoy, así que la regla lo excluía correctamente.

**Pero** tiene un mes de tiempo de entrega y se quiebra en junio. Una orden puesta después de que
la cobertura baje del objetivo **ya llega tarde**.

**La regla:** si la cobertura proyectada es menor que `objetivo + tiempo de entrega`, es un ítem de
vigilancia con fecha de decisión. Captura ese y MGO 1700+, que es justo el que solo se salva por el
stock en tránsito.

**Cumplir el objetivo hoy no es lo mismo que no necesitar decisión.**

---

## Decisión 6 · El guardián numérico

**Qué:** todo número en el texto que devuelve el modelo se compara contra el conjunto de cifras
calculadas. Si escribe una que no existe: **un reintento con corrección**, y si insiste, **cae a la
plantilla determinista**.

**Por qué:** "el modelo no debe inventar" es una intención. Esto lo hace mecánico.

**Dos bugs reales que tuvo el guardián**, y los encontraron las pruebas:
- La expresión regular se tragaba la coma final: `"April 2026, month 5"` leía `2026,` como número.
- Marcaba la salida del propio sistema: los nombres de SKU tienen dígitos (`MGO 514+ 500g`).

---

## Decisión 7 · Sobrestock — nació de una observación del modelo

En una corrida temprana el modelo comentó que MGO 100+ inmovilizaba capital de trabajo. Era una
inferencia justa, pero **el modelo la había hecho, no la había recibido**.

En vez de borrarla, la convertimos en **campo calculado**: stock por encima del doble del objetivo.
Resultado: **87.708 dólares** inmovilizados — 56.777 en MGO 100+ y 30.931 en MGO 263+ 250g.

El brief no lo pedía, pero pregunta *"qué está en riesgo"*, y capital dormido en bodega es un riesgo
de otro tipo.

---

## Decisión 8 · Python CLI, no n8n y no aplicación web

**Por qué no web:** el brief dice que un script limpio de Python vale igual. Un frontend sería
regalar horas en lo que dijeron que no puntúa.

**Por qué no n8n, que es su herramienta:** n8n gana en orquestación —conectores mantenidos,
calendario, reintentos, historial que alguien no técnico puede leer—, y así lo propusimos en la
Parte 2. Pero la Parte 1 es lógica de negocio: simulación mes a mes, excepciones por SKU, guardián
sobre la salida del modelo. En n8n eso queda como JavaScript dentro de nodos: sin pruebas
unitarias, sin diffs legibles. **Y pidieron explicar cómo verificamos la aritmética — un lienzo no
se puede testear.**

**La frase:** *n8n orquesta, Python decide.*

---

## Decisión 9 · Corre sin instalar nada, y sin Docker

**Por qué no Docker:** el revisor quiere ejecutar en treinta segundos, no esperar un build.

**Qué hicimos mejor:** el análisis corre **sin API key y sin red**, solo biblioteca estándar. Y el
briefing generado está **commiteado**, así que se puede evaluar sin ejecutar nada.

**Y hay una historia detrás.** El comando documentado en el README **no funcionaba** en un clon
limpio: yo venía corriendo con `PYTHONPATH=src` en mi terminal y nunca lo vi. Lo descubrimos
clonando el repo publicado y siguiendo nuestras propias instrucciones. **Las 77 pruebas estaban en
verde todo el tiempo** — ninguna prueba podía detectarlo. Movimos el paquete a la raíz.

Está documentado en el prompt log como el defecto que *"solo se encuentra usando el entregable como
lo usaría un extraño"*.

---

## Decisión 10 · Especificación antes del código

`SPEC.md` con **12 requisitos numerados**, escritos antes de una línea de código. Cada uno con
pruebas nombradas por requisito, en seis archivos. Así la traza spec → código → prueba es explícita.

Dijeron que *"las entregas fuertes suelen incluir pruebas o verificaciones"*, y esto además produce
**commits incrementales naturales** — 18, no uno gigante.

---

## Decisión 11 · CI en tres sistemas y dos versiones de Python

**Por qué:** porque este repositorio ya había fallado una vez por "funciona en mi máquina". Y volvió
a pasar: **el CI se puso rojo mientras el lint local estaba verde**, porque el CI instalaba una
versión más nueva de ruff con más reglas activas. Fijamos la versión exacta.

Ahora corre en Linux, macOS y Windows contra Python 3.11 y 3.12. La insignia en el README es lo
único del repositorio que no depende de que te crean.

---

## Decisión 12 · Multi-proveedor detrás de una interfaz de un método

Gemini por API key, Gemini por Vertex AI, Claude, GPT, o plantilla determinista. Se detecta según
la credencial presente.

**Por qué:** un revisor con clave de Anthropic no podía correr el camino del modelo. La abstracción
existía en el diseño y no en el código, **lo cual es peor que no tenerla** porque el README la
insinuaba. Si falta el SDK o la clave está mal, cae a la plantilla en vez de romperse.

---

## Decisión 13 · Diagramas como código, no imágenes

Mermaid dentro del README en vez de exportar de draw.io. **Un PNG se desactualiza en silencio**; un
bloque mermaid vive en el mismo commit que la arquitectura que describe.

---

## Decisión 14 · El prompt log documenta seis fallos, dos míos

Pidieron dónde ayudó la IA y dónde se equivocó. Los seis están escritos, incluidos:
- **Dos suposiciones mías de prueba equivocadas, con el código correcto** — entre ellas la de MGO
  1700+, donde el cálculo estático habría disparado la orden innecesaria.
- El comando del README que no corría en clon limpio.
- El modelo ignorando dos instrucciones explícitas (título y sección de método), resueltas en código.

**Tres de los seis los encontraron las pruebas, no la lectura del código.** Ese es el argumento de
por qué escribirlas.

---

## Parte 2 — Morning Intelligence Brief

**Qué:** un mensaje diario de Slack, menos de 200 palabras, con máximo tres cosas. Si nada cruza el
umbral, lo dice en una frase — *"hoy no necesitas nada"* es lo que hace creíbles los otros días.

**Fuentes:** Shopify, Amazon SP-API, **Cin7**, **Klaviyo** y **Gorgias** — los sistemas que su
propio aviso de empleo nombraba. Orquestado en **n8n**, que es su herramienta.

**Tres clases de señal, porque son preguntas distintas:**
- **Cambió anoche** — un período fuera del rango esperado.
- **Va en mala dirección** — deriva sostenida: tres días consecutivos, o pendiente negativa a 14
  días. Un bache que se recupera nunca llega al brief.
- **Necesita decisión hoy** — lo que tiene fecha límite. **Encabezan aunque valgan menos dinero**,
  porque las otras dos pueden esperar un día.

**El problema del horario, que era la pregunta trampa:** no adivinar cuándo despierta. Inferir por
IP es lo *creepy*; un modelo aprendido de sus horas de sueño es lo *sobreingenierado*. La solución:
**generar una vez y entregar al primer contacto** — se retiene el brief y se publica cuando el
ejecutivo aparece activo en Slack, con respaldo en la zona horaria de su Google Calendar, que viaja
con él. Si algo cambia después, **se edita el mensaje** en vez de mandar otro.

**Costo:** menos de **75 dólares al mes**, dominado por hosting. La IA cuesta menos de un dólar.

**Modo de falla que más importa:** datos parciales en silencio. Si el reporte de Amazon llega tarde,
el brief debe decir *"cifras de Amazon no disponibles"* en vez de reportar una caída del 30% que en
realidad es un archivo faltante.

---

## La respuesta a su pregunta de negocio

*"What changed, what is at risk, and what should we do next?"*

**Cambió:** todo creció, entre 3,9% y 13,2% mensual. Pero MGO 100+ es el líder de volumen y el más
lento, y **el único donde un canal retrocede** — Amazon cayó de 404 a 388 mientras Shopify subía.

**En riesgo:** seis SKU se quiebran en tres meses, con **97.665 dólares mensuales** detrás de las
acciones. Más **87.708 inmovilizados** en sobrestock.

**Qué hacer:** cuatro órdenes antes de abril, ordenadas por dinero en juego. Dos decisiones para
mayo. Y tres cosas que la máquina no decide sola: investigar Amazon en MGO 100+, reconsiderar la
descontinuación de Propolis —la línea que más crece—, y resolver la contradicción de fechas.
