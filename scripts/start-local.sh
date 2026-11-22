#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export NAV_MODEL_URL="${NAV_MODEL_URL-http://127.0.0.1:${NAV_MODEL_PORT:-8879}}"
exec "${NAV_PYTHON:-python3}" server.py
