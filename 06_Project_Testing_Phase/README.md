# Phase 6 – Project Testing

## 1. Automated Tests
Run from this folder:
```bash
pip install -r requirements-test.txt
pip install -r ../05_Project_Development_Phase/requirements.txt
pytest -v
```
| File | What it checks |
|------|----------------|
| `tests/test_layout_builder.py` | Panels are merged correctly; missing/odd story data doesn't crash |
| `tests/test_routes.py` | Home page, `/generate`, JSON API, error display, validation (422), export page, download path-traversal protection |

AI calls are mocked in the route tests, so they run without an API key or GPU.

## 2. Manual Test Cases (end-to-end, real models)
Fill in the **Actual result / Status** columns after you run each case, and attach screenshots to Phase 8.

| ID | Test | Steps | Expected result | Actual result | Status |
|----|------|-------|-----------------|---------------|--------|
| TC-01 | Home page | Open `http://127.0.0.1:8000` | Form with 5 fields is shown | | |
| TC-02 | Default comic | Submit the default fox prompt | 5 panels with images, text, dialogue | | |
| TC-03 | Change tone/style | Choose *funny* + *comic book*, submit | New story/images in the new mood and style | | |
| TC-04 | PDF download | Click *Download Your Comic as PDF* | PDF downloads (5 pages), then success page opens | | |
| TC-05 | Export success | Click *Go Create Another Comic* | Returns to the form | | |
| TC-06 | JSON API | POST `/generate-comic/json` from `/docs` | JSON with `layout` and `pdf_path` | | |
| TC-07 | Test image | GET `/test-image` | JSON with an image path; image opens | | |
| TC-08 | Missing API key | Remove `GEMINI_API_KEY`, submit | Readable error shown on the form | | |
| TC-09 | Empty field | Clear the prompt, submit | Browser blocks submit (required field) | | |

## 3. Bugs Found & Fixed
| # | Problem | Cause | Fix |
|---|---------|-------|-----|
| 1 | 404 model not found | `gemini-1.5-*` models retired | Configurable model list with fallback (`.env`) |
| 2 | Stable Diffusion download fails | `runwayml/...` repo removed | Use `stable-diffusion-v1-5/stable-diffusion-v1-5` |
| 3 | Image save error | Filename built from prompt, no `.png` | Short random filename with `.png` |
| 4 | PDF crash | `fpdf` API (`uni=True`, cursor position) | Use `fpdf2` with `new_x` / `new_y` |
| 5 | Template error | Old `TemplateResponse` signature | `TemplateResponse(request, name, context)` |
| 6 | Images not shown / wrong paths | Relative paths, no static mount | Absolute paths + `/static` mount |
| 7 | Story/panel mismatch | Splitting text on `**Panel` | Gemini Pro returns JSON per panel |
