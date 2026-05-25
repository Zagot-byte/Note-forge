# main.py — FastAPI app, middleware, routes

import re
import logging

from datetime import datetime
from pathlib import Path

import aiofiles

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from config import NOTES_DIR, MODEL
from models import GenerateRequest
from prompt import SYSTEM_PROMPT
from loop import run_tool_loop

logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def read_root():
    return FileResponse("index.html")


@app.post("/generate")
async def generate_note(request: GenerateRequest):
    if not request.image_b64 and not request.text:
        raise HTTPException(status_code=400, detail="Either image_b64 or text must be provided")

    context_block = (
        f"Room: {request.room}\n"
        f"Difficulty: {request.difficulty}\n"
        f"What was new: {request.what_was_new}\n\n"
        "---\n\n"
    )

    system_prompt = request.system_prompt or SYSTEM_PROMPT

    if request.image_b64:
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": context_block + (request.text or ""),
                "images": [request.image_b64],
            },
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": context_block + request.text},
        ]

    payload_base = {
        "model": MODEL,
        "options": {"temperature": 0.2},
    }

    generated_content = await run_tool_loop(messages, payload_base)

    if not generated_content:
        raise HTTPException(status_code=500, detail="model returned empty response")

    # Derive filename from the <!-- filename: ... --> comment, fallback to room-slug + date
    filename_match = re.search(r'<!--\s*filename:\s*(.+?)\s*-->', generated_content)
    if filename_match:
        filename = Path(filename_match.group(1).strip()).name
    else:
        room_slug = re.sub(r'[^\w\s-]', '', request.room.lower())
        room_slug = re.sub(r'[-\s]+', '-', room_slug).strip('-')
        filename  = f"{room_slug}-{datetime.now().strftime('%Y-%m-%d')}.md"

    # Collision avoidance
    stem      = filename[:-3] if filename.endswith(".md") else filename
    candidate = filename
    counter   = 1
    while (NOTES_DIR / candidate).exists():
        candidate = f"{stem}-{counter}.md"
        counter += 1

    filepath = NOTES_DIR / candidate

    try:
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            await f.write(generated_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to save note: {e}")

    return JSONResponse({
        "filename": candidate,
        "filepath": str(filepath.absolute()),
        "content":  generated_content,
    })
