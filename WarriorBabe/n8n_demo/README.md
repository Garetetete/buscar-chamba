# Demo n8n para el video de WarriorBabe (datos sintéticos)

Réplica **sintética** del flujo SolarWinds → service desk: nada del cliente real, todo inventado.

| Archivo | Qué es |
|---|---|
| `2_solarwinds_to_servicedesk.json` | **El flujo que se muestra.** Webhook con token → validar → reglas → **consultar la fuente de verdad** → crear o actualizar ticket → guardar → responder. Sin nodos Code |
| `1_mock_systems.json` | Simula la fuente de verdad y el service desk (Aranda). Guarda el estado en la *static data* del flujo y puede simular una caída |
| `credential_webhook_token.json` | Credencial Header Auth del webhook (`X-Webhook-Token: demo-token-123`, solo demo) |
| `alerta_cpu.json`, `alerta_info.json` | Alertas de prueba para el video |
| `test_demo.py` | Prueba de punta a punta, 46 verificaciones |
| `build_workflows.py` | Genera los tres JSON (por si hay que cambiar algo y regenerar) |
| `levantar_demo.ps1` | Levanta todo en un PC nuevo con un solo comando |
| `demo_alertas.ps1` | Limpia los datos y manda las 3 alertas del video (`-Pausa` para ir con Enter) |

## Verificado (7 nov 2026, n8n 2.46.6 en Docker)

- `test_demo.py`: **46/46**, varias corridas. Cubre: sin token o con token malo → 403; alerta nueva → crea
  ARD-1001; la misma alerta otra vez y un reintento idéntico → actualizan ARD-1001, sin duplicar; otra
  máquina → ARD-1002; informativa y bajo el umbral → se ignoran con su motivo; payload sin NodeName o sin
  MetricName → 400; nodo caído → ticket aunque no traiga umbral; **caída del service desk → 502 tras
  3 reintentos, sin dejar nada a medias; al volver, reenviar la misma alerta crea exactamente un ticket**;
  al final los dos sistemas coinciden.
- Registro de eventos de n8n: 88 de 88 ejecuciones exitosas (el 502 es una ruta manejada, no un fallo).
- Revisado en el editor con capturas: lienzo, zonas, notas y la configuración de cada nodo.

## Buenas prácticas aplicadas (guías oficiales de `n8n-io/skills` y la comunidad de n8n)

- **Nombres:** flujo con verbo y categoría (`Webhook: create service desk tickets from SolarWinds alerts`),
  nodos nombrados por lo que hacen (`Find open ticket`, no `HTTP Request1`), descripción del flujo y
  etiquetas en minúscula (`monitoring`, `service desk`, `demo`).
- **Code es el último recurso:** el flujo principal usa Edit Fields e IF con expresiones. Code solo en los
  mocks, donde hay estado.
- **Lienzo:** izquierda a derecha, rejilla de 16 px, una zona por etapa numerada ("1. Validate payload",
  "2. Apply business rules", "3. Create or update the ticket") con título `###` y una línea; azul =
  validar y transformar, verde = crea algo. Notas en el nodo solo donde la configuración no es obvia.
- **Errores:** los nodos HTTP tienen Retry on Fail (3 intentos, 5 s) y salida de error
  (`continueErrorOutput`) conectada a una sola respuesta 502 sanitizada. Validación con IF y 400.
- **Seguridad:** el webhook exige un token por Header Auth; la credencial no está escrita en ningún nodo.
- **Idempotencia:** la llave es `nodo|métrica`, tomada de los datos de la alerta (no del id de ejecución).
  Reenviar es seguro.

## Usarlo

El contenedor `n8n-wb` ya tiene todo importado y publicado.

1. Si está apagado: `docker start n8n-wb`
2. Abrir http://localhost:5678 y crear la cuenta de dueño (es local, solo vive en tu equipo).
3. Abrir **"Webhook: create service desk tickets from SolarWinds alerts"**.

Desde PowerShell, en esta carpeta:

