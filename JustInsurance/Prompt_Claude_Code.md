# Prompt para Claude Code — ejercicio JustInsurance

> Pegar todo lo que está entre las líneas `=====` como primer mensaje, **después** de: descargar
> el paquete, descomprimirlo en una carpeta propia y leer tú mismo el README.md. Abrir Claude Code
> dentro de esa carpeta.

=====

You are my pair-engineer for an unpaid take-home exercise from JustInsurance, a US
insurance-licensing education company. I am Saúl, the candidate. Talk to me in **Spanish**;
everything that goes into the repository (code, comments, commits, docs) is in **English**.

## Rules

1. **The starter's README.md is the source of truth.** Where this prompt and the README disagree,
   the README wins; tell me about the conflict.
2. **Time is reported honestly.** Their cap is three hours of active work, including tests and the
   handoff. Run `date` when we start and at each phase boundary and append it to
   `docs/TIME_LOG.md` (phase, start, end). If I pause, I will tell you, and you log the pause.
   Never round the total down.
3. **I must be able to explain and change every line live.** Selected finalists get a 45-minute
   walkthrough plus a small change. Keep diffs small and readable, keep the existing stack, style
   and test runner, and add no new framework or dependency unless the README allows it and I
   approve. After each change, explain it to me in 3–4 lines of Spanish, including any TypeScript
   idiom I may not know.
4. **They want an engineer who reviews AI output, not one who only prompts.** Write the failing
   test first, then the fix. Never weaken or delete a test to make it pass; if you think a test
   is wrong, prove it to me first. Tell me when you are unsure instead of guessing.
5. No secrets, no real customer data, no network calls beyond what the starter does, no code from
   any previous employer.
6. **Comments: few, and only the "why".** Match the starter's comment density. Add a short
   comment only where a reader would otherwise "fix" something into a bug: why the insert is
   atomic, why a timeout becomes `uncertain` and not `failed`, why takeover is checked at send
   time. No comments that narrate what the code does, no banners, no commented-out code, and no
   JSDoc on every function. Over-commented code reads as unreviewed AI output, which is exactly
   what they screen for.
7. Keep `docs/AI_USE.md` **as we go, not at the end**: each time you or a subagent proposed
   something wrong that a test, a review or I caught, add one line: what was proposed, how it was
   caught, what we did instead.

## Git

My machine is already set up; do not reconfigure anything:
- Windows 11, Git Bash. git 2.47, `user.name` = Garetetete, `user.email` already set,
  `core.autocrlf=true` (leave it). No default branch configured, so use `git init -b main`.
- GitHub CLI 2.100 is logged in as **Garetetete** over HTTPS (scopes `repo`, `read:org`, `gist`).
  No login, token or SSH setup is needed.
- Node 22.20, npm 10.9, Python 3.12.

Steps:
- First thing: if the folder is not a git repo, `git init -b main` and commit the starter **exactly
  as received** ("Import starter project as received"). Every later change is then a reviewable
  diff against that commit. Make that commit **before installing anything**, so no
  `node_modules/` or build output gets in. If the starter has no `.gitignore` (or it misses
  `node_modules/`, build output or `.env`), add that in a separate second commit, so the import
  stays untouched.
- Small commits, one requirement each: imperative subject citing the REQ ID, a body that says
  **why**. No "feat:" prefixes. Commit when the work is done, not in batches at the end.
- Do not push anywhere until I say so. When I do, it goes to a **private** GitHub repo:
  `gh repo create Garetetete/justinsurance-support-desk --private --source . --remote origin --push`,
  then confirm with `gh repo view --json visibility`. Never public: the exercise is theirs. If the
  README asks for repository access, I will give you the reviewer's GitHub username and you run
  `gh api -X PUT repos/Garetetete/justinsurance-support-desk/collaborators/<username> -f permission=pull`.

## Context (background only; the code and README decide)

- The exercise is a small support inbox with a fictional messaging provider, synthetic data,
  local only. It covers five areas: **customer-data isolation, duplicate-message prevention,
  approval of the exact reply, uncertain delivery, and human takeover.** Full completion is not
  required; correct, well-tested work in priority order beats five half-done areas.
- Their real stack: Next.js on Vercel, a React/Vite dashboard with a Python backend, Absorb LMS,
  and GoHighLevel as CRM and messaging. The fictional provider probably mirrors GoHighLevel:
  webhooks carry an ID and are retried up to 12 times on non-2xx or timeout, the docs say to
  store processed IDs and process idempotently, to acknowledge fast and process asynchronously,
  and delivery status arrives later as `pending | delivered | failed | read`.

## The invariants I expect (adapt names to the starter)

1. **Isolation.** The customer/tenant comes from the authenticated context, never from the body,
   query string or a client-supplied ID. Every read and write is scoped. Another tenant's record
   answers exactly like a missing one. Tests seed **two tenants with data** and check both
   directions, because zero rows from an empty table proves nothing.
2. **Duplicates.** Inbound: dedupe on the provider's message/webhook ID with an atomic guarantee
   (unique constraint or atomic insert-if-absent), not check-then-insert, and test it with
   concurrent duplicates (`Promise.all` or equivalent). Outbound: one idempotency key per
   approved reply, reused on every retry, so a retry can never send twice.
3. **Exact approval.** Approval is bound to the exact content (a version or a hash of the body).
   Any edit after approval invalidates it. The sender sends the stored approved body byte for
   byte, never a regenerated or re-rendered one. Test: approve, edit, send → refused; approve,
   send → the provider received exactly the approved text.
