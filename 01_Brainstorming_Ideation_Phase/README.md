# Phase 1 – Brainstorming & Ideation

## 1. Problem Statement
Creating a comic needs writing, drawing and layout skills. Most people have story ideas but cannot draw,
so their ideas never become a finished comic.

## 2. Idea
ComicCraft lets anyone type a short idea (e.g. *"A brave fox exploring an enchanted forest"*) and choose a
character name, setting, tone and art style. AI then produces a complete illustrated comic and a printable PDF.

## 3. Target Users
| User | Need |
|------|------|
| Hobby storytellers / non-artists | Visualise a story without drawing |
| Students & teachers | Illustrated stories for learning material |
| Content creators | Fast comic drafts and storyboards |

## 4. Ideas Considered
| Idea | Decision | Reason |
|------|----------|--------|
| Text-only story generator | ❌ Rejected | No visual appeal |
| Comic generator with a single model | ❌ Rejected | One model cannot do both good writing and images |
| **Gemini (outline + story) + Stable Diffusion (images) + PDF export** | ✅ Selected | Best mix of creativity, quality and low cost |

## 5. Model Selection
| Task | Model | Why |
|------|-------|-----|
| Panel outline (fast, structured JSON) | Gemini **Flash** | Speed + reliable JSON |
| Narration & dialogue (creative) | Gemini **Pro** | Better creative writing |
| Panel illustrations | Stable Diffusion v1.5 | Open, runs locally, well documented |

## 6. Unique Value
- Personalised: 5 inputs shape the whole comic.
- Re-generate with a different tone/art style to iterate.
- One-click PDF export.

## 7. Expected Outcome
A web app where a user goes from idea → 5-panel illustrated comic → PDF in a few minutes.
