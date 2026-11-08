# WarriorBabe — video de presentación (2 a 4 min)

Meta: **~3:15**, unas 430 palabras. Cámara, y en la sección técnica ~40 s de pantalla con la
réplica sintética del flujo en n8n (ver `n8n_demo/README.md`, sección "Para el video").
Hablar como a un gerente: problema → qué hice → qué pasó. Sin jerga innecesaria.

## Antes de grabar

- Loom (o similar) en modo solo cámara. Luz de frente, fondo ordenado, audífonos con micrófono.
- Tener este guion abierto al lado de la cámara, pero contarlo, no leerlo palabra por palabra.
- Un ensayo con cronómetro. Si pasa de 3:45, recortar la sección 4, no la 3.
- El enlace del video va dentro del formulario. Dejarlo como "cualquiera con el enlace puede ver".

## Guion (en inglés)

### 0:00–0:35 · Quién soy y qué sistemas he operado

> Hi, I'm Saúl Córdoba, an electronics engineer and software developer based in Colombia.
>
> I started as a data analyst, building SQL reports and Power BI dashboards. For the last year
> I've been a developer at a software company. There, I built a multi-tenant SaaS platform for
> AI-powered document analysis, on my own and end to end. It's been in production since early
> 2026 with government and insurance clients. I also build automations in n8n that connect
> business systems.

### 0:35–1:40 · Ejemplo técnico: el flujo de n8n y la decisión de diseño

> Here's an automation that's very close to this role. An insurance client used SolarWinds to
> monitor servers and databases, and Aranda as their service desk. When something went wrong, a
> person had to turn the alert into a ticket by hand.
>
> Our team built an n8n workflow for that, and I helped in every phase, from the
> design to getting it running. SolarWinds sends the alert to a webhook. Business rules decide
> whether it deserves a ticket at all and what type of alert it is. Then the workflow either
> creates the ticket in Aranda or updates the one that already exists.
>
> The key design decision was where the truth lives. Monitoring tools repeat the same alert every
> few minutes while a problem lasts. If the workflow simply created a ticket each time, the team
> would drown in duplicates. So we kept our own service as the single source of truth, and the
> workflow always checks it before acting. That made it safe to re-run anything after a failure:
> the worst case is an update, never a duplicate. That service also fed the dashboard, so the
> dashboard always matched the service desk.

### 1:40–2:30 · Impacto en el negocio y lo que no pude medir

> On business impact: on the SaaS platform, the main business problem was the cost of AI per
> document. I reduced inference costs by more than fifty percent, comparing model spend before and
> after the changes, which made the product much cheaper to scale.
>
> On the n8n workflow, the outcome was one ticket per incident instead of a pile of repeats, and
> alerts that reached the service desk without anyone retyping them. What I couldn't measure is
> the time saved, because we never timed the manual process before automating it. That's the
> lesson I apply now: measure the baseline first, then build.

### 2:30–3:10 · Cómo uso la IA y cómo verifico lo que produce

> I use Claude every day, both inside products and as a coding partner through Claude Code. My
> rule is simple: verify, don't trust.
>
> In my own agent projects, the model proposes and the code checks: every action is validated
> against the real state before it runs. In a reporting project, the model only writes the prose,
> while every number is calculated in code and checked against the data before anything is sent.
> And when Claude writes code with me, I read every change, and nothing gets merged until the
> tests pass.

### 3:10–3:20 · Cierre

> I like building automations that people actually rely on, and I'd love to do that for the
> WarriorBabe teams. Thanks for watching.

## Confirmar antes de grabar

- **"comparing model spend before and after":** ¿así mediste la reducción de costos (factura del
  proveedor, costo por documento)? Si fue de otra forma, cambiar esa frase. **No explicar cómo
  se logró la reducción:** es confidencial.
- **El resultado del flujo de n8n** ("one ticket per incident… without anyone retyping them"):
  debe ser cierto tal cual. Si antes no lo hacían a mano, cambiarlo.
- **Flujo de n8n en equipo (confirmado 7 nov):** Saúl ayudó en todas las fases. Si preguntan qué
  hizo él, tener a mano un ejemplo concreto de cada fase (reglas, consulta a la fuente de verdad,
  integración con Aranda).

## No decir

- El nombre del producto, el dominio (licitaciones / contratación pública), qué hace cada agente,
  cómo se bajaron los costos, conteos internos.
- El nombre del juego. (Aquí se habla de "my own agent projects", sin entrar en el juego.)
- El nombre de la aseguradora.
