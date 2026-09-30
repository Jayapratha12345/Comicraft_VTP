# Phase 7 – Project Documentation

## 1. Project Overview
ComicCraft converts a short story idea into a 5-panel illustrated comic and a downloadable PDF, using
Gemini Flash (outline), Gemini Pro (narration/dialogue) and Stable Diffusion (images) behind a FastAPI web app.

## 2. Folder Structure (Phase 5)
```text
05_Project_Development_Phase/
├── app/
│   ├── main.py            # FastAPI app + static mount
│   ├── routes.py          # endpoints + pipeline
│   ├── config.py          # paths + .env settings
│   ├── gemini_client.py   # shared Gemini call (JSON, model fallback)
│   ├── gemini_flash.py    # generate_outline()
│   ├── gemini_pro.py      # generate_story()
│   ├── image_generator.py # generate_image()
│   ├── layout_builder.py  # build_comic_layout()
│   └── exporters.py       # save_pdf()
├── templates/             # index.html, comic_preview.html, export_success.html
├── static/                # panels/ (images), exports/ (PDFs), fonts/
├── requirements.txt
└── .env.example
```

## 3. Installation Guide
```bash
cd 05_Project_Development_Phase
python -m venv env
env\Scripts\activate                # macOS/Linux: source env/bin/activate
pip install -r requirements.txt
copy .env.example .env              # then edit .env and add GEMINI_API_KEY
uvicorn app.main:app --reload       # run from the folder that contains "app/"
```
Open <http://127.0.0.1:8000>. Interactive API docs: <http://127.0.0.1:8000/docs>.

## 4. Configuration (`.env`)
| Variable | Meaning | Default |
|----------|---------|---------|
| `GEMINI_API_KEY` | Google AI Studio key (required) | – |
| `GEMINI_FLASH_MODELS` | Outline models, tried in order | `gemini-3-flash-preview,gemini-2.5-flash` |
| `GEMINI_PRO_MODELS` | Story models, tried in order | `gemini-3.1-pro-preview,gemini-2.5-pro` |
| `SD_MODEL_ID` | Stable Diffusion repo | `stable-diffusion-v1-5/stable-diffusion-v1-5` |
| `SD_STEPS` / `SD_SIZE` | Quality vs speed | `25` / `512` |

## 5. Usage
1. Enter story prompt, character name, setting, tone, art style → **Generate Comic**.
2. Wait a few minutes (5 images are generated).
3. Review the preview → **Download Your Comic as PDF** → success page.

## 6. API Reference
| Method | Route | Body / Params | Response |
|--------|-------|---------------|----------|
| POST | `/generate` | form: `prompt, character_name, setting, tone, style` | HTML preview |
| POST | `/generate-comic/json` | JSON: `prompt` (+ optional `character_name, setting, tone, style`) | `{layout, pdf_path}` |
| GET | `/download/{filename}` | – | PDF file |
| GET | `/export-success` | `file` (optional) | HTML |
| GET | `/test-image` | `prompt`, `style` | `{message, path}` |

## 7. Troubleshooting
| Symptom | Fix |
|---------|-----|
| `requirements.txt` not found | `cd` into the folder that contains it (`05_Project_Development_Phase`) |
| `GEMINI_API_KEY is missing` | Create `.env` from `.env.example` and add your key |
| Gemini 404 / model not found | Update model names in `.env` |
| Gemini 429 / quota | Use a Flash model in `GEMINI_PRO_MODELS`, or wait |
| Very slow images | Set `SD_STEPS=15`, `SD_SIZE=384`, or use a GPU |
| `No module named app` | Run `uvicorn` from the folder that contains `app/` |

## 8. Limitations & Future Work
Single user, no accounts, fixed 5 panels. Future: user accounts, comic library, speech-bubble overlay on
images, more panels, cloud deployment.

## 9. Conclusion
ComicCraft shows how LLMs and diffusion models can together turn a simple prompt into a complete,
shareable comic, making comic creation accessible to non-artists.
