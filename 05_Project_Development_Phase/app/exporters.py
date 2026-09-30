"""Step 5 - export the comic as a PDF (fpdf2)."""
import os
from datetime import datetime

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from .config import EXPORT_DIR, FONT_PATH


def _new_pdf() -> tuple[FPDF, str]:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    if FONT_PATH.exists():                       # Unicode font (fpdf2: no uni=True)
        pdf.add_font("DejaVu", "", str(FONT_PATH))
        return pdf, "DejaVu"
    return pdf, "Helvetica"                      # fallback: latin-1 only


def _safe(text: str, font: str) -> str:
    return text if font == "DejaVu" else text.encode("latin-1", "replace").decode("latin-1")


def _write(pdf: FPDF, font: str, size: int, text: str):
    if not text:
        return
    pdf.set_font(font, "", size)
    # new_x/new_y are REQUIRED in fpdf2, otherwise the next multi_cell(0, ...) crashes
    pdf.multi_cell(0, 7, _safe(text, font), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def save_pdf(layout: list[dict]) -> str:
    """Build the PDF, save it with a timestamped name, return the file NAME."""
    pdf, font = _new_pdf()

    for panel in layout:
        pdf.add_page()
        pdf.set_font(font, "", 15)
        pdf.multi_cell(0, 10, _safe(f"Panel {panel['panel']}: {panel['title']}", font),
                       align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        img_w = 140
        if os.path.exists(panel["image_path"]):
            pdf.image(panel["image_path"], x=(pdf.w - img_w) / 2, y=pdf.get_y(), w=img_w, h=img_w)
            pdf.set_y(pdf.get_y() + img_w + 6)
        else:
            _write(pdf, font, 12, "[image missing]")

        _write(pdf, font, 11, panel["scene_description"])
        _write(pdf, font, 12, panel["caption"])
        _write(pdf, font, 12, panel["narration"])
        for line in panel["dialogue"]:
            _write(pdf, font, 12, line)

    filename = f"comic_{datetime.now():%Y%m%d%H%M%S}.pdf"
    pdf.output(str(EXPORT_DIR / filename))
    return filename
