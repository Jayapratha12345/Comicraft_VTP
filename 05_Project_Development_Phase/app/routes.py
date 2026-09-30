"""All FastAPI routes.

Routes are plain `def` (not `async def`) on purpose: Gemini calls and Stable
Diffusion are blocking, and FastAPI runs `def` routes in a thread pool so the
server stays responsive.
"""
import traceback

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .config import EXPORT_DIR, TEMPLATES_DIR
from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class PromptRequest(BaseModel):
    prompt: str
    character_name: str = "Hero"
    setting: str = "forest"
    tone: str = "dramatic"
    style: str = "comic book"


def run_pipeline(prompt: str, character_name: str, setting: str, tone: str, style: str):
    """outline -> story -> images -> layout -> pdf. Returns (layout, pdf_filename)."""
    outline = generate_outline(prompt, character_name, setting, tone, style)
    story = generate_story(outline, character_name, tone)
    images = [generate_image(p["image_prompt"], style) for p in outline]
    layout = build_comic_layout(images, story, outline)
    return layout, save_pdf(layout)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"error": None})


@router.post("/generate", response_class=HTMLResponse)
def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...),
):
    try:
        layout, pdf_name = run_pipeline(prompt, character_name, setting, tone, style)
    except Exception as exc:
        traceback.print_exc()                    # full error in the terminal
        return templates.TemplateResponse(
            request, "index.html", {"error": str(exc)}, status_code=500
        )
    return templates.TemplateResponse(
        request, "comic_preview.html", {"layout": layout, "pdf_name": pdf_name}
    )


@router.post("/generate-comic/json")
def generate_comic_json(body: PromptRequest):
    try:
        layout, pdf_name = run_pipeline(
            body.prompt, body.character_name, body.setting, body.tone, body.style
        )
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))
    return {"layout": layout, "pdf_path": f"/download/{pdf_name}"}


@router.get("/download/{filename}")
def download_pdf(filename: str):
    # only allow files our own exporter creates (blocks path traversal)
    path = (EXPORT_DIR / filename).resolve()
    if (path.parent != EXPORT_DIR.resolve() or not filename.startswith("comic_")
            or not filename.endswith(".pdf") or not path.is_file()):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=filename)


@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request, file: str = ""):
    return templates.TemplateResponse(request, "export_success.html", {"file": file})


@router.get("/test-image")
def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation",
               style: str = "comic book"):
    try:
        img = generate_image(prompt, style)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))
    return {"message": "Image generated successfully", "path": img["url"]}
