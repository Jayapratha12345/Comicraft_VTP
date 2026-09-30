"""Shared Gemini helper: JSON output, model fallback, clear errors."""
import json
import re

from google import genai
from google.genai import types

from .config import GEMINI_API_KEY

_client = None


def _get_client() -> "genai.Client":
    global _client
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Copy .env.example to .env and add your key."
        )
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def parse_json(text: str):
    """Parse JSON even if the model wrapped it in ```json fences."""
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE).strip()
    return json.loads(text)


def generate_json(models: list[str], prompt: str, temperature: float = 0.9):
    """Try each model in order; return parsed JSON from the first that works."""
    client = _get_client()
    config = types.GenerateContentConfig(
        response_mime_type="application/json", temperature=temperature
    )
    errors = []
    for model in models:
        try:
            response = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            return parse_json(response.text)
        except Exception as exc:  # 404 retired model, 429 quota, bad JSON ...
            errors.append(f"{model}: {exc}")
    raise RuntimeError("All Gemini models failed:\n" + "\n".join(errors))
