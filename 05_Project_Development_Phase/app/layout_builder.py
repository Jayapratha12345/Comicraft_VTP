"""Step 4 - merge outline + story + images into one list of panels."""


def build_comic_layout(images: list[dict], story: list[dict], outline: list[dict]) -> list[dict]:
    story_by_panel = {s.get("panel", i): s for i, s in enumerate(story, start=1)}
    layout = []
    for idx, (img, info) in enumerate(zip(images, outline), start=1):
        text = story_by_panel.get(info.get("panel", idx), {})
        dialogue = text.get("dialogue") or []
        if isinstance(dialogue, str):
            dialogue = [dialogue]
        layout.append({
            "panel": idx,
            "title": info.get("title", f"Panel {idx}"),
            "scene_description": info.get("scene_description", ""),
            "image_path": img["path"],
            "image_url": img["url"],
            "caption": str(text.get("caption", "")),
            "narration": str(text.get("narration", "")),
            "dialogue": [str(d) for d in dialogue],
        })
    return layout
