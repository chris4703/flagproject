#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec .offline/llama/llama-server -m .offline/qwen.gguf --alias flagstaff-local --host 127.0.0.1 \
    --port "${NAV_MODEL_PORT:-8879}" -c 3072 -np 1 -ngl 99 --no-webui --log-disable
