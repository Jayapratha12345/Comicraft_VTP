"""Step 3 - Stable Diffusion image generation (lazy-loaded, thread-safe)."""
import threading
import uuid

from .config import PANELS_DIR, SD_MODEL_ID, SD_SIZE, SD_STEPS

_pipe = None
_lock = threading.Lock()

STYLE_HINTS = {
    "anime": "anime style, cel shading, vibrant colors, detailed line art",
    "pixel art": "pixel art, 16-bit retro game style, limited palette",
    "comic book": "classic comic book art, bold ink outlines, halftone shading, vivid colors",
    "realistic": "realistic digital painting, cinematic lighting, highly detailed",
}
NEGATIVE = "text, letters, watermark, signature, blurry, deformed, extra limbs, low quality"


def _get_pipe():
    """Load the model once. Uses GPU (fp16) when available, else CPU (fp32)."""
    global _pipe
    with _lock:
        if _pipe is None:
            import torch
            from diffusers import StableDiffusionPipeline

            if torch.cuda.is_available():
                device, dtype = "cuda", torch.float16
            elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
                device, dtype = "mps", torch.float16
            else:
                device, dtype = "cpu", torch.float32

            pipe = StableDiffusionPipeline.from_pretrained(
                SD_MODEL_ID,
                torch_dtype=dtype,
                safety_checker=None,            # avoids false-positive black images
                requires_safety_checker=False,
            )
            pipe = pipe.to(device)
            pipe.enable_attention_slicing()
            _pipe = pipe
    return _pipe


def generate_image(prompt: str, style: str = "comic book") -> dict:
    """Generate one image. Returns {"path": <disk path>, "url": "/static/panels/x.png"}."""
    hint = STYLE_HINTS.get(style.lower(), style)
    full_prompt = f"{prompt}, {hint}"

    pipe = _get_pipe()
    with _lock:                                  # one generation at a time
        image = pipe(
            full_prompt,
            negative_prompt=NEGATIVE,
            num_inference_steps=SD_STEPS,
            height=SD_SIZE,
            width=SD_SIZE,
        ).images[0]

    filename = f"panel_{uuid.uuid4().hex[:12]}.png"   # short, safe, has extension
    path = PANELS_DIR / filename
    image.save(path)
    return {"path": str(path), "url": f"/static/panels/{filename}"}
