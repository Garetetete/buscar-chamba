# Perfil — Saúl Córdoba

> Fuente de verdad para construir y perfeccionar el CV. Última actualización: 2026-07-24.

## Datos personales
- **Nombre:** Saúl Córdoba
- **Teléfono:** (+57) 321 961 1182
- **Email:** sauleduardo1111@gmail.com
- **Ubicación:** Villavicencio, Colombia — acepta trabajo remoto; **búsqueda enfocada en Chile** (remoto/relocalización)
- **GitHub:** https://github.com/Garetetete
- **LinkedIn:** https://www.linkedin.com/in/saul-cordoba-a2997427b
  - ✅ **Enlace correcto desde el 4 oct 2026: `saul-cordoba-a2997427b`** (Saúl lo dejó sin tildes ese día). Hasta esa fecha los 11 CVs, este perfil y el portafolio (garetetete.github.io) apuntaban a `saul-eduardo-cordoba-romero-13b5b72b6`, que no es su perfil. Los CVs se corrigieron el 4 oct; **el portafolio y las postulaciones ya enviadas siguen con el enlace viejo**.
- **Inglés:** B2

## Educación
- **Ingeniería Electrónica — Universidad de los Llanos**, 2018 – 2024 (egresado 2024)
- **Especialización en Instrumentación y Control Industrial — Universidad de los Llanos**, 2024 – 2025
  - **Modalidad de grado: Diplomado en Sistemas IoT y PLC** (con esto se graduó de la especialización)
- **Especialización en Ingeniería de Software — Universidad de los Llanos**, 2025 – 2026

## Habilidades técnicas
*(declaradas por Saúl + verificadas en sus proyectos reales)*
- **Lenguajes:** C, C++, Python, Java, C# (.NET), TypeScript/JavaScript, SQL, MATLAB
- **Backend:** .NET (Clean Architecture / Ardalis), FastAPI, Node/Express, microservicios, API gateways
- **Frontend:** Angular (14–22) y **React 18** (Vite, PrimeReact, react-hook-form), TailwindCSS
  - React confirmado por Saúl el 2026-07-29: ha tocado back **y** front de los proyectos de la empresa. Evidencia en `SoftPolitico\sasoftco_govcodepro_forms_generator_frontend` (app React 18 real, no dependencia transitiva). Esto le abre el segmento **Node.js + React**, que es el de mayor demanda en Get on Board.
- **Bases de datos:** **Oracle** (SQL analítico, usado profesionalmente en Btilink/Aera Energy), PostgreSQL, SQL Server, MongoDB, Redis
- **Automatización industrial e IoT (formación académica, NO experiencia laboral):** programación de **PLC Siemens** con **TIA Portal**, sistemas **SCADA**, **IoT industrial**, lógica de control de procesos. Respaldado por el **Diplomado en Sistemas IoT y PLC**. Aprendido en la universidad, no en la petrolera.
- **DevOps e infraestructura:** Docker y Docker Compose, Linux (avanzado), SSH/despliegue remoto en servidores, Azure DevOps Pipelines, GitHub Actions, CI/CD, nginx, Keycloak/JWT (auth), n8n (automatización)
- **IA / LLMs:** Google ADK (sistemas multiagente), Vertex AI, Gemini, MCP servers, desarrollo agéntico spec-driven (SDD con OpenSpec/Claude Code); visión por computador (OpenCV, MediaPipe)
- **Datos / BI:** Tableau, Power BI, Looker Studio, Pandas, scraping con Selenium
- **Arquitectura y metodologías:** SDD, TDD, Clean Architecture, microservicios, monorepos

