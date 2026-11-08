# Respuestas de cribado — preguntas 11 a 15 (12 de septiembre de 2026)

> Formulario que pide 150–250 palabras por respuesta, con nombres reales de sistemas y
> herramientas. Cada borrador respeta el otrosí 003: **no** aparece el nombre del producto,
> el dominio de negocio, la receta de costos (kill-switch, caching de prompts, rotación
> multirregión, capa BYOK) ni la descomposición interna. El producto se nombra como
> *"our AI document-analysis SaaS platform"* y los clientes solo por sector.
>
> **Lo que está entre corchetes `[...]` es lo que solo tú sabes y hay que rellenar.** Lo que
> no está entre corchetes sale del perfil o de los repos públicos y es verificable.
>
> Conteo de palabras al final de cada respuesta (sin contar los corchetes rellenos).

---

## 11 — A production system that broke unexpectedly

**Opción A — historia completa y verificable (repo público `rag-doc-assistant`).** Es un
proyecto propio, no del trabajo, pero es real, está documentado en el README y en una prueba
de regresión, y responde las cinco preguntas con datos exactos. Usar si no tienes un
incidente del trabajo que puedas contar sin tocar la confidencialidad.

```
The system is rag-doc-assistant, a RAG service I built and run: FastAPI on PostgreSQL
with pgvector, a React front end, and Gemini for embeddings and generation. Users upload
documents, chunks are embedded, and questions are answered with citations.

The failure was silent. With three valid vectors in the table, a similarity search for
top_k=5 returned a single result. No error, no log line, HTTP 200. The symptom showed up
as answers that cited one chunk when the evidence was clearly spread across several.

I debugged it with psql against the running container: SELECT COUNT(*) on chunks versus
what ORDER BY embedding <=> query LIMIT 5 returned, then EXPLAIN ANALYZE, which showed
the IVFFlat index in use. Root cause: IVFFlat partitions vectors into lists and probes
only ivfflat.probes of them (1 by default), so with a small corpus most lists were empty
and neighbors were dropped. My 66 unit tests were green because the in-memory repository
computes cosine similarity by brute force and never touches the index.

Finding it took about [two hours], most of it spent doubting the application code before
questioning the index.

What I would do differently: never trust a vector index without a test against the real
database. I switched to HNSW, which has good recall from the first row, and added an
integration suite (pytest -m integration, run in CI against pgvector/pgvector:pg16) whose
first test asserts that search returns every neighbor requested. A badly chosen index
does not fail; it lies.
```
*(≈ 250 palabras — ajustar el `[two hours]` al tiempo real)*

**Opción B — incidente del trabajo.** Si tienes uno en la plataforma SaaS, esta es la
estructura, con lo que puedes decir sin problema: el sistema (FastAPI + PostgreSQL 15 con
RLS + Keycloak + 8 servicios en Docker Compose, en producción para clientes de gobierno y
seguros), el error concreto `[…]`, las herramientas (`docker compose logs`, los healthchecks,
el contenedor autoheal, `psql`, los logs con ID de correlación), el tiempo `[…]` y la
lección `[…]`. Candidatos que sugiere tu propio perfil: PDFs escaneados que no traían texto
(por eso existe la detección de escaneados), o documentos que un conversor no procesaba
(por eso hay conversor dual Aspose + LibreOffice). Solo si pasó de verdad.

---

## 12 — An API integration that broke in production

Borrador sobre la integración con la API de Gemini/Vertex AI. Todo lo que dice existe en
`rag-doc-assistant` (código público) y en la plataforma del trabajo, salvo los datos entre
corchetes. **Confirma que el incidente ocurrió así antes de enviarlo.**

```
The integration is the one between our AI document-analysis SaaS platform (FastAPI,
Python 3.11) and Gemini through the google-genai SDK on Vertex AI. The API embeds document
chunks and generates structured JSON analyses; a single document can mean dozens of calls,
and users run them in batches.

What went wrong: under batch load the SDK started raising 429 RESOURCE_EXHAUSTED and
occasional 503s. The first version treated every exception the same way, so a quota hit
[failed the whole batch / retried immediately and made the throttling worse], and the raw
SDK message, which includes project identifiers, reached the HTTP response.

The fix had four parts, all still in place. First, classify errors: a small function maps
the SDK exception to a domain ProviderError with a retryable flag, using markers such as
429, 500, 502, 503, 504, resource_exhausted and unavailable; 400s and auth errors are
never retried. Second, retry only retryable errors with exponential backoff plus jitter,
so parallel requests do not retry in lockstep. Third, an asyncio.Semaphore caps concurrent
calls (LLM_MAX_CONCURRENCY), and every call has a timeout. Fourth, the route layer returns
a generic 503 message and logs the real one with the request's correlation ID.

What the next person needs to know is written in the code and in .env.example: retries,
timeout and concurrency are environment variables, not constants; the retryable markers
live in one place; and the fake provider (LLM_PROVIDER=fake) lets you reproduce a failing
batch in the test suite without credentials by setting provider.fail_times.
```
*(≈ 245 palabras)*

---

## 13 — Telling someone something they didn't want to hear

**No hay material en tu perfil para esta, y no la voy a inventar.** Necesito de ti tres
datos y la redacto: (1) quién era y cuál era el problema, (2) cómo lo planteaste, (3) qué
pasó después. Lo que mejor funciona en estas preguntas es un problema técnico con
consecuencia de negocio, planteado con datos y con una alternativa en la mano.

