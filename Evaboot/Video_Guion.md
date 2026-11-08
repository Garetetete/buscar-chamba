# Evaboot — video de 5 minutos (cámara + pantalla, sin editar)

Proyecto: **manukora-sop-briefing** (público, Python). Se presenta como *agentic workflow*:
el modelo escribe → se verifica → se corrige solo → si insiste en inventar, se degrada a plantilla.

## Antes de grabar

- Cerrar Telegram, Gmail, WhatsApp y cualquier ventana de SASOFTCO. Nada de `.env` en pantalla.
- Abrir en VS Code la carpeta `manukora-sop-briefing` (no `buscar-chamba`).
- Pestañas listas: `README.md` (vista previa, con el diagrama), `sop/narrative.py` en
  `generate_briefing` (línea ~590) y en `allowed_numbers` (línea ~105), `docs/prompt-log.md`.
- Terminal en la carpeta del repo, letra grande. Probar una vez los comandos.
- Loom: modo "Screen + Cam", burbuja de cámara en una esquina que no tape código.
- Un ensayo con cronómetro. Si pasa de 5:15, recortar la sección 4, no la 3.

## Guion (en inglés)

### 0:00–0:20 · Intro (mirando a cámara)

> Hi, I'm Saúl, a full-stack and AI engineer from Colombia. This is a Python project that turns a
> monthly sales and inventory extract into a briefing an executive can read in five minutes. The
> interesting part isn't the prose — it's the loop that checks the model before anything ships.

### 0:20–1:30 · Architecture and why (README con el diagrama)

> The whole design rests on one rule: **arithmetic is deterministic Python, the model only writes
> prose.** `loader` validates and pools the channels, `metrics` computes trend, projection and
> stock cover, `rules` decides reorder quantity, timing and priority. All of that is tested and
> involves no model.
>
> What comes out is a set of computed facts — the only figures the model is allowed to state.
> Then `narrative.py` asks the model to write, and a numeric guard checks the result.
>
> Why this way: for an executive, a briefing that reads well and has one wrong number is worse
> than no briefing. My first version pasted the CSV into the prompt and asked the model to reason
> — it did the arithmetic itself and got figures wrong. So I took the math away from it.

### 1:30–2:50 · How I observe the agent and assess quality (código + terminal)

Mostrar `generate_briefing`:

> This is the loop. The model writes, `find_unsupported_numbers` extracts every number in the text
> and checks it against the computed set. If something isn't there, I retry once and the
> corrective prompt names the exact figures it invented. If it does it again, I fall back to a
> deterministic template. Every attempt is recorded in a warnings list, and the run reports which
> provider actually produced the briefing.

Correr:

```
python ..\buscar-chamba\BuilderBot\demo_guard.py
```

> Here are the three outcomes with a scripted model: an honest answer passes; a model that invents
> "$52,000" gets caught and corrects itself on the retry; and one that keeps lying gets replaced by
> the template. The briefing is always produced, and it's never wrong.

Correr:

```
python -m pytest -vv -k "invented or hallucin or degrades"
python -m pytest
```

> Those behaviours are pinned by tests — 77 in total, running in CI on three operating systems,
> with no API key, because the whole analysis works without a model. And the template version is
> committed next to the model version, so I can diff what the model adds.

### 2:50–3:55 · Problems and hardest parts (`allowed_numbers` + `prompt-log.md`)

> Three problems. First, the brief contradicted the data: launch dates in the instructions didn't
> match the sales extract. Instead of silently picking one, the pipeline reports the conflict,
> states the assumption and continues.
>
> Second, the guard had false positives. The same figure appears as 34316, 34,316 or 34,316.00;
> month numbers and years appear everywhere; product names like "MGO 514+" contain numbers. So
> `allowed_numbers` generates the legitimate formats of every figure, treats months and years as
> structural, and treats product codes as identifiers, not claims.
>
> Third — the hardest — was deciding what the model is *not* allowed to do. Each thing I moved out
> of the model made the output more boring to build and much easier to trust.

### 3:55–4:50 · What I learned and what I'm still figuring out (a cámara)

> What I learned: verify, don't trust; design the failure path first; and if the system runs
> without a model, you can actually test it.
>
> What I'm still figuring out: the guard checks that a number *exists* in the facts, not that it's
> attached to the right product — a model could swap two true figures and pass. The next step is
> checking claims as pairs, product plus figure. Second, numbers are easy to verify; prose quality
> isn't. I'd like a small rubric with an LLM judge, calibrated against my own ratings. And third,
> in production I'd want traces per run — retry rate, fallback rate, cost and latency — as metrics
> over time, something like Langfuse.

### 4:50–5:00 · Cierre

> That's the project — the repo is public, link in my application. Thanks for watching.

## No mostrar ni decir

- Nada de SASOFTCO más allá de lo permitido (no producto, no dominio, no receta de costos).
- No abrir la carpeta `buscar-chamba` en el editor ni `Postulaciones.md`.
- No mostrar el bot del juego.