## Proyectos en los que ha trabajado (evidencia en repos locales)
- **Cynthia (autoría propia, desde 0):** ver sección "Proyecto insignia" arriba.
- **IALicitaciones:** sistema multiagente (Google ADK + Vertex AI/Gemini) para análisis forense de licitaciones: coordinador + 6 agentes especializados (extracción, análisis legal/económico/técnico en paralelo, estratega) que generan 5 reportes.
- **Plataforma de trámites ciudadanos (MinTIC, Chiquinquirá):** microservicios .NET Core (Clean Architecture) + Angular 14 + Camunda BPMN para entidades públicas colombianas.
- **Positiva (aseguradora):** microservicios .NET ("jackcore": auth, auditoría, notificaciones, generador de formularios) + Angular + stack de automatización n8n (PostgreSQL 16, Redis 7, nginx) con CI/CD en Azure Pipelines y GitHub Actions.
- **SIARP / Positiva ARL:** mantenimiento de monolito enterprise Java 8/Spring/MyBatis/Vaadin (~1.700 clases, 24 módulos) con integración SAP y servicios SOAP.
- **PMO Platform:** .NET 9 + Angular 22 + Keycloak 26, totalmente dockerizado.
- **QR Ticketing (Laravel 10 + PostgreSQL):** emisión de tickets QR firmados, pagos con webhooks, control de aforo y validación anti doble ingreso, integrado con WordPress.
- **Análisis de sentimiento facial:** FastAPI + OpenCV/MediaPipe/HSEmotion para líneas de tiempo de emociones en video, con CI (GitHub Actions, pytest, ruff).
- **Pipeline de datos gubernamentales:** CSV → PostgreSQL (Docker) → Looker Studio vía ngrok.
- **Scraper de licitaciones:** Python + Selenium + Pandas sobre licitaciones.info, con descarga masiva de PDFs y filtrado con IA.
- **Juego multijugador en tiempo real:** monorepo TypeScript, Phaser 3 + Socket.io + Express, desplegado en Railway.
- **Plataforma de IA corporativa:** despliegue de LibreChat con Vertex AI + propuesta ejecutiva de arquitectura (gobernanza de costos, anti Shadow-AI).
- **Agente autónomo con LLM para un juego de estrategia web (proyecto personal, oct 2026, en `Desktop\Chamba\Travian`, repo local sin remoto).** Verificado en el código el 2026-10-15:
  - **Dos capas:** un motor de reglas en Python que juega cada 2–10 min (cola de construcción por fases, héroe, almacenes, reservas, detección de ataques vía GraphQL), y un **"cerebro" con la API de Claude** (SDK `anthropic`, Haiku 5.5) que fija la estrategia que el motor ejecuta.
  - **Bucle de agente escrito a mano:** hasta 8 turnos, **15 herramientas con JSON schema `strict`** (lectura, estrategia, acciones de juego, alertas), cada acción **validada contra el estado real** antes de ejecutarse, máximo 5 acciones por llamada, modo *dry-run*, errores de herramienta devueltos al modelo sin tumbar el proceso.
  - **Costos:** *prompt caching* de 1 h sobre un playbook de 720 líneas, revisión cada 55 min para reutilizar la caché, costo por llamada registrado en JSONL (~USD 0,005 por llamada). El cerebro se dispara por eventos (ataque entrante, plan atascado) con *cooldowns*.
  - **Retrospectiva diaria** con salida estructurada (JSON schema) que escribe un diario y lecciones.
  - **Bucle de auto-mejora:** las solicitudes de cambio (del cerebro, de errores repetidos o del usuario) las implementa **Claude Code headless (Opus) en un `git worktree` aislado** con herramientas restringidas y archivos protegidos; exige pytest en verde, hace merge, reinicia vía supervisor y **revierte solo (`git revert`) si no llega un heartbeat sano del nuevo SHA en 25 min**. Límite de 4 por día.
  - **Operación:** supervisor con backoff exponencial y bloqueo de instancia única, heartbeat, Docker Compose o tareas programadas de Windows. Login con Playwright y luego HTTP puro (httpx, GraphQL, REST) con BeautifulSoup.
  - **Calidad:** ~4.400 líneas de Python (22 módulos), **59 pruebas pytest** offline contra fixtures HTML reales, README de 137 líneas. Sin CI ni linter configurados todavía. Todos los commits son co-escritos con Claude Opus (describirlo como asistido por IA).
  - ⚠️ **Para el CV y entrevistas:** el juego (Travian) prohíbe los bots en sus términos (§3), y el repo tiene datos de la cuenta real. **No publicarlo** en GitHub ni en el portafolio, y no nombrar el juego por escrito: describirlo como *"autonomous LLM agent that plays a live web strategy game"*. Este proyecto **no** está cubierto por la cláusula de SASOFTCO, así que aquí sí puede hablar de prompt caching y control de costos.
  - Versión anterior (nov 2025, `Documents\Travian_bot`): prototipo con Playwright async, APScheduler y SQLite, sin LLM ni pruebas.