4. **Uncertain delivery.** A timeout or ambiguous error after the request left is **neither** a
   failure **nor** a success: record an explicit uncertain state. Never auto-resend with a new
   key. Resolve by checking the provider's status or retrying with the same idempotency key, and
   surface what stays unresolved to a human. Test with a fake provider that accepts the message
   and then times out.
5. **Human takeover.** Once a human takes a conversation, the bot sends nothing more. Check it **at
   send time, atomically** (conditional update or transaction), not only when the draft is
   created, and invalidate pending bot drafts. Test the race: draft created → human takes over →
   send attempt is blocked.

Name tests after requirements (`REQ-003 ...` in the file or test name) so the mapping is obvious.
For the main trap in each area, add one **contrast test** that shows the naive version failing,
when it is cheap.

## Files we add (the starter's own structure stays untouched)

```
README.md            theirs; only add a short "Submission" pointer to HANDOFF.md if allowed
HANDOFF.md           reviewer's entry point: changes per REQ, how to run, remaining risks
docs/SPEC.md         5–8 REQs, one screen, plus "Out of scope — declared, not forgotten"
docs/AI_USE.md       tools, what was delegated, what I verified, where the AI was wrong
docs/TIME_LOG.md     phase, start, end, pauses, real total
<their test folder>/ one new test file per REQ, following their naming convention
```

## Code layout

**One send gate.** Every outbound message, from the bot or a human, a first try or a retry, goes
through a single function that checks, in order: tenant scope → conversation not taken over (for
bot sends) → approval matches the exact body → idempotency key → state transition. Other paths
may not call the provider directly. This is the design thesis to state in HANDOFF.md: the rules
live in one place, so they can't be skipped by a second code path.

**An explicit message state machine.** For example `draft → approved → sending → sent |
uncertain | failed`, plus `cancelled` for drafts invalidated by an edit or a takeover. Define the
allowed transitions once and reject the rest.

**Where it goes:** if the starter already has a domain/service/lib layer, put it there and follow
its conventions. Only if the rules are scattered across route handlers, extract the minimum needed
to make them testable without HTTP, for example:

```
<their src or lib>/inbox/
  send-gate.ts        the single outbound path described above
  message-state.ts    allowed transitions, pure, no I/O
  dedupe.ts           inbound and outbound idempotency
```

Handlers, storage and the fake provider stay where they are and just call these. Do not
reorganize anything else: a large move makes the diff unreadable and is a bad trade inside the
time cap. If the starter is not TypeScript, use the same idea with its language's conventions.

## How to work

**Phase 0 — recon. Launch these three subagents in parallel, read-only:**
- *Mapper:* project layout, entry points, data model and storage, the fake provider, how
  tenant/auth context flows, and the exact commands to install, run and test. Under 300 words.
- *Brief-vs-code auditor:* read README.md against the code. For each of the five areas, say what
  exists, what is missing, and anything that looks deliberately broken (planted bugs, TODOs,
  misleading names, contradictions between README and code). Quote file:line. Under 400 words.
- *Baseline:* install and run the existing tests and the app exactly as the README says. Report
  what passes, what fails and why, with verbatim errors.

Then write `docs/SPEC.md` from their findings: one REQ per area, plus one per planted bug worth
fixing, in priority order. Keep it to one screen. Show it to me; I will answer quickly. Commit it.

**Phase 1 — build.** Default order unless the README says otherwise: isolation, duplicates, exact
approval, takeover, uncertain delivery. For each REQ: failing test → minimal fix → full suite
green → commit → explain it to me. While you implement one REQ, you may run **one** subagent that
writes the failing tests for the next REQ, touching only its own new test file. Never run
parallel agents that edit the same source files.

**Phase 2 — independent review.** Launch one fresh subagent that did not write the code. Give it
`git diff <import-commit>..HEAD` and the five invariants, not our reasoning. Ask for real defects
only: races, unscoped queries, paths where a duplicate, an unapproved or a post-takeover message
can still go out, and tests that would still pass with the bug present. Fix what is critical;
list the rest as remaining risks. Log what it caught in `docs/AI_USE.md`.

**Phase 3 — handoff.**
- `HANDOFF.md`: what changed and why (short section per REQ), how to run the tests, **remaining
  risks and unfinished work** (honest and specific), and decisions I would discuss with the tech
  lead.
- `docs/AI_USE.md` final pass and `docs/TIME_LOG.md` closed with the real total.
- Clean-clone check: clone the repo into a fresh folder, follow the README's commands literally,
  and confirm the tests pass there.
- Package or share exactly as the README asks.

Start now: set up git as described, log the start time, then launch the three recon subagents in
parallel.

=====

## Si algo sale mal a mitad de camino

- **Si se está alargando:** quedarse con los primeros REQ bien hechos y declarar los demás como
  riesgos en `HANDOFF.md`, con el diseño en 3–4 líneas cada uno. Ellos dicen que no hace falta
  terminar todo.
- **Si Claude propone agregar una librería** (Redis, colas, otro ORM): decir que no, salvo que el
  README lo pida.
- **Si un test falla y Claude quiere cambiar el test:** pedirle que primero demuestre que el test
  está mal. Si estaba mal, anotarlo en `docs/AI_USE.md`; en Manukora eso fue de lo más valioso.
- **Si se cae Claude Code o se acaba el contexto:** decirle "Read docs/SPEC.md, docs/TIME_LOG.md,
  docs/AI_USE.md and git log, then continue from the next unfinished REQ".
