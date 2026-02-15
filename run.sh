#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PYTHON="$PROJECT_DIR/venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
    echo "Virtualenv not found."
    echo "Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

cd "$PROJECT_DIR"

exec "$PYTHON" tui.py
