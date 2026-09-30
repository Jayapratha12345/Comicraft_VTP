"""Step 2 - Gemini Pro: narration + dialogue for every panel."""
import json

from .config import GEMINI_PRO_MODELS
from .gemini_client import generate_json


def generate_story(outline: list[dict], character_name: str, tone: str) -> list[dict]:
    """Return a list of dicts: panel, caption, narration, dialogue (list[str])."""
    request = f"""You are a comic book writer. Tone: {tone}. Hero: {character_name}.
Write the text for every panel of this outline. Keep panels self-contained
but part of one cohesive story.

OUTLINE:
{json.dumps(outline, indent=2)}

Return ONLY a JSON array with one object per panel:
  "panel" (integer, same as outline),
  "caption" (short box text, max 15 words),
  "narration" (2-3 sentences),
  "dialogue" (array of strings formatted "Speaker: line", may be empty)."""

    data = generate_json(GEMINI_PRO_MODELS, request)
    if isinstance(data, dict):
        data = next((v for v in data.values() if isinstance(v, list)), data)
    if not isinstance(data, list):
        raise ValueError("Gemini Pro did not return a list of panel stories.")
    return [d for d in data if isinstance(d, dict)]
