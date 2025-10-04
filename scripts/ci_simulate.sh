#!/usr/bin/env bash
set -euo pipefail
echo "[CI] Installing requirements..."
pip install -r requirements.txt
echo "[CI] Running flake8..."
flake8 backend tests
echo "[CI] Running pytest..."
pytest -q
echo "[CI] Done."
