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

## Escenarios (7 nov, a partir de las ideas de Saúl)

### Scenario 1: Design a knowledge-base agent

> **Finding information.** Connect the sources (Google Drive or any system with an API) and index them for RAG: split documents into chunks, store embeddings with metadata (source, owner, last-modified date), and retrieve the most relevant chunks for each question. The agent answers only from what it retrieved and cites the document for every claim.
>
> **Keeping it current.** A scheduled sync (or Drive change notifications) re-indexes edited files and removes deleted ones. When two sources conflict, the agent prefers the most recent or the owner-approved one, shows both, and flags the conflict to the document owner.
>
> **When there's no reliable answer.** It says so plainly ("I couldn't find this in the documentation") and never guesses. It hands the question to the right person with the context, and every unanswered question goes into a log that shows which docs are missing.
>
> **Assessing quality.** A test set of real questions with expected answers, written with the department, scored on correctness, citation accuracy and correct refusals. In production, thumbs up/down plus a weekly review of unanswered and low-rated questions.
>
> **Before launch,** I'd test the questions the docs do cover, the ones they don't (it must refuse), conflicting documents, a freshly edited document, and permissions, so nobody gets answers from documents they can't access.
>
> I built a version of this: https://github.com/Garetetete/rag-doc-assistant (RAG with verifiable citations that refuses to make things up).

### Scenario 2: Find and measure an opportunity

> **Understand first.** I'd sit with the people who do it and watch it once, then ask: how often does it happen, how long does each run take, how many people do it, and where do mistakes happen? What systems are involved, and do they have an API? What happens downstream when there's an error? Automation is worth it when time per run × frequency × people, plus the cost of errors, clearly exceeds the cost to build and maintain it.
>
> **Example.** Teachers in Colombia type every student's grades into the school platform by hand. A practical solution: the teacher takes a photo of the grade sheet, a vision model extracts each name and grade, and the teacher reviews a pre-filled table and approves it before anything is submitted. The model does the typing; the human still does the checking. Low-confidence readings are highlighted, and the original photo is stored for audit.
>
> **Baseline.** Before building, time the manual process for a week or two and count the corrections made after submission.
>
> **Measuring:**
> - **Time saved:** time per upload before vs. after (photo + review).
> - **Adoption:** the share of grade uploads that go through the bot, and who stops using it, and why.
> - **Problem solved:** fewer corrections after submission, and teachers saying the task no longer eats their week.
>
> **Assumptions:** the platform accepts uploads by API or form automation, and the sheets are readable. I'd validate both with a small pilot before scaling.

### Scenario 3: Partial failure, rate limit and duplicates in n8n

> **Investigate.** In the execution history, find the failed run and the exact node, then read the 429 response: which limit was hit, and is there a Retry-After header? Check whether several executions ran at the same time (a burst of events, or a manual re-run on top of an automatic retry). That usually explains both the rate limit and the duplicates.
>
> **Recover safely.** Don't re-run the whole workflow: the first write already succeeded. Check what each system actually holds for that event ID, then retry only the failed update once the rate limit resets.
>
> **Prevent duplicates.** Make every step idempotent with the event ID as the key: before creating, look it up; if it exists, update instead of insert (or use an upsert if the API supports it). That makes any re-run safe. My team used this exact pattern at work: an n8n flow that checked our source-of-truth service before creating or updating a ticket in Aranda.
>
> **Handle the rate limit.** Turn on Retry on Fail with increasing waits, respect Retry-After, and batch events with a Wait node when they come in bursts.
>
> **Verify.** Confirm both systems have exactly one matching record for the event ID. For bulk recoveries, run a reconciliation query that compares the two systems.
>
> **Monitoring and documentation.** An Error Trigger workflow that alerts the team with the event ID and the failed step, a final node that logs the outcome of every run, and a short runbook explaining how to recover a partial failure without creating duplicates.
