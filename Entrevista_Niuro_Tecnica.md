# Entrevista con IA — Niuro, Senior Full-Stack Integration Engineer

Preparación para las preguntas técnicas del tipo "ya que usas Python, ¿cómo harías…?". El cargo es de
**integraciones**, así que lo más probable es que pregunten por APIs de terceros, webhooks,
autenticación, fallos y rendimiento.

## Cómo responder cualquier pregunta técnica

Usa siempre la misma estructura, en 45 a 90 segundos:

1. **Reformula el problema en una frase** ("So the goal is to…"). Te da tiempo para pensar.
2. **Di el enfoque** en 2 o 3 pasos, con los nombres de las herramientas.
3. **Nombra un riesgo y cómo lo cubres** (fallos, duplicados, seguridad, escala).
4. **Cierra con cómo lo probarías o vigilarías.**
5. Si puedes, **conecta con algo que ya hiciste** ("I did something similar when…").

Si no sabes algo, no te inventes un dato. Di: *"I haven't used that directly, but this is how I would approach it…"* y aplica la estructura.

Frases útiles para ganar tiempo: *"Let me think about that for a second."* · *"There are two parts to this."* · *"The main risk here is…"*

---

## 1. Integraciones con APIs de terceros

**How would you consume a third-party API that is slow and sometimes fails?**

I'd wrap it in a small client class, using httpx with explicit timeouts, so the rest of the code never calls the API directly. I'd classify errors: timeouts, 429 and 5xx are retryable, while 4xx like 400 or 401 are not. Retryable errors get exponential backoff with jitter and a maximum number of attempts. I'd also cap concurrency with a semaphore so we don't overload them, and log every failure with a correlation ID. I did exactly this with the Gemini API: under batch load it returned 429 errors, and classifying errors plus backoff and a concurrency limit fixed it.

**How would you handle an API with rate limits?**

First I'd read the limits from the docs and the response headers, like Retry-After or X-RateLimit-Remaining. On the client side I'd limit concurrency with an asyncio semaphore, or use a token bucket if the limit is per second. When I get a 429, I'd respect Retry-After instead of retrying immediately. For high volume I'd move the calls to a queue with workers, so the limit is controlled in one place.

**How would you fetch all records from a paginated API?**

I'd write a generator that follows the pagination, using cursor or next-page tokens if the API supports them, and yields records page by page, so I never load everything into memory. Each page request goes through the same retry logic. If it's a long sync, I'd save the last cursor so the job can resume after a failure instead of starting over.

## 2. Webhooks

**How would you build a webhook receiver in Python?**

With FastAPI, I'd create an endpoint that first verifies the signature, usually an HMAC of the raw body with a shared secret, compared with hmac.compare_digest to avoid timing attacks. Then I'd store the event and return 200 quickly, and process it in a background worker, because the sender will retry if I take too long.

**What if the same webhook arrives twice?**

Webhooks are at-least-once, so duplicates are normal. I'd make processing idempotent: save the event ID with a unique constraint in the database, and if it already exists, skip it. For operations like payments, I'd also check the state before applying a change, so processing it twice has the same result as once. I handled this kind of thing with payment webhooks in a QR ticketing system.

**What if events arrive out of order?**

I'd rely on the timestamp or version in the event, and only apply an update if it's newer than what I have stored. Or, for critical data, I'd treat the webhook as a signal and fetch the current state from the provider's API.

## 3. Autenticación

**How would you integrate with an API that uses OAuth2?**

It depends on the flow. For server-to-server, I'd use client credentials: request a token, cache it until shortly before it expires, and refresh it automatically. For user access, the authorization code flow with PKCE. Secrets go in environment variables or a secret manager, never in code. I've worked with this using Keycloak as the identity provider, with OAuth2, OpenID Connect and JWT validation.

**How do you validate a JWT in an API?**

I'd verify the signature with the provider's public keys from the JWKS endpoint, cached, and check the expiration, the issuer and the audience. Then I'd read the claims I need, like the user ID, roles or tenant. In my platform a middleware did this on every request and also set the tenant for row-level security in PostgreSQL.

## 4. Datos y sincronización

**How would you sync data between two systems?**

First I'd decide the source of truth for each field. For the sync itself, I'd prefer incremental: use an updated_at timestamp or a change cursor, and only process what changed since the last run. I'd use upserts so re-running is safe, keep a log of what failed, and add a reconciliation job that compares counts or checksums to catch drift.

