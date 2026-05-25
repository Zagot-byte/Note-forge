# loop.py — agentic tool-calling loop

import json
import logging
import httpx

from fastapi import HTTPException

from config import OLLAMA_URL
from tools import TOOLS, TOOL_EXECUTORS

logger = logging.getLogger(__name__)


async def run_tool_loop(messages: list, payload_base: dict) -> str:
    """
    Drives the Ollama chat endpoint in a tool-calling loop.
    Returns the final text response once the model stops calling tools.
    """
    messages = list(messages)

    async with httpx.AsyncClient(timeout=180.0) as client:
        for round_num in range(10):  # safety valve
            payload = {
                **payload_base,
                "messages": messages,
                "tools": TOOLS,
                "stream": False,
            }

            logger.debug(f"[round {round_num}] sending payload:\n{json.dumps(payload, indent=2)[:3000]}")

            try:
                resp = await client.post(OLLAMA_URL, json=payload)
                logger.debug(f"[round {round_num}] response {resp.status_code}: {resp.text[:1000]}")
                resp.raise_for_status()
            except httpx.ConnectError:
                raise HTTPException(status_code=503, detail="ollama not running")
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Ollama error: {e} | body: {resp.text[:500]}"
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ollama error: {e}")

            data = resp.json()
            msg  = data.get("message", {})
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                return msg.get("content", "")

            messages.append({
                "role": "assistant",
                "content": msg.get("content", ""),
                "tool_calls": tool_calls,
            })

            for call in tool_calls:
                fn_name = call.get("function", {}).get("name", "")
                fn_args = call.get("function", {}).get("arguments", {})

                if isinstance(fn_args, str):
                    try:
                        fn_args = json.loads(fn_args)
                    except json.JSONDecodeError:
                        fn_args = {}

                executor = TOOL_EXECUTORS.get(fn_name)
                result   = await executor(fn_args) if executor else f"[unknown tool: {fn_name}]"

                logger.debug(f"[round {round_num}] tool {fn_name} → {result[:200]}")
                messages.append({"role": "tool", "content": result})

    raise HTTPException(status_code=500, detail="tool-call loop exceeded max rounds")
