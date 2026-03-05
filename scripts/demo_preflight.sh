#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

QUICK_MODE="false"
if [[ "${1:-}" == "--quick" ]]; then
  QUICK_MODE="true"
fi

log() {
  printf "[demo-preflight] %s\n" "$1"
}

fail() {
  printf "[demo-preflight] ERROR: %s\n" "$1" >&2
  exit 1
}

if [[ ! -f "app/app.py" ]]; then
  fail "app/app.py not found. Run from the repository root."
fi

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  log "Activated .venv"
fi

PYTHON_CMD="${PYTHON_CMD:-/usr/local/bin/python}"
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
  else
    fail "No Python interpreter found."
  fi
fi

if command -v streamlit >/dev/null 2>&1; then
  log "Streamlit command found in PATH"
elif [[ -x ".venv/bin/streamlit" ]]; then
  log "Streamlit command found in .venv/bin"
else
  fail "Streamlit is missing. Install dependencies with: pip install -r app/requirements.txt"
fi

if [[ "$QUICK_MODE" != "true" ]]; then
  log "Running focused readiness tests"
  "$PYTHON_CMD" -m pytest -q app/tests/test_roles.py app/tests/test_capabilities.py tests/test_notify.py
else
  log "Quick mode enabled: skipping tests"
fi

log "Checking for active Streamlit endpoint"
FOUND_PORT=""
for port in 8501 8502 8503 8504 8505; do
  if curl -fsS "http://localhost:${port}/_stcore/health" >/dev/null 2>&1; then
    FOUND_PORT="$port"
    break
  fi
done

if [[ -n "$FOUND_PORT" ]]; then
  log "Health endpoint is live at: http://localhost:${FOUND_PORT}/_stcore/health"
  log "Open app at: http://localhost:${FOUND_PORT}"
else
  log "No active app instance found on ports 8501-8505"
  log "Start the app with: ./scripts/start_app.sh"
fi

log "Preflight complete"