## Experiencia laboral

### Desarrollador — SASOFTCO (2025 – 2026, actual)
- **Entró alrededor de agosto de 2025** (dicho por Saúl el 2026-10-20); antes estuvo ~1 año en Btilink. Experiencia profesional total: ~2 años; full stack e IA: ~1 año y algo. En tablas de años usar "1+" para Python, Angular, .NET e IA generativa.
- ⚠️ **Contrato renovado hasta el 30 de noviembre de 2026** (dicho por Saúl el 2026-10-20); según él puede retirarse cuando quiera. En formularios: cargo **actual** ("2025 to present"), disponibilidad "on short notice". Revisar si la renovación mantiene la exclusividad, la no competencia y el preaviso del contrato anterior antes de firmar con otra empresa. La confidencialidad del otrosí 003 sigue vigente igual.
- Desarrollo backend y frontend; diseño de arquitectura.
- Docker y gestión de contenedores; C/C++ y Python.
- Gestión de repositorios y pipelines en Azure DevOps.
- **Proyecto destacado — "Cynthia"** (ver sección propia abajo): sistema de inteligencia de licitaciones con agentes IA, creado desde cero. **En producción desde 2026.**

## Proyecto insignia — Cynthia (Sistema de Inteligencia de Licitaciones con Agentes IA)
*Creado desde cero por Saúl dentro de la empresa. Análisis verificado del código fuente (2026-07-24):*

- **Magnitud:** ~50.000 líneas de Python (194 archivos) + microservicio C#/.NET + frontend; **120+ endpoints REST/SSE** en 17 routers; ~20 tablas y ~30 migraciones SQL; 8 servicios orquestados con Docker Compose.
- **Backend:** FastAPI (Python 3.11) + Uvicorn, Poetry, arquitectura por capas (routes → services → core → database), SQLAlchemy 2.0 sobre **PostgreSQL 15**.
- **IA — 4 agentes especializados** vía **Vertex AI / Gemini** (google-genai + Google ADK): *Doc Argus* (análisis técnico multi-empresa con % de aptitud), *Lex Centinela* (legal), *CompetEx* (viabilidad económica), *Ratio Prime* (solvencia financiera). PDFs enviados nativamente a Gemini con prompt-prefix caching y salida estructurada (response_schema JSON).
- **Multi-proveedor BYOK:** capa adaptadora que soporta Gemini, Anthropic Claude, OpenAI y endpoints compatibles (DeepSeek, Kimi); cada tenant aporta sus credenciales, cifradas con Fernet.
- **Optimización de costos IA:** "kill switch" que aborta análisis restantes si el puntaje técnico es bajo (ahorro estimado 59–80%), rotación multi-región de Vertex (4 regiones) con backoff exponencial, modelo Flash barato para segunda opinión.
- **Multi-tenancy real:** grupos/tenants con **Row-Level Security de PostgreSQL** inyectado por middleware, permisos por vista, storage configurable por tenant (OneDrive/SharePoint, Google Drive, local).
- **Ingesta de datos:** API comercial de licitaciones.info + **SECOP II vía API Socrata de datos.gov.co** (consultas SoQL paginadas a 50k filas, chunking por año, filtros UNSPSC), contratos adjudicados y PAA; import/export Excel (openpyxl).
- **Funcionalidades:** streaming SSE de progreso en tiempo real, procesamiento batch paralelo con semáforos, chat conversacional por licitación con historial, **rellenado automático de anexos DOCX/PDF con IA** (incluye detección de PDFs escaneados y scoring de validación), cotizaciones de mercado con Google Search grounding y presupuesto consolidado, dashboards de KPIs con Chart.js, notificaciones por Gmail OAuth.
- **Auth y DevOps:** **Keycloak (OAuth2/OIDC)** con validación JWT, nginx reverse proxy, conversores de documentos duales (servicio ASP.NET Core con Aspose.Words + LibreOffice headless), backups automáticos de Postgres cada 24h con retención de 14 días, contenedor autoheal, healthchecks, entornos QA/test con compose múltiple, calidad con ruff + pytest, desarrollo spec-driven (OpenSpec).
- **Novedades abr–oct 2026 (revisado en el repo el 2026-10-20, ~420 commits, casi todos de Saúl):** clasificación de documentos con IA como etapa de preparación (Word/Excel a PDF, comprimidos, PDF ilegibles), embudo de revisión donde la IA recomienda y el analista decide, vista de estado del sistema con registro de cada análisis, RLS en todas las tablas con tenant tras una auditoría de fugas entre clientes, backends de almacenamiento intercambiables, SECOP como segunda fuente. **En desarrollo, sin subir:** soporte multipaís con datos abiertos de República Dominicana. En formularios: "open-data sources from more than one country (in development)", sin nombrar fuentes.
- ✅ **Decisión de atribución (2026-07-24):** en los CVs no se menciona CGH ni ninguna licencia de terceros.

