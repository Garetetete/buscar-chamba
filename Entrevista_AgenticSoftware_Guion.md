# Entrevista con IA — AGENTIC SOFTWARE, Full Stack Developer

Formato: conversación de voz en tiempo real con un entrevistador de IA, en inglés, unos 15 minutos. Un solo intento, sin pausas. Cámara, pantalla y pestañas supervisadas, pantalla completa obligatoria. En 15 minutos caben 5 a 7 preguntas: **respuestas de 60 a 90 segundos**, no más.

## Cómo responder (la regla para todas)

1. **Primero la respuesta directa, en una frase.** Después el ejemplo. La IA evalúa si respondiste lo
   que se preguntó.
2. **Un ejemplo concreto con un número.** "120+ endpoints", "8 services", "more than 50% cost reduction".
3. **Cierra cuando termines.** No rellenes. Si te quedan segundos, calla: es mejor que divagar.
4. **Frases cortas, ritmo tranquilo.** Un B2 claro puntúa mejor que un inglés rápido con errores.
5. **Si no entiendes:** *"Sorry, could you repeat the question?"* o *"Could you rephrase that?"*.
6. **Si no sabes algo:** dilo y muestra cómo lo aprenderías. El aviso lo pide textual: valoran decir
   *"I haven't done that yet"* en voz alta.

**Confidencialidad (SASOFTCO):** "a multi-tenant SaaS platform for AI-powered document analysis",
clientes de gobierno y seguros. Nada de nombre del producto, dominio de licitaciones, caché de prompts,
rotación de regiones ni capa de llaves por cliente.

---

## Lo que pide el cargo (de aquí salen las preguntas)

React, Next.js y TypeScript · Python con FastAPI o Flask · PostgreSQL · Git y CI/CD (GitHub Actions o
Azure DevOps) · algo de Azure (App Services, Functions, Storage, Azure SQL) · Docker. Deseables: OAuth y
JWT, microservicios, integraciones de IA (Azure OpenAI, Claude, MCP), Microsoft 365, redes en Azure.
Es **mid-level** y lo dicen en serio: no esperan que sepas todo.

---

## Preguntas probables y respuestas para practicar

### 1. Tell me about yourself.

I'm a software developer from Colombia. I started as an Electronics Engineer and moved into software, and for the last two years I've built backend and full-stack systems. My main project is a multi-tenant SaaS platform for AI-powered document analysis. I built it on my own, end to end, and it runs in production for government and insurance clients. It uses Python and FastAPI, PostgreSQL, Angular and React on the front end, and eight services in Docker with CI/CD. Before that, I worked as a data analyst for a US oil company, building dashboards on Oracle data. I like owning a feature from the database to the user interface, and I use AI tools every day to move faster.

### 2. Tell me about a project you're proud of. / Walk me through its architecture.

The document-analysis platform. Users upload batches of documents, and the system processes them without supervision and returns structured analyses. The backend is FastAPI on PostgreSQL, with row-level security so each client only sees its own data. Authentication is OAuth2 and OpenID Connect with Keycloak. The AI part uses Gemini models, with outputs validated against a JSON schema before anything is saved. Progress streams to the browser with server-sent events. Everything runs in Docker Compose, deployed with CI/CD. I'm proud of it because it's real: more than 120 endpoints, in production, and I built every layer.

### 3. Tell me about a hard problem you solved. (o: a bug, a challenge, something that went wrong)

Some documents were scanned PDFs with no text layer. The extraction came back empty, and nothing looked wrong, so the system was silently producing bad results. I added a detection step before the model sees the file. Scanned documents are now routed differently and reported, instead of being analyzed as if they were empty. The lesson: an empty result should fail loudly, not pass quietly.

### 4. What's your experience with React and Next.js?

I have about one year with React. I built forms and admin screens with React 18, React Hook Form and TypeScript. Angular is where I have more experience, from version 14 to 22. With Next.js I'm still building experience. I understand the main ideas, like server and client components and file-based routing, and the concepts from React and Angular carry over. It's the first thing I'd strengthen in this role.

### 5. What's your experience with Python and APIs?

Python is my main language. I build REST APIs with FastAPI every day: Pydantic models for validation, SQLAlchemy with PostgreSQL, async endpoints, background jobs with retries, and tests with pytest. I also have a public FastAPI project with unit, BDD and end-to-end tests.

### 6. How do you use AI tools in your work? / Have you integrated AI into an application?

Two ways. First, as a developer: I use Claude Code every day. I write a short spec first, the agent implements it, and the tests decide when it's done. I review every change it makes. Second, inside products: I've integrated Gemini, Claude and OpenAI APIs, with structured outputs validated against a schema, retries, and cost tracking. Measuring where the spend went cut our inference costs by more than half. I've also worked with MCP servers to give agents access to tools.

### 7. What's your experience with Azure? / With cloud?

My production cloud was Google Cloud, with Vertex AI. On Azure, I've used Azure DevOps a lot: repositories and CI/CD pipelines for .NET and Angular projects. I haven't deployed to Azure App Services or Azure Functions in production yet. The concepts are the same I already use, like containers, managed databases and secrets, so I'd expect to ramp up fast.

### 8. How do you handle CI/CD and deployments?

I use GitHub Actions and Azure DevOps Pipelines. A typical pipeline runs linting and tests on every push, builds the Docker images, and deploys to the server. In my public repos, CI runs on three operating systems. I like small, frequent deployments, because they're easier to roll back.

### 9. How do you handle authentication? (OAuth, JWT)

I've implemented OAuth2 and OpenID Connect with Keycloak. The frontend gets the token, the backend validates the JWT on every request, and permissions are checked by role. For multi-tenant data, I add row-level security in PostgreSQL, so even a bug in the API can't leak another client's data.

### 10. Describe a time you had to learn something new quickly.

At work I had to maintain a large legacy Java and Spring system with SAP integration, which wasn't my stack. I started by reading the code paths of the feature I needed, wrote small tests around them, and made changes in small steps. Within a couple of weeks I was shipping fixes safely.

### 11. How do you work with a team / handle disagreement / communicate in a remote team?

I communicate early: if I'm blocked or I see a risk, I say it the same day, in writing. When I disagree with a technical decision, I explain the trade-off with a concrete example, and if the team decides otherwise, I commit to it. In remote work, clear written updates matter more than meetings.

### 12. Why this role? / Why AGENTIC SOFTWARE?

Because it combines the things I do every day: Python services, a modern front end, cloud deployment and AI integrations. And I like that you describe it honestly as a mid-level role where learning fast matters. I'm strong on the backend and AI side, and this role would help me grow on Next.js and Azure.

### 13. Do you have any questions for us? (si la IA lo pregunta)

Yes. What does the first month look like for someone in this role? And what's the current split of work between new features and maintenance?

---

## Antes de empezar (lista rápida)

- Un solo monitor conectado. Todas las demás aplicaciones y notificaciones cerradas.
- Audífonos con micrófono, cuarto en silencio, buena luz de frente.
- Subtítulos en directo de Windows (`Windows + Ctrl + L`) activados **antes** de abrir el enlace, si los
  va a usar. Solo en inglés, sin traducción.
- Agua cerca. Respirar antes de cada respuesta: dos segundos de silencio no restan.