**How would you process a very large file, for example a 5 GB CSV?**

I wouldn't load it into memory. I'd read it in chunks, with the csv module line by line or pandas with chunksize, validate each row with Pydantic, and insert in batches, with COPY for PostgreSQL if possible. Invalid rows go to an error file with the reason, instead of failing the whole import. I did something similar with a government data pipeline, from CSV to PostgreSQL.

**How would you validate data coming from an external system?**

With Pydantic models: define the expected schema, let it validate types and required fields, and reject or quarantine what doesn't match. Never trust external data, even from a "reliable" partner. I use the same idea with LLM outputs: every response is validated against a JSON schema before it's used.

## 5. Rendimiento y concurrencia

**When would you use async, threads or processes in Python?**

Async is best for many concurrent I/O operations like API calls or database queries; that's what I use with FastAPI. Threads also work for I/O, especially with libraries that aren't async. For CPU-heavy work, like processing images or large calculations, I'd use processes, because the GIL prevents threads from running Python code in parallel.

**An endpoint is slow. How do you find out why?**

I'd measure first, not guess: check the logs and timings per step, then the database with EXPLAIN ANALYZE, which often shows a missing index or an N+1 query. If it's an external call, I'd add a timeout and maybe a cache with Redis. For Python code, a profiler like cProfile. I once found a silent problem with a vector index this way, using psql and EXPLAIN ANALYZE.

**How would you use Redis in an integration?**

For caching responses from slow APIs with a TTL, storing OAuth tokens until they expire, rate limiting with counters, and as a broker for a job queue like Celery or RQ. The key is defining when the cache is invalidated.

## 6. Background jobs y colas

**How would you run long tasks without blocking the API?**

The API receives the request, saves a job with status "pending" and returns a job ID immediately. A worker processes it, with Celery or a simple queue, and updates the status. The client can poll the status or receive progress through Server-Sent Events, which is what I used to stream progress of AI analysis in my platform.

## 7. Pruebas y calidad

**How do you test code that depends on an external API?**

Unit tests with the API mocked, for example with respx for httpx, including the error cases: timeouts, 429, malformed responses. I like a fake implementation behind an interface, so I can simulate failures on demand. Then a few integration tests against a sandbox or a real container. Everything runs in CI with pytest and ruff, and nothing merges if it fails.

**How do you make sure a production integration is healthy?**

Structured logs with correlation IDs, health checks, metrics like error rate and latency per provider, and alerts when they cross a threshold. In my platform I used Docker health checks with an autoheal container that restarts unhealthy services.

## 8. Python general (por si preguntan lo básico)

| Tema | Respuesta corta en inglés |
|---|---|
| Decorator | A function that wraps another to add behavior, like logging, retries or auth checks, without changing its code. |
| Context manager | An object used with `with` that guarantees cleanup, like closing a file or a DB session, even if there's an error. |
| Generator | A function with `yield` that produces values lazily, one at a time; ideal for large data or pagination. |
| List vs tuple | Lists are mutable; tuples are immutable and can be dictionary keys. |
| `is` vs `==` | `==` compares values; `is` compares identity, the same object in memory. |
| Mutable default argument | Never use `def f(x=[])`, because the list is shared between calls; use `None` and create it inside. |
| GIL | The lock that lets only one thread run Python bytecode at a time; it limits CPU parallelism with threads, not I/O. |
| Dependency management | Poetry or pip with a lock file, and virtual environments per project. |

## 9. Si preguntan por .NET o Angular (el cargo también los pide)

**.NET:** Clean Architecture with separate layers (domain, application, infrastructure, API), dependency injection, Entity Framework Core or ADO.NET for data, and HttpClient through IHttpClientFactory with Polly for retries.

**Angular:** components, services for API calls, RxJS for async streams, HTTP interceptors to attach the JWT and handle 401 errors globally, and guards to protect routes.

---

## Recordatorios

- Sueldo: **USD 3.800 al mes** (rango del aviso: 3.500–4.000). Disponibilidad: **inmediata**.
- Años: **unos 2 profesionales**. No inflarlo.
- Cláusula: plataforma = "multi-tenant SaaS platform for AI-powered document analysis". Nada de nombre, dominio ni receta de costos.
