#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p .state
model_port="${NAV_MODEL_PORT:-8879}"
app_port="${NAV_PORT:-8878}"

if [ -x .offline/llama/llama-server ] && [ -s .offline/qwen.gguf ]; then
    if ! curl -fsS --max-time 2 "http://127.0.0.1:$model_port/health" >/dev/null 2>&1; then
        if ! [ -s .state/demo-model.pid ] || ! kill -0 "$(cat .state/demo-model.pid)" 2>/dev/null; then
            nohup ./scripts/start-model.sh > .state/demo-model.log 2>&1 </dev/null &
            echo $! > .state/demo-model.pid
        fi
    fi
else
    echo "Local model assets are unavailable. The interview will run with rules."
fi

if ! curl -fsS --max-time 2 "http://127.0.0.1:$app_port/api/health" >/dev/null 2>&1; then
    nohup ./scripts/start-local.sh > .state/demo-app.log 2>&1 </dev/null &
    echo $! > .state/demo-app.pid
fi

attempt=0
until curl -fsS --max-time 2 "http://127.0.0.1:$app_port/api/health" >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 12 ]; then
        echo "The Navigator could not start. Inspect .state/demo-app.log."
        exit 1
    fi
    sleep 1
done
printf 'Open http://127.0.0.1:%s\n' "$app_port"
curl -fsS "http://127.0.0.1:$app_port/api/health"
printf '\nRefresh after the local model loads if model_ready is false.\n'
