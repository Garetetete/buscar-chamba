# WarriorBabe — AI Automation Specialist · cuestionario de candidato (5 nov 2026)

Invitación de John Gibson (Rippling) del 5 nov, corregida el 6 nov (decía Analytics Engineer por error). Postuló el 2 nov.
Formato: 20–30 min de preguntas escritas + video de 2–4 min (el enlace va dentro del formulario). Escenarios hipotéticos: declarar supuestos y qué información pediría. IA permitida, con nota de dónde ayudó y cómo se verificó.

## About you

- **Full name:** Saúl Córdoba
- **Email:** sauleduardo1111@gmail.com
- **Time zone and overlap with ET:**

> Colombia, UTC−5 all year (no daylight saving). That's the same clock as Eastern Time from November to March and one hour behind it from March to November. I can work standard Eastern business hours, 9 a.m. to 5 p.m. ET, all year round.

- **Portfolio / work sample:**

> https://garetetete.github.io · https://github.com/Garetetete/manukora-sop-briefing (Python pipeline where an LLM writes an executive briefing and a guard checks every figure against the computed data before it ships: one corrective retry, then fallback to a template; 77 tests in CI).

## Your experience

### AI agent you personally built

> A personal project from October 2026: an autonomous agent that plays a live web strategy game around the clock. The repo is private because it holds real account data. (At work I also run AI in production, in a multi-tenant SaaS platform for document analysis, but that one is confidential.)
>
> **Problem.** The game rewards well-timed decisions every few minutes, like what to build, when to defend and how to spend resources. A person can't keep that up.
>
> **How it works.** It has two layers:
> 1. **A deterministic Python rules engine** runs every 2–10 minutes and does the safe, repetitive work: a phased build queue, resource reserves and attack detection.
> 2. **A "brain" on the Claude API** sets the strategy the engine follows. It is a hand-written agent loop: up to 8 turns, with 15 tools defined by strict JSON schemas (read state, set strategy, game actions, alerts). Every action the model proposes is validated against the real game state before it runs. Each call is capped at 5 actions, and a dry-run mode lets me watch decisions without executing them. Tool errors go back to the model as messages instead of crashing the process. The brain wakes on events, like an incoming attack or a stalled plan, with cooldowns between runs. A daily retrospective with structured output writes lessons back into its notes.
>
> **Tools:** Python, Claude API (anthropic SDK), Playwright for login and then plain HTTP (httpx, GraphQL, REST) with BeautifulSoup, Docker Compose, and pytest.
>
> **What I implemented:** the architecture, the tool schemas and the validation layer, the event triggers, and the supervisor (exponential backoff, single-instance lock, heartbeat). I also built the test suite. I worked with Claude Code as a pair programmer and reviewed every change.
>
> **Testing:** 59 offline pytest tests run against real HTML pages captured from the game. Before letting the agent act, I ran it in dry-run mode.
>
> **Challenges:**
> - **Actions that sound right but can't happen.** A model can confidently propose something the current state doesn't allow, like not enough resources or a slot that's already busy. I didn't trust its judgment for that. Every tool call passes a validator against live state, and the validator returns a precise error the model can correct from, so invalid actions never reach the game.
> - **Self-updates breaking the running agent.** The agent can request changes to its own code. Those are applied by Claude Code running headless in an isolated git worktree. Tests must pass before the merge, and if the new version doesn't report a healthy heartbeat within 25 minutes, the change is reverted automatically.
> - **Cost.** The 720-line playbook sits behind one-hour prompt caching, and reviews run every 55 minutes to reuse the cache. A call costs about half a cent.

### Production n8n workflow

Datos de Saúl (7 nov): webhook de SolarWinds → reglas que deciden si se registra y qué tipo de alerta → consulta al servicio interno (fuente de verdad, alimenta un dashboard) → crea ticket en Aranda o actualiza el existente. **Supuesto sin confirmar:** el monitoreo con el historial de ejecuciones de n8n y volver a correr las fallidas. También falta confirmar si lo construyó él solo.

> **Context.** At work, for an insurance client, our team built an n8n workflow that turned infrastructure alerts into service-desk tickets without creating duplicates. I helped in every phase, from the design to getting it running.
>
> **Trigger.** A webhook that received alerts from SolarWinds: server, database and other infrastructure metrics.
>
> **Connected systems:**
> - SolarWinds, which sends the alerts.
> - n8n, which runs the workflow.
> - Aranda Service Desk, where the tickets live.
> - An internal service our team built. It was the source of truth: it stored every alert and ticket and fed a monitoring dashboard.
>
> **Main steps:**
> 1. Receive the SolarWinds payload on the webhook and normalize it.
> 2. Apply business rules to decide whether the alert should be registered at all and what type of alert it is, so noise doesn't become tickets.
> 3. Query our internal service to check whether a ticket already exists for that alert.
> 4. If none exists, create a ticket in Aranda with the ticket number, severity and everything SolarWinds sent, and record it in our service.
> 5. If one already exists, update that ticket instead of opening a new one.
>
> **Monitoring and recovery.** Failed runs showed up in n8n's execution history with the exact node and payload that failed. I fixed the cause and re-ran them. Re-running was safe by design: monitoring tools repeat alerts while a problem persists, and the workflow always checked the source of truth before acting. A repeated or reprocessed alert updated the existing ticket instead of opening a duplicate, and the dashboard always matched the tickets.

### Nota de uso de IA (si el formulario la pide en un campo, o al final de la última respuesta)

> AI use: I used Claude to structure and tighten my written answers. Every technical detail comes from my own projects, and I checked each one against my code and notes before submitting.

## Versiones cortas (las que se envían; 7 nov)

### AI agent

> A personal agent that plays a live web strategy game 24/7 (private repo: it holds real account data). A Python rules engine handles routine moves every few minutes. A "brain" on the Claude API sets strategy through a hand-written agent loop with 15 strict-schema tools.
>
> What I implemented: the architecture, the tools, and a validation layer that checks every proposed action against the live game state before it runs. I also wrote a supervisor with retries and a heartbeat.
>
> Testing: 59 pytest tests against real captured pages, plus a dry-run mode.
>
> Main challenge: the model sometimes proposed actions the state didn't allow. Instead of trusting it, invalid actions are rejected with a precise error the model corrects from, so they never reach the game.
>
> Tools: Python, Claude API, Playwright/httpx, Docker, pytest.

### n8n workflow

> Built with my team for an insurance client, and I helped in every phase: a webhook received SolarWinds alerts (servers, databases). Business rules decided whether to register each alert and its type. The workflow then checked our internal service, which was the source of truth and fed a dashboard, for an existing ticket. If there was none, it created one in Aranda Service Desk with severity and details; if there was one, it updated it.
>
> Monitoring: failed runs showed up in n8n's execution history, and I fixed the cause and re-ran them. Re-running was safe because the workflow always checked the source of truth first, so repeated alerts never created duplicate tickets.
