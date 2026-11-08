# Loom para BuilderBot Pro — guion y comandos

> Demo principal: `manukora-sop-briefing` (repo público). Mención corta, sin mostrar nada: el
> barrido de vacantes. Duración objetivo: **2:30**. En inglés, con tu voz; cámara opcional.
> El Loom tiene que quedar **público** antes de enviarlo.

## Antes de grabar (5 minutos)

**Qué abrir, y nada más:**

1. **Navegador, una ventana nueva** con solo estas pestañas (ni Gmail, ni Get on Board, ni nada
   personal; el Gmail conectado es de otra persona y no puede aparecer):
   - https://github.com/Garetetete/manukora-sop-briefing — el README con el diagrama
   - https://github.com/Garetetete/manukora-sop-briefing/blob/main/output/sop-briefing-2026-03.md
     — el informe generado
2. **VS Code abierto solo en la carpeta** `D:\Pruebas\BuscarChamba\manukora-sop-briefing`
   (no en `BuscarChamba`, porque el explorador mostraría `buscar-chamba` y el ejercicio de
   JustInsurance). Deja abierto `sop/narrative.py` en la línea 590 (`generate_briefing`).
3. **Terminal (PowerShell)** con letra grande (`Ctrl` + `+` tres o cuatro veces):

```powershell
cd D:\Pruebas\BuscarChamba\manukora-sop-briefing
cls
```

**Revisa también:**
- Notificaciones de Windows apagadas (Inicio → "Asistente de concentración" / "No molestar").
- Nada de tokens ni variables de entorno en pantalla. No corras `set`, `env` ni `echo $env:...`.
- Haz una grabación de prueba de 10 segundos para revisar el micrófono.

## Los comandos, en orden

Todos probados el 2 de noviembre en tu máquina (Python 3.12): sin API key, sin internet, cada
uno tarda menos de 5 segundos.

| # | Comando | Qué se ve |
|---|---|---|
| 1 | `python -m sop.cli --template-only` | 12 SKUs leídos, 4 recomendaciones de pedido, 2 en vigilancia, 3 decisiones, 3 conflictos de datos |
| 2 | `python ..\buscar-chamba\BuilderBot\demo_guard.py` | Los 3 casos del guardia: modelo honesto, modelo que se corrige y modelo que insiste en inventar |
| 3 | `python -m pytest -vv -k "invented or hallucin or degrades"` | 5 pruebas del guardia con nombres legibles: "a hallucinated number triggers a retry", "persistent hallucination falls back to the template", "a failing provider degrades instead of crashing" |
| 4 | `python -m pytest` | `77 passed` |

**Qué hace `demo_guard.py`:** cambia el modelo real por uno guionizado que devuelve respuestas
fijas. Así el guardia actúa en vivo sin API key y sin esperas. Lo dices en voz alta en el video
("I swap the real model for a scripted one"); no es un truco, es como lo prueban las pruebas.

## El guion

Frases cortas a propósito. No lo leas palabra por palabra: ten esta hoja al lado y di la idea de
cada bloque con tus palabras. Si te equivocas, sigue; Loom deja recortar el principio y el final.

**[0:00–0:15] · Cámara encendida · pestaña del README**

> Hi, I'm Saúl Córdoba, a full-stack and AI engineer from Colombia. In the next two minutes I'll
> show you an automation I built, and what it does when the AI gets something wrong.

**[0:15–0:40] · Baja al diagrama del README · si quieres, apaga la cámara aquí**

> This started as a brief from Manukora, a honey brand. Every month, someone turns a sales and
> inventory spreadsheet into a briefing for the executives. By hand, that takes hours, and it's
> easy to get a number wrong. So I built it around one rule: Python does all the math, and the
> model only writes the text.

**[0:40–1:00] · Terminal → comando 1 · luego, un segundo en la pestaña del informe**

> One command. It reads twelve products, calculates demand and stock cover, and flags four
> reorders, ranked by revenue at risk. This run doesn't even need an API key. If no model is
> available, it still produces the full briefing from a template.

**[1:00–1:40] · Terminal → comando 2 · señala cada caso mientras sale**

> Now the interesting part. Models make up numbers. So every figure in the model's text is
> checked against the computed facts. Here I swap the real model for a scripted one, so you can
> see the guard work.
>
> First: an honest answer. It ships.
>
> Second: the model invents fifty-two thousand dollars. The guard rejects it and sends a
> correction, and the second try is clean.
>
> Third: the model keeps inventing. Instead of shipping a wrong briefing, it falls back to the
> template. It degrades, it doesn't break.

**[1:40–1:55] · VS Code en `generate_briefing` → terminal, comandos 3 y 4**

> This is the whole loop: try, check, retry once, fall back. And each of those paths is a test.
> Seventy-seven tests, running on Linux, Mac and Windows on every push.

**[1:55–2:15] · Puedes volver a la cámara o dejar el README de fondo**

> I build like this every day with Claude Code. For example, I run my own job-search pipeline
> with it: six sources, de-duplication, and retries when an API rate-limits me. Claude writes a
> lot of the code. I review it, and I own what ships.

**[2:15–2:30] · Cierre**

> For your team it's the same idea. A GoHighLevel webhook fails, or a Stripe token expires: the
> agent detects it, retries, and if it still can't fix it, it alerts a human instead of failing
> silently. Thanks for watching.

## No decir ni mostrar

- Nada de SASOFTCO: ni pantallas, ni nombre del producto, ni clientes.
- Nada del ejercicio de JustInsurance.
- Nada del bot del juego.
- No digas que fue una prueba de contratación ni cómo terminó. "A brief from Manukora" es
  verdad y basta. Si en la llamada preguntan, lo cuentas tal cual.
- No muestres archivos de `buscar-chamba`: el barrido se menciona, no se enseña.

## Después de grabar

1. Recorta el inicio y el final en Loom.
2. Compartir → **Anyone with the link** (público). Ábrelo en una ventana de incógnito para
   comprobar que se ve sin iniciar sesión.
3. Pega el enlace en el formulario: https://builderbot.techfektor.com/ai-builder
4. Avísame para registrarlo en `Postulaciones.md`.
