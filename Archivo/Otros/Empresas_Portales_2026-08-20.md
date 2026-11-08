# Portales propios de empresas — 20 de agosto de 2026

> Cuarto canal, y el que tiene mejor perfil de todos: **las empresas publican en su propio sistema
> de contratación, sin contador de postulantes y sin intermediario.** Es el mismo perfil que las
> vacantes por correo directo — el único formato donde le ha ido bien.

## Cómo se leen estos tableros

Muchas empresas usan Greenhouse, Lever o Ashby, y **los tres exponen la lista completa en JSON
público**, sin autenticación:

```bash
https://boards-api.greenhouse.io/v1/boards/<empresa>/jobs?content=false
https://boards-api.greenhouse.io/v1/boards/<empresa>/jobs/<id>   # detalle
https://api.lever.co/v0/postings/<empresa>?mode=json
https://api.ashbyhq.com/posting-api/job-board/<empresa>
```

De 12 empresas probadas respondieron dos: **Truelogic** (Ashby, **156 vacantes**) y **Wizeline**
(Greenhouse, 35). Las demás usan portales cerrados o slugs distintos.

---

# 🏆 Wizeline — cinco vacantes solo para Colombia

Consultora mexicana grande, ya estaba en la lista de 20 empresas 100% remotas del canal de Telegram.

## Senior AI Engineer (Python Advanced) — Colombia
https://www.wizeline.ai/careers/job?gh_jid=7306267

**Los requisitos son su stack literal, y no piden años:**

| Piden | Él tiene |
|---|---|
| **Python backend con FastAPI** y entendimiento profundo de **ASGI** | ✅ FastAPI + Uvicorn a diario |
| **LLMs, frameworks de agentes IA, prompt engineering aplicado** | ✅ |
| **Pruebas unitarias y de integración desde el día uno** | ✅ 77 tests con CI |
| **CI/CD con GitHub Actions** | ✅ |
| AWS (DynamoDB, ECS, IAM) | ⚠️ solo IAM |
| Deseable: manejo de herramientas de IA en el día a día | ✅ |

**A diferencia de las otras dos de Wizeline, esta no lista requisito de años.** Dice Senior en el
título, pero la lista de skills no pone la barrera. Es el vacío más pequeño de todo lo que hemos
visto: solo AWS.

## Senior AI Agent Engineer — Colombia
https://www.wizeline.ai/careers/job?gh_jid=8139378

**Inglés B2 avanzado o C1** — es la primera que acepta B2 explícitamente. LLM con **GPT, Claude o
Gemini**, prompt engineering, function/tool calling y evaluación. RAG con pipelines de embeddings y
búsqueda semántica. Orquestación de agentes con LangChain/LangGraph/CrewAI. Deseables: **SSE o
WebSockets** ✅ y **MCP**.

⚠️ Pide **5+ años**. Pero el inglés B2 baja una barrera que casi todas las demás ponen en C1.

## Las otras tres de Colombia

- **Senior AI Engineer** · https://www.wizeline.ai/careers/job?gh_jid=6566944 — 5+ años en IA/ML y **AWS Bedrock**. ❌ AWS es el vacío
- **Staff Backend Engineer (GraphQL / AWS / Python)** · https://www.wizeline.ai/careers/job?gh_jid=7939095 — nivel Staff
- **Fullstack Software Engineer - React & Node** · https://www.wizeline.ai/careers/job?gh_jid=7264950

---

# 🥈 Truelogic — 156 vacantes, todas LatAm remoto

Ya había aparecido tres veces en los barridos de LinkedIn. Su tablero completo tiene mucho más.

## Semi-Senior Full Stack Engineer (Python / React) — E-learning · 11 ago
https://jobs.ashbyhq.com/truelogic/ce6df8e4-2b60-4f58-b22e-271615e271b0

**Dice Semi-Senior**, que es su nivel declarado, y aun así pide experiencia con IA generativa:

- 3+ años con Python y React
- APIs REST y arquitecturas de microservicios ✅
- Nube (AWS preferido), CI/CD y despliegues en contenedores ✅ Docker
- **Experiencia previa con aplicaciones GenAI/LLM, prompt engineering, integración de modelos** ✅

Ofrecen "pago muy competitivo en USD" y trabajo con empresas de EE. UU. ⚠️ React es ~1 año — es el
punto flojo, no Python.

## Senior Full-Stack Engineer (.NET/Angular) — GovTech / HR Software · 12 ago
https://jobs.ashbyhq.com/truelogic/fd49f0c7-396e-4179-8a4e-427b1ce851fb

**GovTech**, y él entregó para el sector gobierno. Los requisitos:

- 5+ años con C#, .NET, Angular y SQL ⚠️ el único muro
- MS SQL Server con procedimientos almacenados, índices y optimización de consultas ✅
- **"Experiencia con herramientas de desarrollo asistido por IA como GitHub Copilot, Claude Code o Cursor"** ✅
- **"Comprensión de conceptos de IA incluyendo LLMs, MCP y RAG"** ✅
- Pruebas unitarias y de integración ✅

## Senior Full-Stack Engineer (TypeScript / AI Automation) — Real Estate · 28 may
https://jobs.ashbyhq.com/truelogic/6e4b2e7e-11aa-4a14-9b59-a20eb67587ef

Pide **"experiencia práctica usando asistentes de código como Cursor o Claude Code"** y construir
funcionalidades con LLM o **sistemas agénticos**. PostgreSQL ✅.
⚠️ El muro es *"expert-level proficiency in TypeScript"* con genéricos y uniones discriminadas.
TypeScript no es su fuerte.

## Otras del tablero, para tener en cuenta

**Senior Software Architect (C#/Angular/AI First) — GovTech** y **Principal Full-Stack Engineer
(.NET/Angular) (AI-First)**: su stack exacto más gobierno más IA, pero nivel **arquitecto y
principal**. Fuera por ahora — vale saber que existen porque es la dirección natural en dos años.

**Forward Deployed Engineer (AI & Business Transformation)**: pide 5–10 años de consultoría. Fuera.

---

## Canales probados que NO sirvieron

| Canal | Resultado |
|---|---|
| **t.me/s/remotejobscol** | **Nada nuevo desde el 17 de agosto** (un solo post, de QA) |
| **Himalayas** (`himalayas.app/jobs/api`) | Funciona, pero son **98.350 avisos sin filtrar** y el API no tiene búsqueda. No es viable paginarlo |
| **RemoteOK** (`remoteok.com/api`) | Funciona, devuelve solo ~100 avisos recientes. **Cero coincidencias** con su stack elegibles para LATAM |
| Lever y Workable en 12 empresas | Ningún slug respondió |

---

## Lo que cambia

**Este canal no tiene contador de postulantes.** En Get on Board sabemos que 209 postulantes es
ruido y 8 es señal; acá no hay dato, pero tampoco hay 900 personas que ya aplicaron desde un botón
de LinkedIn. Se postula en el sistema de la empresa, no en un agregador.

**Dos entran directo arriba de la cola:**

1. **Wizeline — Senior AI Engineer (Python Advanced), Colombia.** FastAPI, ASGI, LLM, tests,
   GitHub Actions, y **sin requisito de años en la lista de skills**. El único vacío es AWS.
2. **Truelogic — Semi-Senior Full Stack (Python/React).** Dice Semi-Senior y pide GenAI.

**Y hay que ampliar la lista de tableros.** Solo probé 12 empresas y respondieron 2. Vale probar
los slugs de las que ya sabemos que contratan en Colombia: CI&T, AgileEngine, BairesDev, Applaudo,
Encora, Perficient, Slalom, Auxis, Cegeka, Movate.