## 🔒 RESTRICCIONES CONTRACTUALES — leer antes de tocar cualquier CV
Fuente: **Otrosí 003 al Contrato de Prestación de Servicios 032-2026** (leído el 2026-07-29). Vigencia del contrato: **26 ene 2026 – 30 ago 2026**.

**Prohibido en CVs, portafolio, entrevistas y formularios:**
- El **nombre interno del producto** ("Cynthia").
- El **dominio de negocio**: licitaciones públicas, SECOP II, contratación estatal, y los agentes descritos por función legal/económica/financiera.
- La **receta de optimización**: kill-switch por umbral, prompt caching, rotación multirregión, capa BYOK.
- La **descomposición interna**: número de routers, tablas, migraciones.
- El **código fuente** (nunca compartirlo ni subirlo a GitHub personal).

**Permitido y conservado:** autoría en solitario y de extremo a extremo, estado "en producción", stack de herramientas públicas (FastAPI, PostgreSQL, RLS, Keycloak, Docker, Vertex AI, Gemini), magnitud (120+ endpoints, 8 servicios) y una cifra de resultado ("reducción superior al 50% en costos de inferencia").

**Base legal:** Cláusula Vigésima (propiedad intelectual: código, arquitectura de datos, ingeniería de prompts, pesos de modelos — pero **derechos morales de Saúl preservados**, art. 30 Ley 23/1982); Cláusula Vigésima Segunda (confidencialidad permanente + prohibición de **usar la información en beneficio propio**; también prohíbe discutir hallazgos con terceros, o sea aplica a entrevistas); Cláusula Vigésima Tercera (**no competencia durante la vigencia** → negociar inicio de cualquier empleo nuevo **después del 30 de agosto de 2026**).

**Otros hallazgos:** el contrato tiene rasgos de contrato realidad (exclusividad, presencialidad en Cláusula Undécima, menciona "marca empleadora"); confidencialidad y cesión de PI son válidas igual en un CPS, la cláusula frágil es la de exclusividad. Por la Cláusula Undécima se quitó "(Remoto)" de la línea de SASOFTCO en todos los CVs.

### Desarrollador / Analista de datos — Btilink SAS (2024 – 2025)
- **Rol real: analista de datos** (aclarado por Saúl el 2026-07-24), no desarrollo industrial.
- **Consultas SQL sobre bases de datos Oracle** para extraer y consolidar información de la operación petrolera.
- Reportes y dashboards en **Tableau y Power BI** para **Aera Energy LLC** (compañía petrolera de EE. UU., California): ingresos, salidas, volúmenes de producción.
- Dashboards usados por varias personas/equipos para el monitoreo continuo de la operación.
- ⚠️ **Importante:** en esta empresa **no** trabajó con PLC ni SCADA — esos vienen de la universidad. No mezclar.
- *(pendiente: número aproximado de dashboards/usuarios, frecuencia de reportes)*

