# config.py — paths, model, and valid note types

from pathlib import Path

NOTES_DIR     = Path.home() / "notes" / "thm"
TEMPLATES_DIR = Path(__file__).parent / "templates"
OLLAMA_URL    = "http://localhost:11434/api/chat"
MODEL         = "gemma4-cyber:latest"

VALID_TYPES = [
    "ctf-writeup", "privesc", "crypto-hash", "web-pentest",
    "tool-usage", "active-directory", "network", "forensics",
    "malware-re", "research-notes", "general-notes",
]
