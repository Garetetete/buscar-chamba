# Entrevista Manukora — guion

**Hoy, 1:00 p.m. Colombia / 11:00 a.m. Pacífico · 25 minutos · Nadeem Munshi**

Léelo en voz alta un par de veces. **No lo tengas abierto durante la llamada** — se nota. La idea
es reconocer la pregunta, no recitar. **Respuestas de 60 a 90 segundos.**

---

# HOJA DE CIFRAS — para no titubear con un número

| Dato | Valor |
|---|---|
| Reposiciones recomendadas | **4** |
| Ingreso mensual que cubren | **$97.665** |
| Ítems de vigilancia | 2 · el mayor es MGO 263+ 500g con **$40.308/mes** |
| Capital inmovilizado en sobrestock | **$87.708** ($56.777 + $30.931) |
| SKU que se quiebran en ≤3 meses | 6 |
| Crecimiento de la demanda | **3,9% a 13,2%** mensual · nada cae |
| Pruebas | **77** · 12 requisitos · 18 commits |
| CI | 3 sistemas × 2 versiones de Python |
| Las 4 órdenes | 514+500g **650u** $34.316 · 850+500g **450u** $29.477 · Energy **750u** $17.396 · Recovery **800u** $16.476 |
| MGO 1700+ | solo stock **2,80** · stock+orden **4,13** · por fases **3,35** · objetivo **3** |
| Propolis | **1,20 meses** (~36 días) · piso 30 días → señalar, no reponer · crece **+40%** |
| Divergencia de canal | MGO 100+ · Shopify **+24**, Amazon **−16** |
| Costo Parte 2 | **< $75/mes**, la IA menos de $1 |

---

## Antes de empezar

*"Before we start — just so you know, English is my second language, so I might ask you to repeat
something."*

---

## 1 · "Tell me a bit about yourself."

I'm an electronics engineer, but I actually started out as a data analyst. I spent a year at
Btilink on a contract with Aera Energy, a US oil company — writing SQL against their Oracle
databases and building Tableau dashboards their operations teams used every day.

Two things from that year stuck with me. Every time I found something in the data, I'd question
whether it was actually real or whether I'd just written a query that looked right. And how you
present it matters as much as finding it — nobody acts on a number they don't understand.

My team lead there was really into AI tools and pushed me to learn them. That's what got me
started.

Then I moved into development. For the past year I've been building a multi-tenant SaaS platform
for AI document analysis — I designed it and built it on my own, end to end, and it's in
production now. That's where I learned what actually breaks when you run AI for real users. Same
instinct as before: don't trust the output, check it.

---

## 2 · "Why did you separate the deterministic Python from the model?"

**Casi segura. La elogió por escrito.**

Because I wanted the output to be checkable. If the model does the arithmetic, nobody can verify
the briefing without redoing the maths — and a wrong number inside a confident paragraph is worse
than no briefing at all.

So every figure is computed in tested Python, and the model only turns those figures into prose.
Two things fall out of that. The whole analysis runs with no API key, so it still works if the
model is unavailable. And I can check what the model returns against the computed values — if it
writes a number that isn't in the facts, the run retries once, then falls back to a deterministic
template rather than shipping something wrong.

---

## 3 · "Why didn't you use n8n?"

**Casi segura. Es su herramienta.**

n8n would be my choice for the orchestration — the maintained connectors, the schedule, the
retries, and a run history someone outside engineering can read. That's exactly what I proposed
in Part 2.

But Part 1 is business logic: a month-by-month inventory simulation, per-SKU policy exceptions,
and a check on the model's output. In n8n that becomes JavaScript inside code nodes — no unit
tests, no meaningful diffs. And the brief asked how I verified the maths, which I couldn't have
answered with a canvas.

So: n8n orchestrates, code decides.

**Y si suena a que lo evitas por no conocerlo, aclara:** to be clear, I'm not avoiding n8n out of
unfamiliarity — I've used it at work to integrate SolarWinds and Aranda with our .NET services.
This was a judgement about where the logic belongs, not about the tool.

---

## 4 · "What's your actual experience with n8n?"

**Ahora es una respuesta fuerte. Sistemas concretos, con nombre.**

I've used it at work to integrate systems that don't talk to each other natively — SolarWinds for
monitoring and Aranda for service management, wired into the .NET microservices we run. That's
exactly what n8n is good at: sitting between enterprise tools, handling the authentication and the
retries, and giving you a run history you can look at when something didn't fire.

Alongside that I've done BPMN orchestration in Camunda, so I've seen both the visual-workflow
approach and the code-first one.

What I'd add beyond the tool itself is the operational thinking: idempotency so a replayed webhook
doesn't double-count, backoff on retries, and alerting when a job silently doesn't run at all —
which is the failure mode nobody notices until someone asks why a report is missing.

---

## 5 · "Walk me through the cover calculation."

**Prueba técnica. Ten `sop/metrics.py` abierto en `simulate_cover`.**

Both obvious shortcuts are wrong, in opposite directions. Stock divided by demand ignores stock
already in transit. Stock plus units on order credits it as if it were on the shelf today. And
both assume demand stays flat, when everything in that range grows four to thirteen percent a
month.