## Pendientes por definir
1. **Verificar compilación de los 10 CVs tras agregar LinkedIn** — Docker estaba apagado; falta confirmar que ninguno pasó a 2 páginas.
2. **Números concretos de Btilink** (cuántos dashboards, cuántos usuarios, frecuencia de reportes) para equilibrar el peso frente a SASOFTCO.

**Cerrado:** **certificaciones formales tipo Azure/GCP: ninguna.** Pero sí tiene un **Diplomado en Sistemas IoT y PLC**, que fue su **modalidad de grado** para la Especialización en Instrumentación y Control Industrial (aclarado 2026-07-24). Ya incorporado en los 7 CVs dentro de Educación. Los 7 conservan además la sección `CERTIFICACIONES Y DISTINCIONES` comentada por si obtiene alguna después.

## Decisiones tomadas
- **Cargo unificado:** en todas las variantes el cargo en SASOFTCO es **"Desarrollador de Software"** (título real, seguro ante verificación laboral). La especialización se comunica en el headline y el perfil, no inventando títulos.
- **Atribución de Cynthia:** sin mención de CGH ni licencias de terceros (ver sección del proyecto).
- **LaTeX:** nunca usar `\MakeUppercase` dentro de `\titleformat` (rompe en Overleaf); títulos de sección en mayúsculas literales. No usar `babel` español (altera comillas/guiones); sí `microtype` para mejor justificado.
- **Público internacional (2026-07-24):** las referencias colombianas van autoexplicativas para que las entienda cualquier reclutador (Chile, España, remoto). "SECOP II" siempre acompañado de "el sistema nacional de contratación pública de Colombia". No usar siglas locales sueltas (MinTIC, PAA, datos.gov.co) sin glosa.
- **Chile:** los 7 CVs son neutros por rol, NO localizados por país. Si Saúl pide versión para Chile, agregar disponibilidad explícita de relocalización a Chile solo en esas copias (perjudica si aplica en Colombia o a remoto en EE.UU.). Variantes con más tracción allá: industrial y Fullstack+DevOps.

## CVs generados (carpeta `CVs/`)
Todos: una página, ATS-friendly, listos para pegar en Overleaf en blanco (pdfLaTeX).

> ✅ **Verificado por compilación real el 2026-07-24:** los 9 compilan sin errores y ocupan **exactamente 1 página** cada uno.
> Para re-verificar tras cualquier cambio (requiere Docker corriendo), copiar los `.tex` a una carpeta temporal y ejecutar:
> ```bash
> docker run --rm -v "<CARPETA>:/work" -w /work ghcr.io/xu-cheng/texlive-small sh -c \
>   'tlmgr update --self >/dev/null 2>&1; tlmgr install titlesec enumitem microtype >/dev/null 2>&1
>    for f in *.tex; do pdflatex -interaction=nonstopmode "$f" >/dev/null 2>&1; \
>    grep -o "Output written.*" "${f%.tex}.log" | sed "s/.*(//;s/,.*//"; done'
> ```
> Notas: la imagen `texlive-small` **no** trae `titlesec` (de ahí el `tlmgr install`), y `tlmgr` falla sin el `update --self` previo. Usar `MSYS_NO_PATHCONV=1` si se corre desde Git Bash en Windows.