Candidatos que se me ocurren desde lo que sé de ti, por si alguno es real:

- **Costo de inferencia.** Decirle a tu jefe que el análisis por documento salía más caro
  de lo que se podía cobrar, y proponer la reducción que terminó siendo del 50 %+. Se puede
  contar **sin** la receta: solo el problema, cómo lo mediste y el resultado.
- **Un plazo que no daba.** Alguna entrega de la plataforma o de los proyectos .NET/Angular
  para gobierno o seguros.
- **Dependencias de terceros.** Una decisión de licencia o de librería que no convenía.
- **En Btilink.** Un dashboard cuyos números contradecían lo que el cliente esperaba ver.

Estructura para 150–250 palabras cuando tengas el caso:

```
Context (2 sentences: the system, the person, why it mattered to them).
The problem, with the number that made it undeniable.
How I raised it: privately first, with the measurement and one alternative already costed.
What happened: the decision taken, and what it cost or saved.
One line on what I'd do differently.
```

---

## 14 — Name of a system you shipped and one technical decision

Aquí la cláusula pega de frente: el formulario pide el **nombre real** y el nombre interno
está prohibido. La salida honesta es decirlo, y luego dar el nombre de algo que sí puedes
nombrar. Esto suele jugar a favor: demuestra criterio con acuerdos de confidencialidad.

```
The product name is covered by a confidentiality clause in my contract, so I will describe
it rather than name it: it is a multi-tenant SaaS platform for AI-powered document
analysis that I designed and built solo, end to end, and that has been in production since
early 2026 for clients in the government and insurance sectors. Users upload documents;
specialized agents on Vertex AI / Gemini analyze them in parallel and return structured
results; progress streams over SSE. Stack: FastAPI (Python 3.11), SQLAlchemy 2.0 on
PostgreSQL 15, Keycloak, nginx, eight Docker Compose services, 120+ REST/SSE endpoints.

One decision I own: tenant isolation is enforced with PostgreSQL row-level security, not
with WHERE clauses in application code. A middleware resolves the tenant from the
Keycloak JWT and sets it as a session variable on the connection; every table with tenant
data has an RLS policy that filters on that variable. I chose it because the alternative,
remembering to add tenant_id = :tenant to every query, fails silently the first time
someone forgets, and in a product that holds contracts and insurance documents a single
missed filter is a data leak to another customer. RLS moves the guarantee from
discipline to the database: a query without the variable returns nothing. The cost was
real (per-request session setup, and admin jobs need an explicit bypass role), but you
pay it once instead of on every pull request.

If a public name helps: rag-doc-assistant (github.com/Garetetete), same interface-driven
design, 108 tests.
```
*(≈ 250 palabras — recorta la última frase si te pasas)*

⚠️ Verifica el detalle de la implementación de RLS (variable de sesión desde el middleware,
rol de bypass para trabajos administrativos): lo escribí a partir de "RLS inyectado por
middleware" del perfil. Si el mecanismo real es otro, cámbialo; no lo dejes si no es exacto.

---

## 15 — A production system where one agent coordinated other agents

Tienes dos sistemas multiagente: los agentes de la plataforma SaaS (en producción) y el
proyecto de coordinador + 6 agentes con Google ADK. **La cláusula prohíbe describir los
agentes por su función (legal, económica, financiera)**, así que van como "specialized
analysis agents". Las partes de memoria y de fallos llevan corchetes porque no tengo el
detalle real; **no las envíes sin confirmar cada una**.

```
Yes, in production: the analysis pipeline of our AI document-analysis SaaS platform, built
on Google ADK with Vertex AI / Gemini and running since early 2026.

Assignment and tracking. A coordinator receives a document and fans out to specialized
analysis agents running in parallel, each with its own prompt and a JSON schema enforced
through Gemini's structured output. Each result is a PostgreSQL row keyed by document and
agent with a status [pending / running / done / failed], so "what is left" is a query,
not in-memory state. Batches run under an asyncio.Semaphore; progress streams over SSE.

Shared state and context. Agents never talk to each other: they share the extracted text,
and the coordinator hands downstream agents the structured outputs of upstream ones, never
free text, so the contract between agents is a schema.

Memory. Short-term is the agent's prompt context for one document. Session is the
per-document chat, whose history is stored in PostgreSQL [and trimmed to the last N
turns]. Long-term is the results themselves, persisted per tenant under row-level security and
reused by later features (dashboards, document autofill) without re-running the models.

Failures. Transient errors are retried with exponential backoff; after that the agent's
row is marked failed, the others complete, and the document shows a partial result that
can be re-run for that agent alone [confirm].

Repeated actions and handoffs. [A completed agent row is never re-executed unless
explicitly requested; re-runs are keyed by document+agent, so a duplicate request is a
no-op. Confirm the real mechanism.]
```
*(≈ 250 palabras con los corchetes rellenos; si algo no existe, quítalo y di que no lo
resolviste, que es exactamente lo que el formulario pide)*

---

## Antes de enviar

1. Rellenar los corchetes con datos reales. Si un dato no existe, quitar la frase.
2. Pasar el contador de palabras del propio formulario: el límite es por respuesta.
3. Releer con la lista prohibida al lado: nombre del producto, dominio, kill-switch,
   caching de prompts, rotación multirregión, capa BYOK, número de routers/tablas/migraciones.
