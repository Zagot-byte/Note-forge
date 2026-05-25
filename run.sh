#!/bin/bash
set -e

echo "[*] Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "[!] Ollama is not installed"
    echo "    Install it from: https://ollama.com"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "[+] Creating .venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "[+] .venv activated"

uvicorn main:app --reload
