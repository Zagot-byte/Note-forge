#!/bin/bash 
#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    echo "[+] Creating .venv..."
    python3.14 -m venv .venv
fi

source .venv/bin/activate

echo "[+] .venv activated"

uvicorn main:app --reload
