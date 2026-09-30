"""Step 1 - Gemini Flash: 5-panel comic outline."""
from .config import GEMINI_FLASH_MODELS
from .gemini_client import generate_json

NUM_PANELS = 5


def generate_outline(prompt: str, character_name: str, setting: str,
                     tone: str, style: str) -> list[dict]:
    """Return a list of dicts: panel, title, scene_description, image_prompt."""
    request = f"""You are a professional comic planner.
Create exactly {NUM_PANELS} comic panels for this story.

STORY: {prompt}
MAIN CHARACTER: {character_name}
SETTING: {setting}
TONE: {tone}
ART STYLE: {style}

Return ONLY a JSON array. Each item must have:
  "panel" (integer, 1-{NUM_PANELS}), "title" (string),
  "scene_description" (string, 1-2 sentences),
  "image_prompt" (string: a visual description for Stable Diffusion.
   Always describe {character_name}'s look the same way in every panel.
   Do NOT include speech bubbles or text in the image)."""

    data = generate_json(GEMINI_FLASH_MODELS, request)

    if isinstance(data, dict):                 # some models wrap the list
        data = next((v for v in data.values() if isinstance(v, list)), data)
    if not isinstance(data, list) or not data:
        raise ValueError("Gemini did not return a list of panels.")

    outline = []
    for i, item in enumerate(data[:NUM_PANELS], start=1):
        if not isinstance(item, dict) or not item.get("image_prompt"):
            raise ValueError(f"Invalid panel from Gemini: {item}")
        outline.append({
            "panel": i,
            "title": str(item.get("title") or f"Panel {i}"),
            "scene_description": str(item.get("scene_description", "")),
            "image_prompt": str(item["image_prompt"]),
        })
    return outline
