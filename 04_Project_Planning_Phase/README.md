# Phase 4 – Project Planning

## 1. Milestones
| Milestone | Activities | Deliverable |
|-----------|-----------|-------------|
| M1 – Model selection & architecture | Research models, define architecture, set up environment | Model choice, folder structure, venv |
| M2 – Core functionality | Outline, story, image, layout and PDF functions | Working `app/*.py` modules |
| M3 – Routes | Write `routes.py` (form, JSON, export, test-image) | Working endpoints |
| M4 – Frontend | HTML/CSS pages + Jinja2 binding | `index`, `comic_preview`, `export_success` |
| M5 – Deployment & testing | Local deployment, end-to-end verification | Running app on `127.0.0.1:8000` |
| M6 – Documentation & demo | README, phase documents, screenshots/video | This repository |

## 2. Task Breakdown
| Task | Owner | Status |
|------|-------|--------|
| Choose Gemini + Stable Diffusion models | [Name] | ✅ Done |
| Build AI modules | [Name] | ✅ Done |
| Build FastAPI routes | [Name] | ✅ Done |
| Build templates | [Name] | ✅ Done |
| Test & fix runtime errors | [Name] | ✅ Done |
| Documentation & GitHub upload | [Name] | 🔄 In progress |

## 3. Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Gemini model gets retired (404) | App fails | Model names in `.env` with fallback list |
| Gemini quota / rate limit (429) | Generation fails | Use a Flash model for both steps; retry later |
| Slow image generation on CPU | Long waits | Fewer steps / smaller size via `.env`; GPU recommended |
| Gemini returns invalid JSON | Crash | JSON mode + validation + clear error page |
| API key leaked to GitHub | Security | `.env` in `.gitignore`; only `.env.example` committed |

## 4. Tools
Python, VS Code, Git/GitHub, Uvicorn, Google AI Studio, Hugging Face.
