#!/usr/bin/env bash
# Manda las 3 alertas de la demo y muestra el resultado de cada una. Requiere curl.
# Uso, desde esta carpeta:   bash demo_alertas.sh
# Opciones:  --pausa       espera Enter antes de cada alerta (para ir explicando en el video)
#            --sin-reset   no borra los tickets anteriores
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-5678}"
BASE="http://localhost:$PORT/webhook"
PAUSA=0; RESET=1
for a in "$@"; do
  case "$a" in
    --pausa) PAUSA=1 ;;
    --sin-reset) RESET=0 ;;
  esac
done

send_alert() {
  if [ "$PAUSA" = 1 ]; then read -rp $'\n[Enter] '"$1"; else printf '\n%s\n' "$1"; fi
  if ! out=$(curl -fsS -X POST "$BASE/solarwinds-alert" -H 'X-Webhook-Token: demo-token-123' \
        -H 'Content-Type: application/json' --data-binary "@$2"); then
    echo "No respondio el webhook. Corre primero: bash levantar_demo.sh"; exit 1
  fi
  # Una linea por campo, en verde (python3 viene en casi todo Linux; si no, se muestra el JSON tal cual)
  printf '%s' "$out" | python3 -c 'import json,sys; [print(f"\033[32m{k:<12}: {v}\033[0m") for k,v in json.load(sys.stdin).items()]' 2>/dev/null \
    || printf '\033[32m%s\033[0m\n' "$out"
  sleep 1
}

if [ "$RESET" = 1 ]; then
  curl -fs -X POST "$BASE/mock/reset" >/dev/null
  echo "Datos limpios: los tickets empiezan en ARD-1001."
fi

send_alert "1. Alerta de CPU nueva -> crea el ticket" alerta_cpu.json
send_alert "2. La misma alerta otra vez -> actualiza el mismo ticket, sin duplicar" alerta_cpu.json
send_alert "3. Alerta informativa -> se ignora" alerta_info.json

printf '\nListo. En n8n: flujo principal -> pestana Executions, ahi estan las 3 ejecuciones.\n'
