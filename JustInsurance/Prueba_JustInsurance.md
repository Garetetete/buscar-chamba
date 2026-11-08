# Prueba técnica — Senior AI Native Full-Stack @ JustInsurance

> ⚠️ **Privado. No va dentro del repositorio que se entrega.** Está en español a propósito, como
> en Manukora: todo lo del entregable va en inglés, así un archivo en español ahí salta a la vista.
> El prompt para Claude Code está en `Prompt_Claude_Code.md`.

## Estado

- **Vacante:** Senior AI Native Full-Stack Software Engineer · remoto · **USD 4.000–6.000/mes** ·
  Get on Board (417 postulantes al 31 oct).
- **27 oct:** respondió las 3 preguntas. **30 oct:** invitación a la prueba; Saúl aceptó, dio el
  correo de Drive (sauleduardo1111@gmail.com) y se comprometió a entregar **a más tardar el lunes
  2 nov, 6 p. m. hora Colombia**, si el acceso llega el sábado.
- **Después:** solo finalistas, 45 min en vivo explicando la entrega y haciendo un cambio pequeño,
  con IA permitida.

## La empresa

- **Qué es:** cursos para sacar la licencia de agente de seguros en EE. UU. (vida, salud y P&C en
  los 50 estados), educación continua, exámenes de práctica, clases en vivo, y paneles para que las
  agencias sigan a sus reclutas. Precios desde USD 199 la licencia y USD 39 la educación continua.
  Más de 20.000 estudiantes, 4,9 en Trustpilot (145 reseñas).
- **Fundador y CEO:** Justin vom Eigen. Fundó en 2018 y vende cursos desde 2022; antes vendía
  carros. Empezó porque los agentes que reclutaba reprobaban el examen. Sede en Puerto Rico, oficina
  en Miami, unas 15 personas a dic. 2025 y planes de crecer.
- **Para qué te quieren:** probablemente el primer ingeniero de planta. Trabajarías con el **COO**
  y el líder técnico actual, y heredarías código hecho con IA.
- **Stack observado:**
  - Sitio y checkout en **Next.js sobre Vercel** (antes WordPress).
  - Panel del estudiante en **React + Vite + Tailwind** con backend **Python (gunicorn)** en Render.
  - LMS: **Absorb**.
  - CRM y mensajería: **GoHighLevel**, más Bitrix24 y Google Sheets por agencia.
  
  El Python del panel es un punto a tu favor para la entrevista.
- **Fuentes:** aviso de Get on Board, refreshmiami.com (dic. 2025), Trustpilot, los encabezados de
  sus sitios. El sitio principal bloquea visitas fuera de EE. UU. y Canadá, así que no se leyó.

## Qué evalúan (de sus propias palabras)

- "Not looking for someone who only knows how to generate applications through prompts without
  understanding the underlying code." → **Todo lo que entregues lo tienes que poder explicar y
  modificar en vivo.**
- "Understands the difference between a working prototype and reliable production software." →
  Los cinco temas del ejercicio son justo eso: duplicados, entrega incierta, carreras.
- Piden por escrito: código, pruebas, explicación de cambios **y riesgos pendientes**, nota de uso
  de IA y tiempo usado. "Stop at the cap and explain anything unfinished."

## Lo que se reutiliza de Manukora (y lo que no)

Nadeem elogió la separación clara de responsabilidades y que hubiera pruebas, supuestos y registro
de prompts: *"That made the work much easier to evaluate."*

| Se reutiliza | Se deja (no cabe en 3 h) |
|---|---|
| Leer el enunciado contra el código antes de programar (Fase 0) | Matriz de CI en 3 sistemas |
| `SPEC.md` corto con REQ numerados y lista de fuera de alcance | 77 pruebas (aquí 15–25 bien elegidas) |
| Pruebas nombradas por REQ y una prueba de contraste por trampa | Varios proveedores de LLM, diagramas |
| Registro de "dónde se equivocó la IA" escrito sobre la marcha | `assumptions.md` largo (va en el HANDOFF) |
| Commits pequeños con el porqué en el cuerpo | Auditoría aparte larga (aquí 10 min) |
| Clonar limpio y seguir el propio README antes de entregar | |

### Qué salió mal o flojo en Manukora, y cómo se evita aquí

| En Manukora | Aquí |
|---|---|
| El comando del README fallaba en un clon limpio (`PYTHONPATH=src`); se descubrió tarde | Clonar limpio y seguir el README **antes** de entregar, como paso fijo |
| El código se escribió antes que las pruebas (el commit de pruebas llegó después) | Prueba que falla primero, después el arreglo, por cada REQ |
| Varios commits con la misma hora: se notaba que se agruparon al final | Commit al terminar cada REQ, no en lote |
| Parte del registro de IA se escribió al final | `docs/AI_USE.md` se llena en el momento |
| Se construyó de más (3 proveedores, diagramas, CI en 6 combinaciones) | Solo los 5 temas, en orden de gravedad |
| No había un commit con el proyecto "tal como llegó" (era proyecto desde cero) | Primer commit = el paquete intacto, así el revisor ve el diff limpio |

El rechazo de Manukora llegó después de la entrevista y el revisor elogió la entrega, así que el
método funcionó; lo que se corrige aquí es el orden y la evidencia.

### ¿SPEC o solo agentes?

**SPEC corto sí, fase larga de SPEC no.** El enunciado ya trae los 5 temas, así que no hace falta
la especificación de 12 requisitos de Manukora. Pero ir directo a los agentes sin nada escrito
falla de dos formas: los agentes en paralelo interpretan distinto qué es "correcto", y el revisor
del final no tiene contra qué comparar. Una página con 5–8 REQ, escrita después del
reconocimiento, resuelve ambas cosas, ordena las pruebas y los commits y da la estructura del
HANDOFF.

### Estructura de la entrega

Se respeta la estructura del paquete que manden. Solo se agrega:

```
HANDOFF.md           lo primero que lee el revisor
docs/SPEC.md         5–8 REQ en una pantalla
docs/AI_USE.md       nota de uso de IA y dónde se equivocó
docs/TIME_LOG.md     tiempo real por fase
<carpeta de pruebas de ellos>/  un archivo nuevo por REQ
```

**Git:** el paquete se sube a un repo **privado** de GitHub (`gh repo create --private`). Si el
README pide un enlace, se agrega a Justin como colaborador. Si pide un zip, se manda el zip.
Nunca público, porque el ejercicio es de ellos.

## Antes de que llegue el acceso (no cuenta en las 3 h)

- [ ] Node LTS, git y Claude Code funcionando; probar `npx vitest --version` o `npx jest --version`.
- [ ] Repasar los 5 invariantes de `Prompt_Claude_Code.md` hasta poder explicarlos sin leer.
- [ ] Decidir: ¿explicación escrita o video de 5–7 min? El video ahorra tiempo pero hay que hablar
      en inglés; el escrito lo puede pulir Claude dentro del tope.
- [ ] Bloque de 3 h seguidas, sin reuniones de SASOFTCO.
- [ ] **No empezar el ejercicio antes de tener acceso**, y no abrir el paquete hasta estar listo
      para arrancar el reloj.

## Recordatorios

- No es trabajo pagado ni contrato, así que no choca con SASOFTCO. Si llega oferta, revisar la
  cláusula de exclusividad antes de firmar.
- Si te preguntan el salario en la entrevista: rango publicado USD 4.000–6.000. Pide
  **USD 4.500–5.000**.
- Si el acceso no llega el sábado, escribir el domingo: "Still waiting for Drive access; I'll
  submit within 48 hours of receiving it".
