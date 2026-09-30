from app.layout_builder import build_comic_layout


def _data(n=5):
    outline = [{"panel": i, "title": f"Title {i}", "scene_description": "scene", "image_prompt": "p"}
               for i in range(1, n + 1)]
    story = [{"panel": i, "caption": "cap", "narration": "nar", "dialogue": ["Fox: hi"]}
             for i in range(1, n + 1)]
    images = [{"path": f"/tmp/{i}.png", "url": f"/static/panels/{i}.png"} for i in range(n)]
    return images, story, outline


def test_layout_has_one_entry_per_panel():
    layout = build_comic_layout(*_data())
    assert len(layout) == 5
    assert [p["panel"] for p in layout] == [1, 2, 3, 4, 5]


def test_layout_merges_text_and_image():
    first = build_comic_layout(*_data())[0]
    assert first["title"] == "Title 1"
    assert first["image_url"] == "/static/panels/0.png"
    assert first["narration"] == "nar" and first["dialogue"] == ["Fox: hi"]


def test_missing_story_panel_does_not_crash():
    images, story, outline = _data()
    layout = build_comic_layout(images, story[:3], outline)   # story shorter than outline
    assert layout[4]["narration"] == ""


def test_dialogue_string_is_converted_to_list():
    images, story, outline = _data(1)
    story[0]["dialogue"] = "Fox: hello"
    assert build_comic_layout(images, story, outline)[0]["dialogue"] == ["Fox: hello"]
