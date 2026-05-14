import os

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from constants import C_BLACK, C_BORDER, PUBLIC_DIR


def _asset(name: str) -> str | None:
    p = os.path.join(PUBLIC_DIR, name)
    return p if os.path.exists(p) else None


def logo_path() -> str | None:
    return _asset("logo.png") or _asset("logo.jpg") or _asset("logo.svg")


def sig_path() -> str | None:
    return _asset("signature.png") or _asset("signature.jpg")


def fmt_address(address: str, state: str, pincode: str, country: str) -> str:
    return ", ".join(p for p in [address, state, pincode, country] if p and p.strip())


def draw_heading(c: canvas.Canvas, text: str, x: float, y: float, size: float = 11):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(C_BLACK)
    c.drawString(x, y, text)
    w = c.stringWidth(text, "Helvetica-Bold", size)
    c.setStrokeColor(C_BLACK)
    c.setLineWidth(0.7)
    c.line(x, y - 2, x + w, y - 2)


def draw_info_table(
    c: canvas.Canvas,
    rows: list[tuple[str, str]],
    x: float, y: float,
    total_w: float, label_w: float,
    fsize: float = 10,
) -> float:
    """Draw the bordered certificate info table. Returns y immediately below the table."""
    pad = 6
    lh  = fsize + 4

    val_style = ParagraphStyle(
        "val", fontName="Helvetica", fontSize=fsize,
        leading=lh, textColor=C_BLACK,
    )

    row_meta: list[tuple[str, str, float, float]] = []
    value_w = total_w - label_w - pad * 2
    for label, value in rows:
        if value:
            _, ph = Paragraph(value.replace("\n", "<br/>"), val_style).wrap(value_w, 300)
        else:
            ph = lh
        row_h = max(ph + pad * 2, 22)
        row_meta.append((label, value, row_h, ph))

    table_h = sum(r[2] for r in row_meta)

    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.rect(x, y - table_h, total_w, table_h, fill=0)
    c.line(x + label_w, y, x + label_w, y - table_h)

    cur_y = y
    for i, (label, value, row_h, ph) in enumerate(row_meta):
        if i > 0:
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.6)
            c.line(x, cur_y, x + total_w, cur_y)

        c.setFont("Helvetica-Bold", fsize)
        c.setFillColor(C_BLACK)
        c.drawString(x + pad, cur_y - pad - fsize, label)

        if value:
            para = Paragraph(value.replace("\n", "<br/>"), val_style)
            para.wrap(value_w, 300)
            para.drawOn(c, x + label_w + pad, cur_y - pad - ph)

        cur_y -= row_h

    return cur_y
