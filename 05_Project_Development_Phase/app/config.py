"""Central configuration: absolute paths + environment variables."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent      # project root
load_dotenv(BASE_DIR / ".env")

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORT_DIR = STATIC_DIR / "exports"
FONT_PATH = STATIC_DIR / "fonts" / "DejaVuSans.ttf"

for _d in (PANELS_DIR, EXPORT_DIR):
    _d.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def _split(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


GEMINI_FLASH_MODELS = _split(os.getenv("GEMINI_FLASH_MODELS", "gemini-3-flash-preview,gemini-2.5-flash"))
GEMINI_PRO_MODELS = _split(os.getenv("GEMINI_PRO_MODELS", "gemini-3.1-pro-preview,gemini-2.5-pro"))

SD_MODEL_ID = os.getenv("SD_MODEL_ID", "stable-diffusion-v1-5/stable-diffusion-v1-5")
SD_STEPS = int(os.getenv("SD_STEPS", "25"))
SD_SIZE = int(os.getenv("SD_SIZE", "512"))