So I walk it forward month by month: deduct projected demand, and credit an incoming order only in
the month it lands.

That changes an answer. MGO 1700+ reads 2.80 months on stock alone, against a three-month target —
so you'd reorder. Stock plus on-order reads 4.13, so you wouldn't, and it hides the risk. The
simulation says 3.35: no order due, but put it on the watch list. **The static calculation would
have triggered an unnecessary purchase order on the most expensive line you sell.**

---

## 6 · "How did you handle the data context rules?"

Five of the seven live in `policy.py`, declared and separate from the arithmetic, so every
exception is visible in one place and adding a rule never means editing a formula.

The target cover for MGO 1700+ isn't hard-coded — it's read from the CSV column, and there's a
test that the target actually drives the decision. Hard-coding two would have worked on this
extract and broken on the next one.

And `Order_Arrival_Months = 0` is a single condition in the loader: units on order **and** an
arrival month, both required.

**Si te aprieta ahí, la honestidad completa:** On this dataset it changes nothing, because all six
rows with a zero also have zero units on order. But the code would break on an extract where an
order exists with that marker, so I tested it with synthetic data that has that combination — the
naive formula returns 52 months of cover where the honest one returns under three.

---

## 7 · "You added a watch list we didn't ask for. Why?"

Because the SKU with the most revenue at stake in your data — MGO 263+ 500g, about forty thousand
dollars a month — wasn't in my recommendations at all. It clears its cover target today, so the
rule correctly excluded it.

But it has a one-month lead time and it runs out in June. An order placed after cover drops below
target is already late. Clearing the target today isn't the same as needing no decision.

Without that section, the briefing would have quietly omitted the biggest number in the range.

---

## 8 · "What was the hardest part?"

Deciding what not to trust. The brief said one thing and the data said another: the Bioactive
Blends supposedly launched mid-January, but the extract records December sales for all three. And
the brief warned about a SKU with high revenue and declining demand — nothing in that data
declines.

Both times the right answer was to report the mismatch and state my assumption, rather than
quietly picking one and moving on. That's a judgement call, not a coding problem.

---

## 9 · "How did you make sure it wasn't just summarising the spreadsheet?"

**Es la advertencia más fuerte del brief. Muy probable.**

By computing the things that turn a number into a decision, and handing those to the model already
resolved. A weak line says "cover is 1.99 months against a target of 2". Mine says "order 650
units by April, because it runs out in May and thirty-four thousand a month is at stake".

The difference is four computed fields the model couldn't have inferred from the CSV: the
quantity, the order-by date, the revenue at stake, and the ranking. **The reasoning quality came
from the design, not from the prompt.**

---

## 10 · "Someone comes to you with a vague request. What do you do?"

**Habilidad central del aviso.**

I ask what decision the output has to support, before choosing any tool. That comes from the
analyst year — I built dashboards nobody opened because I'd answered the question I was given
instead of the one behind it.

Concretely: who reads this, what do they do differently once they have it, and how will we know it
worked. Then I'd build the smallest version that answers that and put it in front of them before
making it robust. Most vague requests get specific fast once someone sees a first draft they can
react to.

---

## 11 · "Tell me about Part 2." / "How would the daily brief work?"

**No estaba en la versión anterior de este guion. Puede salir.**

One Slack DM a day, under 200 words, at most three things. If nothing crosses the materiality bar
it says so in one sentence — "nothing needs you today" is what makes the other days credible.

n8n pulls the previous complete day from Shopify, Amazon SP-API, Cin7, Klaviyo and Gorgias into a
Postgres table, with an idempotency key so a replayed webhook never double-counts. Then
deterministic detection compares each metric against an expected range built from eight weeks,
matched by day of week, so a normal Sunday dip never fires.

Candidates are classified into three kinds, because they're different questions: what changed
overnight, what's trending the wrong way over several days, and what needs a decision today
because it has a deadline. **The deadline ones lead even when the dollar value is smaller, because
the other two can wait a day.**

## 12 · "How would you handle the timezone problem?"

**Era la única restricción de diseño explícita. Casi seguro que sale.**

I wouldn't try to guess when he wakes up. Inferring location from IP is the creepy option, and a
learned model of his sleeping hours is the overbuilt one.

Instead: generate once and deliver on first contact. The brief is produced at a fixed data cutoff
and held. n8n listens to Slack's presence event and posts the moment he becomes active, wherever
he is. If he hasn't appeared by a configurable hour — say eleven in whatever timezone his Google
Calendar reports, which travels with him — it sends anyway.

And if something material lands after it's sent, we edit that same message rather than pinging
twice. One message a day, always in the same place. **It uses signals he already emits, not new
surveillance.**

---

## 13 · "Can you show me?" — el plan de demostración

**Solo dos comandos. Cuatro segundos. No puede fallar.**

```powershell
cd "c:\Users\Dell\Desktop\Looker y Liscitaciones\BuscarChamba\manukora-sop-briefing"
python -m sop.cli --template-only
python -m pytest
```

