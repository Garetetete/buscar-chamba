# Prueba práctica — AI Automation Engineer @ Manukora

> ⚠️ **Este archivo es privado y NO va dentro del repositorio entregable.** Contiene análisis de
> estrategia y de las trampas del brief; que un revisor lo lea sería pésimo. Vive en
> `BuscarChamba/`, el repo vive en `BuscarChamba/manukora-sop-briefing/`. **Está en español a
> propósito**, como cortafuegos: todo lo del repo va en inglés, así un archivo en español ahí
> dentro salta a la vista.

---

## Estado

- **Vacante:** AI Automation Engineer — Manukora · Remoto (Sudamérica) · **USD 4.000–4.850/mes**
  · nivel **Semi Senior** · contratación por **Deel**
- **Postulado:** 4 de agosto de 2026, cuando el aviso tenía **1 postulante**. Al 5 de agosto:
  **46**. Pasó a prueba práctica.
- **Plazo:** 48 horas calendario desde la recepción del brief.
- ⏰ **PRIMERA ACCIÓN PENDIENTE: pedir extensión de la ventana.** El brief lo ofrece
  explícitamente (*"if the timing is genuinely awkward, reply and we can agree on a better
  window"*). Tiene trabajo de tiempo completo. Entregar apurado cuesta más que pedir tiempo.

## Qué evalúan de verdad

Textual del brief: *"A polished narrative with no working system will not pass. A working system
with unclear reasoning will also be hard to assess."* Quieren **las dos cosas**.

Y sobre todo: *"A weak output says what the data already says. A strong output turns the data
into a decision."* El examen es de **criterio de negocio**, no de programación.

El uso de IA está **sancionado por ellos**: *"We expect you to use AI throughout. That is part of
what we are evaluating."*

---

## Números verificados (calculados, no estimados)

Demanda M4 = Shopify + Amazon (inventario común). Cobertura = stock / demanda M4.

| SKU | Dem. M4 | Cobertura | Objetivo | ¿Orden? | Ingreso/mes | Tendencia M1→M4 |
|---|---:|---:|---:|:--|---:|---:|
| MGO 100+ 250g | 1032 | 6,20 | 2 | sí (2000/1m) | $25.790 | +11,7% |
| MGO 263+ 250g | 1604 | 4,55 | 2 | sí (3200/1m) | $56.124 | +20,8% |
| **MGO 263+ 500g** | 684 | 2,49 | 2 | **NO** | $37.613 | +23,0% |
| MGO 514+ 250g | 940 | 3,62 | 2 | sí (1600/1m) | $46.991 | +23,7% |
| **MGO 514+ 500g** | 392 | **1,99** | 2 | **NO** | $31.356 | +30,7% |
| MGO 850+ 250g | 536 | 3,54 | 2 | sí (800/2m) | $37.515 | +21,8% |
| **MGO 850+ 500g** | 244 | **1,80** | 2 | **NO** | $26.838 | +32,6% |
| **MGO 1700+ 100g** | 300 | **2,80** | **3** | sí (400/2m) | $17.997 | +33,9% |
| Propolis 30ml | 168 | 1,37 | 2 | NO | $5.878 | +40,0% |
| Bioactive Immunity | 528 | 2,27 | 2 | sí (800/1m) | $21.115 | +37,5% |
| **Bioactive Energy** | 388 | **1,91** | 2 | **NO** | $15.516 | +42,6% |
| **Bioactive Recovery** | 364 | **1,68** | 2 | **NO** | $14.556 | +46,8% |

### ⚠️ CORRECCIÓN tras implementar la cobertura por fases (5 ago)

La tabla de arriba usa **cobertura estática** (`stock / demanda M4`), que es la que calculé
primero. Al simular mes a mes acreditando las órdenes en su mes de llegada, **dos casos cambian
de conclusión**:

- **MGO 1700+ 100g deja de necesitar reposición.** Estático da 2,80 contra objetivo 3 → parecía
  corto. Pero las 400 unidades llegan en el mes 2 y la cobertura real sube a **3,35**, por encima
  del objetivo. **El cálculo estático habría disparado una orden de compra innecesaria.** Es el
  mejor ejemplo de por qué el modelo por fases importa, y va al README.
- **MGO 263+ 500g baja de 2,49 a 2,22** porque la demanda crece. Sigue sobre el objetivo de 2, así
  que no se repone — pero queda como caso de vigilancia, con quiebre proyectado en junio.

**Lista final del motor (4 recomendaciones, ordenadas por ingreso en juego):**

| # | SKU | Unidades | Cobertura | Ingreso/mes |
|---|---|---:|---:|---:|
| 1 | MGO 514+ 500g | 650 | 1,75 | $34.316 |
| 2 | MGO 850+ 500g | 450 | 1,58 | $29.477 |
| 3 | Bioactive Energy | 750 | 1,62 | $17.396 |
| 4 | Bioactive Recovery | 800 | 1,42 | $16.476 |

### Reposición recomendada según cálculo estático inicial (superado por lo de arriba)
1. **MGO 514+ 500g** — 1,99 meses · $31.356/mes
2. **MGO 850+ 500g** — 1,80 meses · $26.838/mes
3. **Bioactive Energy** — 1,91 meses · $15.516/mes
4. **Bioactive Recovery** — 1,68 meses · $14.556/mes
5. **MGO 263+ 500g** — 2,49 meses, técnicamente sobre objetivo, **pero sin orden y creciendo
   23%**: cruza por debajo en ~1 mes. Recomendarlo *antes* de que sea urgente es pensar hacia
   adelante, que es exactamente lo que piden.

---

## Las cinco trampas del brief

1. **`Order_Arrival_Months = 0` significa que NO hay orden**, no que llega ya. Seis SKU. Un
   script ingenuo infla la cobertura. Es el fallo automático más probable.
2. **MGO 1700+ tiene objetivo de 3 meses**, no 2. Está en 2,80: sano contra 2, corto contra 3.
   Si el código usa un target fijo, reprueba.
3. **Propolis**: 1,37 meses ≈ **41 días**. La regla dice deprioritizar salvo bajo 30 días → **no
   reponer**, solo señalar. Tensión interesante: es **el SKU que más crece (+40%)** y lo
   descontinúan en Q2.
4. **Inventario común**: sumar Shopify + Amazon, no tratarlos por separado.
5. 🔑 **Contradicción en sus propios datos.** El brief dice que los Bioactive Blends lanzaron a
   **mediados de enero de 2026** (mitad de M2), pero la tabla muestra **ventas en M1 = diciembre
   de 2025** (232, 164, 152 en Shopify). **Detectarlo y declararlo en el README es probablemente
   el gesto de mayor puntaje disponible.** Sea error suyo o trampa deliberada, la respuesta es la
   misma: señalarlo, declarar el supuesto adoptado y seguir.

## Una advertencia suya que no aplica — y decirlo suma

El brief anticipa: *"si un SKU tiene alta oportunidad de ingreso pero la demanda claramente cae,
señala la tensión"*. **Ningún SKU cae.** Todos crecen entre +11,7% y +46,8%.

Las tensiones reales son otras dos:
- **Propolis**: el de mayor crecimiento del catálogo, y lo están matando.
- **MGO 100+ 250g**: líder de volumen con el crecimiento más lento, y **único caso de retroceso a
  nivel de canal** — Amazon cayó de 404 a 388 en M4 mientras Shopify subía. Huele a problema de
  listing o precio en Amazon. Ese tipo de inferencia es lo que piden cuando dicen "no resumas la
  hoja de cálculo".

**Consecuencia de diseño:** calcular cobertura con demanda M4 estática **subestima el riesgo**
porque todo crece. Proyectar M5 y M6 es de las mejores decisiones disponibles.

---

## Decisiones de arquitectura (tomadas el 5 de agosto)

| Pregunta | Decisión | Motivo |
|---|---|---|
| ¿Aplicación web? | **No.** CLI que lee CSV y escribe el briefing | El brief: *"a clean Python script is just as valid"*; el envoltorio no puntúa |
| ¿Docker? | **No.** Correr sin infraestructura y **sin API key** | El revisor quiere ejecutar en 30 s. Mejor: proveedor simulado + briefing ya commiteado. Se declara como tradeoff en el README |
| ¿SDD? | **Sí, ligero.** `SPEC.md` de una página, REQ numerados, un test por requisito | Piden tests y "algo inspeccionable". Da commits incrementales naturales |
| ¿Engram? | **No.** Es memoria local, no va en el entregable | En su lugar: `docs/prompt-log.md` commiteado por partes |
| ¿Lenguaje? | **Python** | Lo nombran, es su lenguaje más fuerte, pytest, datos tabulares |
| ¿n8n? | **No en la Parte 1. Sí en la Parte 2** | n8n no se testea ni se revisa bien como código. Demostrar criterio de n8n en la arquitectura del Morning Brief |

### 🔑 La decisión que sostiene todo

> **Separar la matemática del LLM.** Cobertura, proyección, ingreso y ranking en **Python puro,
> determinista y testeado**. El LLM recibe números **ya validados** y solo redacta la narrativa
> ejecutiva.

Da cuatro cosas: el modelo no puede alucinar cifras, la aritmética es verificable, el sistema
funciona aunque el modelo falle, y demuestra su propia consigna — *"AI as a system, not a chat
window"*. **Es la tesis del README.**

---

## Estructura del repo

```
manukora-sop-briefing/          (en BuscarChamba/, se sube a GitHub)
├─ README.md            enfoque, supuestos, tradeoffs, cómo correrlo, verificación
├─ SPEC.md              requisitos numerados, escritos ANTES del código
├─ data/mock_sales.csv
├─ output/sop-briefing-2026-03.md      el briefing generado, commiteado
├─ docs/
│   ├─ prompt-log.md    prompt v1 → mejorado → qué cambió → dónde falló la IA
│   ├─ assumptions.md   incluida la contradicción de Bioactive Blends
│   └─ part2-morning-intelligence-brief.md   500–800 palabras, arquitectura
├─ src/sop/
│   ├─ loader.py        lee y valida el CSV
│   ├─ metrics.py       cobertura, proyección, ingreso — puro, sin IA
│   ├─ rules.py         excepciones: target 3m, Propolis, orden=0
│   ├─ narrative.py     única capa que llama al LLM
│   └─ cli.py
└─ tests/               test_req_001_*.py … por requisito
```

**Todo el repo en inglés.** Este archivo de estrategia se queda fuera.

## Reparto de las 48 horas

| Bloque | Horas |
|---|---|
| SPEC.md y supuestos | 2 |
| Métricas y reglas con tests (**el corazón**) | 6 |
| Capa de narrativa con LLM | 3 |
| Briefing generado y revisado a mano | 2 |
| **Parte 2 — arquitectura, 500–800 palabras** | 3 |
| README y limpieza | 2 |

⚠️ **La Parte 2 no se deja para el final agotado.** Es escritura pura y pesa la mitad de la
evaluación.

## Estrategia del registro de prompts

Son **dos registros distintos**:

1. **Prompt del producto** — la instrucción que la automatización manda al modelo. v1 →
   mejorada → qué cambió. Nace al escribir `narrative.py`.
2. **Uso de IA en la construcción** — arranca **desde la fase de análisis**, no desde el primer
   commit. Esa fase (interrogar el brief contra los datos) es el mejor material que hay.

**No pegar transcripciones de chat**: piden el *stack de instrucciones* y el razonamiento. Un
volcado se lee como pensamiento subcontratado.

**Anotar en el momento, no reconstruir al final.** El historial de commits delata un log que
apareció de golpe.

**Hace falta al menos un ejemplo real de "dónde la IA se equivocó"** — es lo más difícil de
fingir y lo que más credibilidad da. Candidato natural: si el modelo interpreta
`Order_Arrival_Months = 0` como "llega inmediatamente".

---

## Recordatorios

- **Todo lo documentado hay que poder defenderlo hablando.** Verificar los números uno mismo
  antes de entregar; en la entrevista van a preguntar.
- **No incluir credenciales, API keys ni datos reales** (lo pide el brief explícitamente).
- **Exclusividad con SASOFTCO hasta el 30 de agosto de 2026** → si avanza, plantear **inicio en
  septiembre** cuando salga el tema de fechas, no antes.
- El NDA de SASOFTCO **no afecta esta prueba**: los datos son de Manukora y el código es nuevo.

## Pendientes inmediatos

1. ⏰ **Escribir a Manukora pidiendo la ventana de tiempo.**
2. Crear `BuscarChamba/manukora-sop-briefing/` e inicializar git.
3. Escribir `SPEC.md` con los requisitos numerados.
