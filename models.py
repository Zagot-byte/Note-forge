# models.py — Pydantic request models

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    image_b64: str | None = None
    text: str | None = None
    room: str
    difficulty: str          # Easy | Medium | Hard
    what_was_new: str
    system_prompt: str = ""  # optional override