**No corras la versión con el modelo en vivo** — tarda 20 a 40 segundos, depende de la red, y
sobrescribe el artefacto commiteado. Si quieres mostrar esa salida, abre el archivo ya commiteado.

**Si pregunta por las dos versiones del briefing:** the model version reads better — it connects
things, like noticing we face stockouts while sitting on excess inventory. But both contain
exactly the same figures, because the model never calculates. The template is a complete second
path, not a stub.

⚠️ **Sábelo:** el modelo **omitió la sección Watch list** en su versión. El contenido está en "What
is at risk", y la sección completa está en la versión de plantilla. Si sale: *"the model drops
sections sometimes — that's exactly why the things it can't be trusted to remember are guaranteed
in code."*

---

## 14 · "So what did the briefing actually say?"

**La versión de 30 segundos de su propia pregunta de negocio.**

Everything grew — three point nine to thirteen percent a month, nothing declined. Six SKUs run out
within three months, with about ninety-eight thousand dollars of monthly revenue behind the four
orders I recommended. Plus eighty-eight thousand of capital tied up in overstock, which is a
different kind of risk.

And the least obvious finding: the SKU with the most revenue at stake doesn't need an order today,
but it does need a decision before your next meeting.

---

## 15 · "How did you use AI? How long did it take?"

About a day of work. Claude Code throughout — specification first, implement against it, generate
test cases for edge conditions, audit the docs for claims that had drifted.

The prompt log documents six things that went wrong. Two were my own test assumptions being wrong
while the code was right. And one was my own README — the documented command didn't work from a
clean clone, because I'd been running with a path variable set in my shell. I only caught it by
cloning the published repo and following my own instructions. **The test suite had been green the
whole time.**

## 16 · "What would you improve next?"

Three things, in order.

Evaluation — I verify the numbers, but I don't measure whether the analysis surfaced the right
SKUs. A small labelled set plus recall would turn that from opinion into a number.

Second, the cover simulation holds demand flat past three months, which overstates long-horizon
cover. Documented, but real.

Third, I'd ask you for supplier minimum order quantities and unit costs. Right now I rank by
revenue because the extract has no margins — in a real S&OP meeting that would be the wrong basis.

---

## 17 · "Why Manukora?"

Two reasons. The role describes turning messy business requests into reliable systems, and that's
the part I'm actually good at — not just the AI side.

And the requirement about public GitHub work told me you evaluate what people have built rather
than what they claim. That works for me, because everything I say is readable.

Beyond that, this is AI applied to operations rather than a chatbot. The S&OP problem is a real
business decision with money attached, which is more interesting than another chat interface.

## 18 · "Why are you leaving your current job?"

**No hables mal. No reveles nada del contrato.**

I'm not unhappy — I built something I'm proud of and it's running in production. But I was the only
engineer on it, and I've learned as much as I can learn alone. I want people who'll push back on
my decisions.

And I want to keep going deeper into AI systems specifically, which is where this role points.

## 19 · Horario

Yes. I'm in Colombia, UTC-5, and we don't observe daylight saving — my offset never moves, so I'm
predictable year round. I can work 11 to 8 my time, which covers 9 to 6 Pacific. And my late
afternoon is your New Zealand team's next morning.

## 20 · Salario

**El aviso publicó USD 4.000–4.850, contractor por Deel. No inventes cifra.**

The posted range works for me. Since it's a contractor arrangement through Deel rather than
employment, I'd be looking at the upper half of it.

## 21 · Fecha de inicio — **solo si él pregunta**

I have a commitment with my current employer through the end of August, so September would be my
start date. Happy to do onboarding conversations before then.

**No lo saques tú. No expliques más.**

---

## 22 · "Any questions for me?" — elige tres, cierra con la última

1. *"Who's in AI & Systems today? Would I be the first engineer doing this, or joining people
   already building it?"*
2. *"You mentioned an internal AgentOS — how much exists today, and which piece would you want me
   on first?"*
3. *"How do you decide an automation is done? Is there a bar for 'reliable enough to leave
   running'?"* ← **la mejor: demuestra que piensas en mantenimiento**
4. *"How do requests reach the team — do stakeholders come to you directly, or is there a queue?"*
5. *"What does the rest of the process look like after this?"* ← **cierra con esta**

---

## Frases de emergencia

No entendiste → *"Sorry, could you repeat that?"* (una sola vez, sin disculparte dos veces)

Necesitas pensar → *"That's a good question, let me think for a second."*

No sabes → *"I haven't done that. What I have done that's closest is..."*

Te trabaste → *"Let me start that again."*

Pregunta que no preparaste → describe **cómo lo averiguarías**, no inventes. *"I'd start by..."*

---

## Antes de la 1:00 p.m.

- [ ] ¿Llegó el enlace? Si no, escribirle **ya**
- [ ] Cámara, micrófono, conexión probados
- [ ] `Win + Ctrl + L` probado con el paquete de inglés instalado
- [ ] Terminal ya con el `cd` hecho en la carpeta del proyecto
- [ ] Pestañas: README en GitHub · `sop/metrics.py` · el briefing generado
- [ ] Comer liviano antes
- [ ] Fondo ordenado, luz de frente, audífonos
