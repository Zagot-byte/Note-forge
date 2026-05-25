# Note-Forge

Agentic note-generation tool for TryHackMe learning journals. Feeds raw session input (text + screenshots) through an Ollama-powered tool-calling loop to produce structured, Obsidian-compatible markdown notes.

## How it works

1. Paste session text and/or a screenshot into the web UI
2. The LLM receives a system prompt that instructs it to reconstruct messy input, select the appropriate template, optionally search the web for missing context, and write a structured note
3. A tool-calling loop drives the model — calling `select_template` to fetch a content-type template and `web_search` to enrich CVE/tool references
4. The final note (with YAML frontmatter, wikilinks, journey narrative, key takeaways) is saved to `./notes/`

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com) running locally with a compatible model

## Setup

```bash
# Clone and enter the repo
git clone <repo> && cd Note-Forge

# Create and activate virtualenv (or use run.sh which does this)
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.py`:

| Variable       | Default                      | Description                              |
|----------------|------------------------------|------------------------------------------|
| `NOTES_DIR`    | `./notes`                   | Output directory for generated notes     |
| `OLLAMA_URL`   | `http://localhost:11434/api/chat` | Ollama API endpoint               |
| `MODEL`        | `gemma4-cyber:latest`        | Model to use for generation              |
| `VALID_TYPES`  | *(list of 11 types)*         | Content types with matching templates    |

## Usage

```bash
./run.sh
```

Opens at `http://localhost:8000`.

1. Paste a screenshot (ctrl+v) and/or type text
2. Enter the room name, difficulty, and what was new
3. Click **Generate Note**
4. The generated note appears in the UI and is saved to `./notes/`

## Templates

Templates live in `templates/` — one per content type (ctf-writeup, privesc, web-pentest, etc.). The LLM fetches the matching template via the `select_template` tool and uses it as a structural baseline, enriching sections beyond what the template defines.

## Project structure

```
Note-Forge/
├── main.py          # FastAPI app, routes
├── loop.py          # Agentic tool-calling loop
├── prompt.py        # System prompt
├── tools.py         # Tool schemas & executors
├── models.py        # Pydantic request models
├── config.py        # Paths, model, valid types
├── index.html       # Single-page web UI
├── templates/       # Markdown templates per content type
├── notes/           # Generated notes (local, not tracked)
└── run.sh           # Dev launcher
```
