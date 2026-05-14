import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from constants import C_BLACK, C_BORDER, C_YELLOW, C_YELLOW_LIGHT, TERMS
from models import CertificateData
from pdf_helpers import draw_heading, draw_info_table, fmt_address, logo_path, sig_path


def build_pdf(data: CertificateData) -> bytes:
    buf = io.BytesIO()
    page_w, page_h = A4          # 595.27 × 841.89 pt
    cv = canvas.Canvas(buf, pagesize=A4)

    ML = 50
    MR = 50
    CW = page_w - ML - MR        # ≈ 495 pt

    y = page_h - 38

    # ── Header ──────────────────────────────────────────────────
    logo = logo_path()
    logo_h = 28
    if logo:
        try:
            img    = ImageReader(logo)
            iw, ih = img.getSize()
            logo_w = round((iw / ih) * logo_h)
            cv.drawImage(logo, page_w - MR - logo_w, y - logo_h,
                         width=logo_w, height=logo_h,
                         preserveAspectRatio=True, mask="auto")
        except Exception:
            logo = None

    if not logo:
        cv.setFont("Helvetica-Bold", 20)
        cv.setFillColor(C_BLACK)
        cv.drawRightString(page_w - MR, y - 20, "SUNRACK")

    cv.setFont("Helvetica-Bold", 10.5)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y - 18, "S U N R A C K   T E C H N O L O G I E S")
    y -= 38

    # ── Yellow divider ───────────────────────────────────────────
    cv.setStrokeColor(C_YELLOW)
    cv.setLineWidth(2.5)
    cv.line(ML, y, page_w - MR, y)
    y -= 18

    # ── Title ────────────────────────────────────────────────────
    title = "WARRANTY CERTIFICATE"
    cv.setFont("Helvetica-Bold", 13)
    cv.setFillColor(C_BLACK)
    tw = cv.stringWidth(title, "Helvetica-Bold", 13)
    cv.drawString((page_w - tw) / 2, y, title)
    y -= 16

    # ── Info table ───────────────────────────────────────────────
    billing_full = "\n".join(filter(None, [
        data.billingCustomerName,
        fmt_address(data.billingAddress, data.billingState,
                    data.billingPincode, data.billingCountry),
    ]))
    shipping_full = "\n".join(filter(None, [
        data.shippingCustomerName,
        fmt_address(data.shippingAddress, data.shippingState,
                    data.shippingPincode, data.shippingCountry),
    ]))
    warranty_str = (
        f"{data.warrantyPeriod} from the date of dispatch and as per the terms below"
        if data.warrantyPeriod else ""
    )

    info_rows = [
        ("Name of Customer (Billing):",  billing_full),
        ("Name of Customer (Shipping):", shipping_full),
        ("Date of Dispatch:",            data.dateOfDispatch),
        ("Invoice:",                     data.invoicePONumber),
        ("Warranty Period:",             warranty_str),
    ]

    y = draw_info_table(cv, info_rows, x=ML, y=y, total_w=CW, label_w=158)
    y -= 14

    # ── Material section ─────────────────────────────────────────
    draw_heading(cv, "Details of Material Supplied:", ML, y)
    y -= 16

    col_w   = [28, CW - 28 - 88 - 98, 88, 98]
    hdr_lbl = ["#", "PART NAME", "QTY(kWp)", "Remark's"]
    hdr_h   = 22
    row_h   = 24

    cv.setFillColor(C_YELLOW_LIGHT)
    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.5)
    cv.rect(ML, y - hdr_h, CW, hdr_h, fill=1)

    cx = ML
    for i, (w, h) in enumerate(zip(col_w, hdr_lbl)):
        cv.setFont("Helvetica-Bold", 9.5)
        cv.setFillColor(C_BLACK)
        hw = cv.stringWidth(h, "Helvetica-Bold", 9.5)
        cv.drawString(cx + w / 2 - hw / 2, y - hdr_h + 7, h)
        cx += w
        if i < len(col_w) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.setLineWidth(0.5)
            cv.line(cx, y, cx, y - hdr_h)

    y -= hdr_h

    cv.setFillColor(colors.white)
    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.5)
    cv.rect(ML, y - row_h, CW, row_h, fill=1)

    mat_vals = ["1", data.materialPartName, data.quantityKWp, data.remarks]
    cx = ML
    for i, (w, v) in enumerate(zip(col_w, mat_vals)):
        v = v or ""
        cv.setFont("Helvetica", 10)
        cv.setFillColor(C_BLACK)
        vw = cv.stringWidth(v, "Helvetica", 10)
        cv.drawString(cx + w / 2 - vw / 2, y - row_h + 8, v)
        cx += w
        if i < len(col_w) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.line(cx, y, cx, y - row_h)

    y -= row_h + 14

    # ── Terms ────────────────────────────────────────────────────
    draw_heading(cv, "Standard Terms & Conditions:", ML, y)
    y -= 14

    # Available height = current y minus (sig block 86pt + footer clearance 68pt + loop tail 6pt)
    SIG_H      = 86
    FOOT_CLEAR = 68
    available  = y - 6 - SIG_H - FOOT_CLEAR

    D_LEAD, D_GAP = 13.5, 7
    para_hs = []
    _ms = ParagraphStyle("ms", fontName="Helvetica", fontSize=9, leading=D_LEAD, textColor=C_BLACK)
    for t in TERMS:
        _, ph = Paragraph(t, _ms).wrap(CW, 500)
        para_hs.append(ph)
    total_h = sum(para_hs) + (len(para_hs) - 1) * D_GAP

    if total_h > available > 0:
        r    = available / total_h
        lead = max(10.5, D_LEAD * r)
        gap  = max(3,    D_GAP  * r)
    else:
        lead, gap = D_LEAD, D_GAP

    terms_style = ParagraphStyle(
        "terms", fontName="Helvetica", fontSize=9,
        leading=lead, textColor=C_BLACK,
    )

    for para_text in TERMS:
        para = Paragraph(para_text, terms_style)
        _, ph = para.wrap(CW, 500)
        para.drawOn(cv, ML, y - ph)
        y -= ph + gap

    y -= 6

    # ── Signature block ──────────────────────────────────────────
    cv.setFont("Helvetica-BoldOblique", 10)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "For Sunrack Technologies")
    y -= 14

    sig = sig_path()
    if sig:
        try:
            si         = ImageReader(sig)
            sw, sh     = si.getSize()
            sig_disp_h = 52
            sig_disp_w = round((sw / sh) * sig_disp_h)
            cv.drawImage(sig, ML, y - sig_disp_h,
                         width=sig_disp_w, height=sig_disp_h,
                         preserveAspectRatio=True, mask="auto")
            y -= sig_disp_h + 6
        except Exception:
            y -= 10

    cv.setFont("Helvetica", 10)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "Authorised Signatory")

    # ── Footer bar ───────────────────────────────────────────────
    fy = 28
    cv.setStrokeColor(C_YELLOW)
    cv.setLineWidth(2)
    cv.line(ML, fy + 16, page_w - MR, fy + 16)

    cv.setFont("Helvetica-Bold", 8.5)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, fy,      "SUNRACK TECHNOLOGIES LLP")
    cv.drawString(ML, fy - 11, "BOISAR, PALGHAR")

    cv.save()
    buf.seek(0)
    return buf.read()
