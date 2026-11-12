# Giunti Psychometrics — Backend Developer Semi Senior · primera reunión con RH

Aviso: https://co.linkedin.com/jobs/view/4481431932 (barrido del 26 oct). 100 % remoto, solo
residentes en Colombia. Empleo con ley colombiana: contrato fijo de 3 meses, renovable, con
posibilidad de indefinido. **COP 7,7–9 M brutos/mes.** Reporta al Tech Lead, bajo el CTO.

**La empresa:** Giunti Psychometrics es la editorial de pruebas psicológicas del grupo italiano
Giunti, con presencia internacional. Su misión es "hacer accesible la ciencia psicológica a través
de la tecnología": plataformas digitales donde se aplican y califican pruebas. Revisar su web antes
de la reunión para nombrar un producto concreto.

**Lo que piden y lo que él tiene:**

| Piden | Él |
|---|---|
| Python + **FastAPI**, autonomía | Su trabajo diario en SASOFTCO: 120+ endpoints, 8 servicios, hecho solo |
| APIs REST, MySQL/PostgreSQL, Docker, Git | PostgreSQL con RLS, Docker, Git, CI/CD |
| Mantener apps en **PHP** | **MelodicApp** (melodicapp.com), en producción: API en **Laravel 10 / PHP 8.1** (empezó en Laravel 13 / PHP 8.3 y la portó porque el hosting corre 8.1). Ver abajo |
| Integrar CMS, PIM, ERP o CRM | Integración con **Aranda Service Desk** vía n8n (trabajo de equipo; ayudó en todas las fases). Confirmar si tiene otra integración con ERP/CRM |
| Pruebas, documentación, revisión de código | pytest, CI (Manukora: 77 pruebas) |
| Seguridad, protección de datos | Multi-tenant con aislamiento por cliente, Keycloak/OIDC |
| Deseables: GCP (Cloud Run, **Vertex AI**), **LLM y RAG**, Alembic, GitHub Actions | Vertex AI/Gemini en producción, rag-doc-assistant, GitHub Actions |
| Deseables que no tiene | Celery, Prefect, RabbitMQ/Kafka, Django: decirlo con honestidad |
| Título en Sistemas/Software "o afín" | Ingeniero Electrónico **+ Especialización en Ingeniería de Software** (Universidad de los Llanos, 2025–2026). Hueco cerrado |

## Respuestas preparadas (en español)

**Cuéntame de ti (60–90 s).**

> Soy Ingeniero Electrónico y desarrollador backend con Python. Hoy trabajo en SASOFTCO, donde
> construí y mantengo una plataforma SaaS multi-tenant de análisis documental con IA, para
> clientes de gobierno y seguros, en producción desde inicios de 2026. El backend es FastAPI con
> PostgreSQL, son más de 120 endpoints en 8 servicios con Docker, autenticación con Keycloak e
> integración con Vertex AI y Gemini; logré bajar más de un 50 % el costo de inferencia. Antes
> trabajé como analista de datos en Btilink, y por mi cuenta construyo proyectos de IA, como un
> asistente RAG con citas verificables. Me interesa este rol porque es mi stack exacto.

**¿Por qué Giunti?**

> Por el stack, que es justo lo que hago: Python, FastAPI, APIs e integraciones. Y por el
> propósito: llevar pruebas psicológicas validadas a plataformas digitales exige rigor con los
> datos, seguridad y confidencialidad, que es como ya trabajo con información sensible. También me
> atraen sus deseables de LLM y RAG en GCP, porque ya los tengo en producción.

**¿Por qué buscas cambiar?**

> Mi contrato actual termina el 30 de noviembre y busco un rol estable, de largo plazo, en un
> equipo con Tech Lead y CTO del que pueda aprender. (Hablar bien de SASOFTCO.)

**Aspiración salarial.**

> **COP 9 millones brutos mensuales**, dentro del rango que publicaron. Lo justifico porque llego
> con FastAPI en producción y con GCP, Vertex AI, LLM y RAG, que están en sus deseables.

Si insisten en bajar: aceptar desde **COP 8,5 M**. Al ser empleo con prestaciones, 9 M vale más
que USD 2.000 como contratista (prima, cesantías, vacaciones y seguridad social pagas).

**¿Cuándo podrías empezar?**

> El **1 de diciembre**: mi contrato actual va hasta el 30 de noviembre.

**¿Te sirve el contrato fijo de 3 meses?** Sí. Preguntar cómo se evalúa la renovación.

**Inglés.** B2: lee y escribe documentación y habla en reuniones técnicas. Piden intermedio.

**¿Tienes experiencia con PHP/Laravel?**

> Sí. Construí el backend de MelodicApp, una plataforma que convierte una canción en su partitura
> en PDF, y hoy está en producción en melodicapp.com. Es una API en Laravel 10 con PHP 8.1 y
> MySQL, con arquitectura de servicios y repositorios, autenticación JWT y unas 34 rutas. Integré
> varios servicios externos: la pasarela de pagos **Wompi** (el procesamiento arranca solo cuando
> el pago se confirma, para no gastar en pedidos que nadie paga), la API de transcripción musical
> de Klangio con consultas periódicas y reintentos, y la edición del PDF para sellar el título y
> los créditos. Además tiene enlaces de descarga firmados, límites de subida y pruebas con PHPUnit.
> El proyecto empezó en Laravel 13 con PHP 8.3, y lo porté a Laravel 10 con PHP 8.1 porque el
> servidor de producción usaba esa versión.

Sirve también para **integraciones** (pagos y API externa) y para **mantener apps PHP en
producción**. Nada de esto es confidencial de SASOFTCO: es un proyecto aparte.

**¿Has integrado CMS, PIM, ERP o CRM?** (su requisito obligatorio más flojo: no inflarlo)

> Un ERP o CRM comercial como tal no, pero integrar sistemas de negocio por API es buena parte de
> lo que hago. En una empresa de seguros, con mi equipo, conectamos las alertas de monitoreo con la
> mesa de servicio Aranda: un flujo que creaba o actualizaba tickets sin duplicarlos, consultando
> primero un servicio propio que era la fuente de verdad. En MelodicApp integré la pasarela de
> pagos Wompi y una API externa con reintentos. El patrón es el mismo con un ERP o un CRM:
> entender su API y su modelo de datos, autenticar, sincronizar sin duplicar, manejar errores y
> límites, y dejar registro de todo. ¿Con qué sistemas trabajan ustedes? Así me preparo desde ya.

Cerrar con la pregunta convierte el hueco en interés. Si tocó Voyager (panel tipo CMS de Laravel)
en PrismadMusic, sumarlo aquí.

**¿Qué no sabes?** Celery, Prefect, Kafka/RabbitMQ: "no los he usado en producción; sí manejo
tareas asíncronas y reintentos, y aprendo rápido". No inventar.

## Preguntas para hacerle a RH

1. ¿Cómo son las siguientes etapas? ¿Hay prueba técnica?
2. ¿Qué proporción del trabajo es FastAPI nuevo y cuánto es mantener PHP?
3. ¿Con qué sistemas de gestión (ERP, CRM, PIM) integran hoy?
4. ¿Qué tamaño tiene el equipo de tecnología y en qué países está?
5. ¿El horario es el de Colombia? ¿Cómo evalúan la renovación a los 3 meses?

## Ojo

- **Praxis** le ofreció USD 2.000/mes el 5 nov: si Giunti avanza, compararlas.
- No mencionar el nombre del producto de SASOFTCO ni su dominio (confidencialidad).