```powershell
$h = @{ 'X-Webhook-Token' = 'demo-token-123' }

# limpiar datos de la demo (los tickets vuelven a empezar en ARD-1001)
Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/mock/reset

# mandar una alerta (la primera vez crea ARD-1001; la segunda lo actualiza)
Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/solarwinds-alert -Headers $h -ContentType 'application/json' -InFile alerta_cpu.json

# alerta informativa: se ignora
Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/solarwinds-alert -Headers $h -ContentType 'application/json' -InFile alerta_info.json

# ver qué quedó en los dos sistemas
Invoke-RestMethod http://localhost:5678/webhook/mock/state | ConvertTo-Json -Depth 5

# simular caída del service desk (on / off)
Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/mock/outage -ContentType 'application/json' -Body '{"on": true}'
Invoke-RestMethod -Method Post -Uri http://localhost:5678/webhook/mock/outage -ContentType 'application/json' -Body '{"on": false}'
```

Durante la caída, `Invoke-RestMethod` muestra el 502 como error rojo: es lo esperado (tarda ~10 s por
los reintentos). Prueba completa: `python test_demo.py`, y luego el reset antes de grabar.

## Para el video (~40 s dentro de la sección técnica, 0:35–1:40)

1. Antes de grabar: correr el reset. n8n abierto en el flujo y PowerShell al lado.
2. Recorrer el lienzo de izquierda a derecha con el mouse: las tres zonas cuentan la historia solas.
3. Mandar `alerta_cpu.json` → `created`, `ARD-1001`.
4. Mandarla **otra vez** → `updated`, **el mismo** `ARD-1001`, `occurrences: 2`.
   Frase: *"same alert twice, still one ticket — that's the source-of-truth check."*
5. Opcional: pestaña **Executions** → la última ejecución, con el camino en verde por "Add note to ticket".
6. Decir que es una réplica con datos sintéticos del flujo real.

## Recrearlo desde cero (otro PC, o si se borra el contenedor)

Con Docker Desktop abierto, desde esta carpeta:

```powershell
powershell -ExecutionPolicy Bypass -File .\levantar_demo.ps1
```

Crea el contenedor, importa y publica todo, reinicia y deja los datos limpios (probado el 7 nov en un
contenedor nuevo). Si el contenedor ya existe, solo lo enciende y limpia los datos. Lo mismo a mano:

```powershell
docker run -d --name n8n-wb -p 5678:5678 -v n8n_wb_demo:/home/node/.n8n -e GENERIC_TIMEZONE=America/Bogota -e TZ=America/Bogota docker.n8n.io/n8nio/n8n:2.46.6
# esperar ~20 s a que arranque
docker cp credential_webhook_token.json n8n-wb:/home/node/cred.json
docker cp 1_mock_systems.json n8n-wb:/home/node/1.json
docker cp 2_solarwinds_to_servicedesk.json n8n-wb:/home/node/2.json
docker exec n8n-wb n8n import:credentials --input=/home/node/cred.json
docker exec n8n-wb n8n import:workflow --input=/home/node/1.json
docker exec n8n-wb n8n import:workflow --input=/home/node/2.json
docker exec n8n-wb n8n publish:workflow --id=wbMockSystems001
docker exec n8n-wb n8n publish:workflow --id=wbSolarwindsFlow
docker restart n8n-wb
```

Si `import:credentials` falla la primera vez (base de datos ocupada mientras arranca), repetirlo.

## Límites conocidos (por si preguntan)

- Dos alertas idénticas **exactamente al mismo tiempo** podrían crear dos tickets: consultar y crear no
  son un solo paso. En producción: restricción única por llave en la fuente de verdad (insertar primero y
  saltar si choca) o procesar las alertas en cola de una en una.
- Falta un **Error Workflow** a nivel de instancia que avise al equipo (n8n lo marca en su "Production
  Checklist"). En producción se agrega uno con Error Trigger hacia Slack o correo.
- Los mocks no tienen autenticación porque solo existen dentro de la demo.
