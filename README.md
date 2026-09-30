# 🎨 ComicCraft – AI Comic Story Creator using Gemini Models

ComicCraft is a FastAPI web app that turns a short story idea into a complete 5-panel comic.
**Gemini Flash** plans the panels, **Gemini Pro** writes narration and dialogue, **Stable Diffusion**
(Hugging Face Diffusers) draws each panel, and the finished comic can be downloaded as a PDF.

## 📁 Project Phases

| # | Phase | Folder |
|---|-------|--------|
| 1 | Brainstorming & Ideation | [`01_Brainstorming_Ideation_Phase`](01_Brainstorming_Ideation_Phase) |
| 2 | Requirement Analysis | [`02_Requirement_Analysis_Phase`](02_Requirement_Analysis_Phase) |
| 3 | Project Design | [`03_Project_Design_Phase`](03_Project_Design_Phase) |
| 4 | Project Planning | [`04_Project_Planning_Phase`](04_Project_Planning_Phase) |
| 5 | Project Development (source code) | [`05_Project_Development_Phase`](05_Project_Development_Phase) |
| 6 | Project Testing | [`06_Project_Testing_Phase`](06_Project_Testing_Phase) |
| 7 | Project Documentation | [`07_Project_Documentation_Phase`](07_Project_Documentation_Phase) |
| 8 | Project Demonstration | [`08_Project_Demonstration_Phase`](08_Project_Demonstration_Phase) |

## ⚙️ Tech Stack
FastAPI · Uvicorn · Jinja2 · Google Gemini (`google-genai`) · Hugging Face Diffusers · PyTorch · fpdf2

## 🚀 Quick Start
```bash
git clone https://github.com/<your-username>/ComicCraft-AI-Comic-Creator.git
cd ComicCraft-AI-Comic-Creator/05_Project_Development_Phase
python -m venv env
env\Scripts\activate            # macOS/Linux: source env/bin/activate
pip install -r requirements.txt
copy .env.example .env          # macOS/Linux: cp .env.example .env  -> add your GEMINI_API_KEY
uvicorn app.main:app --reload
```
Open <http://127.0.0.1:8000> (API docs at `/docs`).

## 👥 Team
- [Your Name] – [Roll no. / Role]

> Built as part of the SmartBridge / SmartInternz program.
