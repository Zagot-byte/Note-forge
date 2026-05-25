# tools.py — tool schemas, executors, and executor dispatch table

import json
import aiofiles
import httpx

from config import TEMPLATES_DIR, VALID_TYPES


# ---------------------------------------------------------------------------
# Schemas (Ollama tool-calling format)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "select_template",
            "description": (
                "Returns the markdown template for the detected content type. "
                "Call this first before writing the note."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "content_type": {
                        "type": "string",
                        "enum": VALID_TYPES,
                        "description": "The content type detected from the input.",
                    }
                },
                "required": ["content_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information about a CVE, tool, technique, "
                "or concept. Only call when missing info would meaningfully hurt accuracy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Concise search query, 3–8 words.",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Executors
# ---------------------------------------------------------------------------

async def exec_select_template(content_type: str) -> str:
    template_path = TEMPLATES_DIR / f"{content_type}.md"
    if not template_path.exists():
        return f"[template not found for type: {content_type}]"
    async with aiofiles.open(template_path, encoding="utf-8") as f:
        return await f.read()


async def exec_web_search(query: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"},
            )
            r.raise_for_status()
            data = r.json()

        parts = []
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            parts.append(abstract)
        for topic in data.get("RelatedTopics", [])[:4]:
            text = topic.get("Text", "").strip()
            if text:
                parts.append(text)

        return "\n\n".join(parts) if parts else f"[no instant-answer result for: {query}]"

    except Exception as e:
        return f"[web_search unavailable: {e}]"


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

TOOL_EXECUTORS = {
    "select_template": lambda args: exec_select_template(args["content_type"]),
    "web_search":      lambda args: exec_web_search(args["query"]),
}
