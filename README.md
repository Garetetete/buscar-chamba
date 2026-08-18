# BuscarChamba

Búsqueda de trabajo remoto de Saúl Eduardo Córdoba Romero — 2026.

> ⚠️ **Este repositorio es privado a propósito.** Contiene expectativas salariales, evaluaciones
> honestas de vacíos de experiencia, y material cubierto por el acuerdo de confidencialidad con
> SASOFTCO. **No cambiar a público.** El historial de git conserva todo lo que se sube, así que
> hacerlo público una vez lo expone para siempre.

## Qué hay aquí

| Archivo | Para qué sirve |
|---|---|
| `Perfil_Saul_Cordoba.md` | **La fuente.** Experiencia, stack, formación, proyectos y las restricciones contractuales. Todo lo demás sale de acá |
| `Postulaciones.md` | Seguimiento de las postulaciones enviadas: fecha, salario, qué se respondió, estado |
| `Vacantes_YYYY-MM-DD.md` | Un archivo por barrido de búsqueda, con enlaces verificados |
| `CVs/*.tex` | CVs en LaTeX, uno por perfil de puesto. Compilan en Overleaf |
| `Entrevista_Manukora_Guion.md` | 22 preguntas con respuestas, cifras clave y frases de emergencia |
| `Entrevista_Manukora_Decisiones.md` | Por qué se decidió cada cosa en la prueba práctica |
| `LinkedIn_Perfil.md` | Titular, "Acerca de", aptitudes y checklist de configuración |
| `Prueba_Manukora.md` | Análisis de los datos de la prueba práctica |

Los CVs son **ATS-first**: sin tablas, sin columnas, sin gráficos. Una sola columna, texto
seleccionable. Compilar con pdfLaTeX.

## Qué NO está aquí

Dos proyectos que tienen repositorio propio y quedan excluidos por `.gitignore`:

- [manukora-sop-briefing](https://github.com/Garetetete/manukora-sop-briefing) — la prueba práctica de Manukora
- [rag-doc-assistant](https://github.com/Garetetete/rag-doc-assistant) — asistente de documentos con RAG

## Reglas que se aplican en cada postulación

**Expectativa salarial, según el esquema de contrato:**

| Esquema | Pedir |
|---|---|
| Rol normal, contrato laboral | USD 2.800 |
| Rol Senior, contrato laboral | USD 3.000 |
| Prestación de servicios | USD 3.300–3.500 |

Preguntar el esquema **antes** de dar un número. Dar rango, no número único.

**Confidencialidad (SASOFTCO, otrosí 003).** Nunca mencionar el nombre interno de la plataforma,
el dominio de negocio, la receta de optimización de costos ni la descomposición interna del
sistema. Aplica a entrevistas, no solo a los CVs. La descripción aprobada es *"plataforma SaaS de
análisis documental con IA"*, y los clientes se nombran **solo por sector** (gobierno y seguros).

**Fecha de inicio:** la cláusula de exclusividad va hasta el **30 de agosto de 2026**. Negociar
inicio en septiembre, y plantearlo **solo cuando salga el tema de oferta**.

**React:** declarar ~1 año con precisión y compensar con Angular. No inflarlo.

## Verificar enlaces de vacantes

Nunca construir la URL de una vacante a partir del título — no funciona. Leer el `href` real y
verificarlo antes de guardarlo. Get on Board devuelve 403 a los fetch normales, pero responde bien
con un user-agent de navegador:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36" \
  "https://www.getonbrd.com/jobs/..."
```

## Dónde buscar

| Canal | Rendimiento observado |
|---|---|
| **LinkedIn** | ~40 vacantes compatibles cada 48 h. El volumen está acá |
| **Get on Board** | Agotado para Colombia: ~1 nueva útil por barrido sobre 410 activas. Pero muestra **número de postulantes**, que es la mejor señal de todas |
| **t.me/s/remotejobscol** | Canal público que recopila posts de contratación. Trae vacantes por **correo directo, sin contador de postulantes** |
| CompuTrabajo | Poco útil para remoto internacional |

**La señal más importante es el número de postulantes.** Las postulaciones con 1 postulante han
llegado a entrevista; las de 600+ nunca respondieron.
