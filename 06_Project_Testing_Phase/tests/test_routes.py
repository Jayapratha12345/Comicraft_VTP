"""Route tests. AI calls are replaced by a fake pipeline, so no API key / GPU is needed."""
import pytest
from fastapi.testclient import TestClient

from app import routes
from app.main import app

client = TestClient(app)

FAKE_LAYOUT = [{
    "panel": 1, "title": "Forest Edge", "scene_description": "A fox at dusk",
    "image_path": "x.png", "image_url": "/static/panels/x.png",
    "caption": "Caption", "narration": "Narration", "dialogue": ["Free: Let's go"],
}]
FORM = {"prompt": "A fox in a forest", "character_name": "Free",
        "setting": "forest", "tone": "dramatic", "style": "anime"}


@pytest.fixture
def fake_pipeline(monkeypatch):
    monkeypatch.setattr(routes, "run_pipeline", lambda *a, **k: (FAKE_LAYOUT, "comic_test.pdf"))


def test_home_page_loads():
    r = client.get("/")
    assert r.status_code == 200 and "Create Your Comic" in r.text


def test_generate_shows_preview(fake_pipeline):
    r = client.post("/generate", data=FORM)
    assert r.status_code == 200
    assert "Forest Edge" in r.text and "/download/comic_test.pdf" in r.text


def test_generate_json(fake_pipeline):
    r = client.post("/generate-comic/json", json={"prompt": "A fox"})
    assert r.status_code == 200
    assert r.json()["pdf_path"] == "/download/comic_test.pdf"


def test_pipeline_error_is_shown_on_form(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("GEMINI_API_KEY is missing")
    monkeypatch.setattr(routes, "run_pipeline", boom)
    r = client.post("/generate", data=FORM)
    assert r.status_code == 500 and "GEMINI_API_KEY is missing" in r.text


def test_missing_form_field_is_rejected():
    assert client.post("/generate", data={"prompt": "only prompt"}).status_code == 422


def test_export_success_page():
    r = client.get("/export-success", params={"file": "comic_test.pdf"})
    assert r.status_code == 200 and "Exported Successfully" in r.text


@pytest.mark.parametrize("name", ["../.env", "secret.txt", "comic_nothere.pdf"])
def test_download_blocks_bad_or_missing_files(name):
    assert client.get(f"/download/{name}").status_code == 404