> ✅ **Auditoría ATS (2026-07-24), sobre el PDF compilado, no sobre supuestos.** Extracción de texto verificada con `pypdf` y `pdfminer.six`:
> - Acentos correctos (codepoints reales: Ú = 0xDA, Ó = 0xD3). **Cero** caracteres rotos (U+FFFD). El combo `inputenc utf8 + fontenc T1 + lmodern` funciona.
> - Viñetas = U+2022 (bullet estándar), legible por parsers.
> - Espaciado íntegro con `pdfminer.six` (0 palabras pegadas). Con `pypdf` se pierden algunos espacios tras negritas — es limitación de esa librería, no del PDF.
> - Palabras clave (Azure DevOps, Vertex AI, Clean Architecture, Power BI, SQL Server, SASOFTCO, Btilink…) extraídas correctamente.
> - Una sola columna, sin tablas, imágenes, cajas de texto, encabezados ni pies de página.
> - **Riesgo residual bajo:** los rangos de fecha usan guion medio tipográfico (–, U+2013) en vez de guion simple. Parsers modernos lo manejan; si alguna vez un ATS no interpreta las fechas, cambiar `--` por `-` en las líneas de fechas.
- `CV_Saul_Cordoba.tex` — **general** (Software Developer | Backend, DevOps & AI). Incluye sección de proyectos destacados.
- `CV_Saul_Cordoba_AI_Engineer.tex` — AI Engineer | LLM & Multi-Agent Systems.
- `CV_Saul_Cordoba_Fullstack_Backend.tex` — Fullstack | Backend (.NET, Python, Angular).
- `CV_Saul_Cordoba_DevOps_Platform.tex` — DevOps & Platform Engineer.
- `CV_Saul_Cordoba_Data_BI.tex` — Data Engineer & BI Analyst.
- `CV_Saul_Cordoba_Fullstack_DevOps.tex` — combinado: Fullstack Engineer & DevOps.
- `CV_Saul_Cordoba_EN.tex` — **versión en INGLÉS del CV general** (Software Developer | Backend, DevOps & AI Engineer). Es el que va por defecto a correos directos y avisos internacionales de backend que no son de IA (registrado el 7 de septiembre de 2026; se usó para CyberAtlas).
- `CV_Saul_Cordoba_AI_Engineer_EN.tex` — **versión en INGLÉS** del perfil AI Engineer (para vacantes remotas internacionales).
- `CV_Saul_Cordoba_Fullstack_DevOps_EN.tex` — **versión en INGLÉS** del perfil Fullstack & DevOps (el de mayor demanda en contratación remota).
- `CV_Saul_Cordoba_Industrial_Control.tex` — **Ingeniero Electrónico | Software Industrial, Instrumentación y Control**. Apunta a minería, energía e industria (mercado chileno). Incluye **PLC y SCADA etiquetados como "formación universitaria"** e instrumentación/control como "formación de posgrado", nunca como experiencia laboral. El puente profesional es el rol de analista de datos de operación petrolera (SQL/Oracle) en Aera Energy. **No incluye Modbus, OPC-UA ni marcas específicas de PLC** (Siemens/Allen-Bradley) porque Saúl no las ha nombrado; si trabajó con alguna en la uni, nombrarla eleva bastante esta variante.

## Rutina automática de búsqueda de empleo
- **Agente en la nube (claude.ai routine)** creado el 2026-07-29: busca vacantes remotas de backend (.NET/Python), DevOps, IA y datos, y entrega dos listas — (A) remotas contratables desde Colombia/LATAM, (B) chilenas que exigen residencia.
- Corre **lunes a viernes 8:07am hora Bogotá** (cron `7 13 * * 1-5` en UTC). Modelo: claude-sonnet-5.
- Panel: https://claude.ai/code/routines/trig_019QBZRvrQRYBuYK4gjHoH4T
- **Limitación clave:** corre en la nube, **no** accede a estos archivos locales. El perfil de Saúl y la lista de las 9 variantes de CV van embebidos en el prompt de la rutina — **si cambia el perfil o se agrega/renombra un CV, hay que actualizar el prompt de la rutina** (con `RemoteTrigger` action `update`).
- Tampoco tiene memoria entre ejecuciones, así que puede repetir ofertas de días anteriores.
- Conector de Indeed: registrado en local (user scope) pero **sin autorizar**; no está disponible en la rutina.

## Notas de contexto
- Objetivo de búsqueda: empleo remoto, mercado de **Chile** principalmente.
- Proyecto Cynthia ubicado en `..\Liscitaciones\sistema_web_limpio_FINAL` (análisis técnico ya incorporado arriba).
