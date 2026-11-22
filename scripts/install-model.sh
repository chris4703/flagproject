#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
[ "$(uname -s):$(uname -m)" = "Darwin:arm64" ] || { echo "Apple Silicon macOS required for this installer."; exit 1; }
mkdir -p .offline
release=b12359
archive=".offline/llama-${release}-macos-arm64.tar.gz"
asset="llama-${release}-bin-macos-arm64.tar.gz"
fetch() {
    target="$1"
    url="$2"
    checksum="$3"
    if [ ! -s "$target" ]; then
        curl --fail --location --silent --show-error --retry 2 --output "$target.partial" "$url"
        printf '%s  %s\n' "$checksum" "$target.partial" | shasum -a 256 -c
        mv "$target.partial" "$target"
    fi
    printf '%s  %s\n' "$checksum" "$target" | shasum -a 256 -c
}
fetch "$archive" "https://github.com/ggml-org/llama.cpp/releases/download/$release/$asset" \
    82b00abc740160e1b9980e6cc79c117345fa34af058c80e6c0a69aa8ddccde75
mkdir -p .offline/llama
if [ ! -x .offline/llama/llama-server ]; then
    tar -xzf "$archive" -C .offline/llama --strip-components 1
fi
fetch .offline/qwen.gguf \
    https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51/qwen2.5-1.5b-instruct-q4_k_m.gguf \
    6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e
