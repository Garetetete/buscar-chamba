#!/usr/bin/env bash
# Levanta la demo de n8n desde cero en Linux (o macOS). Requiere Docker y curl.
# Uso, desde esta carpeta:   bash levantar_demo.sh            (opcional: bash levantar_demo.sh <nombre> <puerto>)
set -euo pipefail
cd "$(dirname "$0")"
NAME="${1:-n8n-wb}"
PORT="${2:-5678}"
VOLUME="${NAME}_data"
export MSYS_NO_PATHCONV=1   # solo importa en Git Bash de Windows

if ! docker info >/dev/null 2>&1; then
  echo "No puedo hablar con Docker. Revisa que este instalado y corriendo."
  echo "Si dice 'permission denied': sudo usermod -aG docker \$USER, cierra sesion y vuelve a entrar"
  echo "(o corre este script con sudo)."
  exit 1
fi

wait_n8n() {
  echo "Esperando a que n8n arranque..."
  for _ in $(seq 60); do
    if curl -fs "http://localhost:$PORT/healthz" >/dev/null; then sleep 3; return; fi
    sleep 2
  done
  echo "n8n no respondio en 2 minutos. Revisa: docker logs $NAME"; exit 1
}

n8n_cmd() {
  for i in 1 2 3 4 5; do
    if docker exec "$NAME" sh -c "$1"; then return; fi
    echo "  reintentando ($i)..."; sleep 4
  done
  echo "Fallo: $1"; exit 1
}

if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
  echo "El contenedor $NAME ya existe: lo enciendo."
  docker start "$NAME" >/dev/null
  wait_n8n
else
  docker run -d --name "$NAME" -p "$PORT:5678" -v "$VOLUME:/home/node/.n8n" \
    -e GENERIC_TIMEZONE=America/Bogota -e TZ=America/Bogota \
    docker.n8n.io/n8nio/n8n:2.46.6 >/dev/null
  wait_n8n

  docker cp credential_webhook_token.json "$NAME:/home/node/cred.json"
  docker cp 1_mock_systems.json "$NAME:/home/node/1.json"
  docker cp 2_solarwinds_to_servicedesk.json "$NAME:/home/node/2.json"
  n8n_cmd "n8n import:credentials --input=/home/node/cred.json"
  n8n_cmd "n8n import:workflow --input=/home/node/1.json"
  n8n_cmd "n8n import:workflow --input=/home/node/2.json"
  n8n_cmd "n8n publish:workflow --id=wbMockSystems001"
  n8n_cmd "n8n publish:workflow --id=wbSolarwindsFlow"
  docker restart "$NAME" >/dev/null
  wait_n8n
fi

# n8n responde a /healthz antes de registrar los webhooks; en un PC lento eso tarda.
echo "Esperando a que carguen los flujos..."
for _ in $(seq 90); do
  if curl -fs -X POST "http://localhost:$PORT/webhook/mock/reset" >/dev/null; then
    echo
    echo "Listo. Abre http://localhost:$PORT (la primera vez pide crear una cuenta local)."
    echo "Datos de la demo limpios: la primera alerta crea ARD-1001."
    exit 0
  fi
  sleep 2
done
echo "Los flujos no cargaron. Abre http://localhost:$PORT y revisa que los dos esten publicados, o mira: docker logs $NAME"
exit 1
