# Phase 2 – Requirement Analysis

## 1. Functional Requirements
| ID | Requirement |
|----|-------------|
| FR-1 | User enters story prompt, character name, setting, tone and art style in a web form |
| FR-2 | System generates a 5-panel outline (title, scene description, image prompt) |
| FR-3 | System writes caption, narration and dialogue for every panel |
| FR-4 | System generates one image per panel in the chosen art style |
| FR-5 | User can preview the comic panel-by-panel in the browser |
| FR-6 | User can download the comic as a timestamped PDF |
| FR-7 | An export-success page confirms the download |
| FR-8 | A JSON API endpoint (`/generate-comic/json`) allows programmatic use |
| FR-9 | A `/test-image` endpoint lets developers test image generation alone |
| FR-10 | Errors (bad key, model failure) are shown clearly to the user |

## 2. Non-Functional Requirements
| ID | Requirement |
|----|-------------|
| NFR-1 | Usable by non-technical users; simple single-page form |
| NFR-2 | API keys stored in `.env`, never in source code or Git |
| NFR-3 | Server stays responsive during generation (blocking work runs in a thread pool) |
| NFR-4 | Model names configurable, because providers retire models often |
| NFR-5 | Runs locally on Windows / macOS / Linux (GPU optional) |

## 3. Software Requirements
| Item | Version / Detail |
|------|------------------|
| Python | 3.10+ |
| Framework | FastAPI, Uvicorn, Jinja2, python-multipart |
| AI | `google-genai`, `diffusers`, `transformers`, `torch`, `accelerate` |
| PDF | `fpdf2` |
| Others | Pillow, python-dotenv |

## 4. Hardware Requirements
| Setup | Notes |
|-------|-------|
| Minimum | 8 GB RAM, ~10 GB free disk (Stable Diffusion weights ≈ 4 GB); CPU works but is slow (minutes per image) |
| Recommended | NVIDIA GPU with 6 GB+ VRAM (seconds per image) |

## 5. External Requirements
- Google Gemini API key (from Google AI Studio)
- Internet on first run (downloads model weights from Hugging Face)

## 6. Constraints & Assumptions
- Single-user local deployment; no login or database.
- Comics are always 5 panels.
- AI output can vary; JSON responses are validated before use.
