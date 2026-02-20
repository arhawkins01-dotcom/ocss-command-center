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

exec "$STREAMLIT_CMD" run app/app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true "$@"
