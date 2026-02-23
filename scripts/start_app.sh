#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

if command -v streamlit >/dev/null 2>&1; then
  STREAMLIT_CMD="streamlit"
elif [[ -x ".venv/bin/streamlit" ]]; then
  STREAMLIT_CMD=".venv/bin/streamlit"
else
  echo "Error: streamlit is not installed. Run: pip install -r app/requirements.txt" >&2
  exit 1
fi

PORT="${OCSS_PORT:-8501}"

port_is_available() {
  python3 - "$1" <<'PY'
import socket
import sys

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  s.bind(("0.0.0.0", port))
except OSError:
  sys.exit(1)
finally:
  try:
    s.close()
  except Exception:
    pass
sys.exit(0)
PY
}

if ! port_is_available "$PORT"; then
  start_port="$PORT"
  found=""
  for try_port in $(seq "$start_port" $((start_port + 20))); do
    if port_is_available "$try_port"; then
      found="$try_port"
      break
    fi
  done

  if [[ -z "$found" ]]; then
    echo "Error: no available port found in range ${start_port}-${start_port}20." >&2
    echo "Tip: stop the other Streamlit server, or set OCSS_PORT=<free_port>." >&2
    exit 1
  fi

  echo "Port $PORT is in use; starting on port $found instead." >&2
  PORT="$found"
fi

exec "$STREAMLIT_CMD" run app/app.py --server.address 0.0.0.0 --server.port "$PORT" --server.headless true "$@"
