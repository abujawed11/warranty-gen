import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from constants import C_BLACK, C_BORDER, C_YELLOW, C_YELLOW_LIGHT
from models import CertificateData
from pdf_helpers import logo_path, sig_path


def _fmt_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%B-%Y")
    except Exception:
        return date_str


def build_pdf_test(data: CertificateData) -> bytes:
    buf = io.BytesIO()
    page_w, page_h = A4
    cv = canvas.Canvas(buf, pagesize=A4)

    ML = 50
    MR = 50
    CW = page_w - ML - MR

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
    y -= 14

    # ── Ref line ─────────────────────────────────────────────────
    ref_label = f"Ref: QUALITY ASSURANCE DEPARTMENT ({data.tcRefNumber})" if data.tcRefNumber else "Ref: QUALITY ASSURANCE DEPARTMENT"
    cv.setFont("Helvetica-Bold", 9)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, ref_label)
    rw = cv.stringWidth(ref_label, "Helvetica-Bold", 9)
    cv.setStrokeColor(C_BLACK)
    cv.setLineWidth(0.5)
    cv.line(ML, y - 1.5, ML + rw, y - 1.5)

    cv.setFont("Helvetica", 9)
    cv.drawRightString(page_w - MR, y, _fmt_date(data.tcDate))
    y -= 16

    # ── Info box: Customer + Supplier + PO ──────────────────────
    FSIZE   = 9
    LEAD    = 13
    PAD     = 6
    LEFT_W  = CW * 0.55
    DIVX    = ML + LEFT_W
    TEXT_W  = LEFT_W - PAD * 2

    normal_s = ParagraphStyle("n", fontName="Helvetica",      fontSize=FSIZE, leading=LEAD, textColor=C_BLACK)
    bold_s   = ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=FSIZE, leading=LEAD, textColor=C_BLACK)

    def _paras(lines):
        result = []
        for style, text in lines:
            s = bold_s if style == "bold" else normal_s
            p = Paragraph(text.replace("\n", "<br/>"), s)
            _, ph = p.wrap(TEXT_W, 400)
            result.append((p, ph))
        return result

    # Customer content
    cust_lines = []
    if data.tcCustomerName:    cust_lines.append(("bold",   data.tcCustomerName))
    if data.tcCustomerAddress: cust_lines.append(("normal", data.tcCustomerAddress))
    if data.tcCustomerGstin:   cust_lines.append(("normal", f"GSTIN {data.tcCustomerGstin}"))
    if data.tcProjectName:     cust_lines.append(("normal", f"Project Name: {data.tcProjectName}"))
    cust_paras = _paras(cust_lines)

    CUST_LABEL_H = LEAD + PAD
    cust_content  = sum(ph for _, ph in cust_paras) + len(cust_paras) * 2
    CUST_H = max(CUST_LABEL_H + cust_content + PAD * 2, 90)

    # Supplier content
    supp_lines = []
    if data.tcSupplierName:    supp_lines.append(("bold",   data.tcSupplierName + ","))
    if data.tcSupplierAddress: supp_lines.append(("normal", data.tcSupplierAddress))
    if data.tcSupplierGstin:   supp_lines.append(("normal", f"GSTIN: {data.tcSupplierGstin}"))
    supp_paras = _paras(supp_lines)

    SUPP_LABEL_H  = LEAD + PAD
    supp_content  = sum(ph for _, ph in supp_paras) + len(supp_paras) * 2
    SUPP_H = max(SUPP_LABEL_H + supp_content + PAD * 2, 70)
    PO_ROW_H = SUPP_H / 3

    TITLE_H = 26
    BOX_TOP = y
    BOX_H   = TITLE_H + CUST_H + SUPP_H

    # Outer border
    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.8)
    cv.rect(ML, BOX_TOP - BOX_H, CW, BOX_H, fill=0)

    # Title row
    title = "TEST CERTIFICATE"
    cv.setFont("Helvetica-Bold", 13)
    cv.setFillColor(C_BLACK)
    tw = cv.stringWidth(title, "Helvetica-Bold", 13)
    cv.drawString((page_w - tw) / 2, BOX_TOP - TITLE_H + 8, title)
    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.6)
    cv.line(ML, BOX_TOP - TITLE_H, ML + CW, BOX_TOP - TITLE_H)

    # Horizontal divider between customer and supplier
    CUST_BOT = BOX_TOP - TITLE_H - CUST_H
    cv.line(ML, CUST_BOT, ML + CW, CUST_BOT)

    # Vertical divider (left / right columns) — only below customer block
    cv.line(DIVX, CUST_BOT, DIVX, BOX_TOP - BOX_H)

    # PO rows: 3 horizontal lines inside right column
    SUPP_TOP = CUST_BOT
    cv.line(DIVX, SUPP_TOP - PO_ROW_H,     ML + CW, SUPP_TOP - PO_ROW_H)
    cv.line(DIVX, SUPP_TOP - PO_ROW_H * 2, ML + CW, SUPP_TOP - PO_ROW_H * 2)

    # Draw customer content
    cy = BOX_TOP - TITLE_H - PAD
    cv.setFont("Helvetica-Bold", FSIZE)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML + PAD, cy - LEAD, "CUSTOMER:")
    cy -= CUST_LABEL_H
    for p, ph in cust_paras:
        p.drawOn(cv, ML + PAD, cy - ph)
        cy -= ph + 2

    # Draw supplier content
    sy = SUPP_TOP - PAD
    cv.setFont("Helvetica-Bold", FSIZE)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML + PAD, sy - LEAD, "SUPPLIER")
    sy -= SUPP_LABEL_H
    for p, ph in supp_paras:
        p.drawOn(cv, ML + PAD, sy - ph)
        sy -= ph + 2

    # Draw PO info (right column, 3 rows)
    po_items = [
        (f"P.O. No.: {data.tcPoNumber}",     True),
        (f"PO Date : {_fmt_date(data.tcPoDate)}",         False),
        (f"Dispatch Date : {_fmt_date(data.tcDispatchDate)}", False),
    ]
    po_y = SUPP_TOP
    for text, bold in po_items:
        mid = po_y - PO_ROW_H / 2 + FSIZE / 2
        cv.setFont("Helvetica-Bold" if bold else "Helvetica", FSIZE)
        cv.setFillColor(C_BLACK)
        cv.drawString(DIVX + PAD, mid, text)
        po_y -= PO_ROW_H

    y = BOX_TOP - BOX_H - 14

    # ── Material table (same as Format 1) ────────────────────────
    cv.setFont("Helvetica-Bold", 11)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "Details of Material Supplied:")
    lbl_w = cv.stringWidth("Details of Material Supplied:", "Helvetica-Bold", 11)
    cv.setStrokeColor(C_BLACK)
    cv.setLineWidth(0.7)
    cv.line(ML, y - 2, ML + lbl_w, y - 2)
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
            cv.line(cx, y, cx, y - hdr_h)
    y -= hdr_h

    cv.setFillColor(colors.white)
    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.5)
    cv.rect(ML, y - row_h, CW, row_h, fill=1)

    mat_vals = ["1", data.tcMaterialPartName, data.tcQuantityKWp, data.tcRemarks]
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
    y -= row_h + 12

    # ── Chemical Composition table ───────────────────────────────
    NUM_W  = 28
    DESC_W = 140
    ELEM_W = (CW - NUM_W - DESC_W) / 5   # 5 element columns

    chem_hdr1_h = 26
    chem_hdr2_h = 20
    chem_row_h  = 20
    chem_h      = chem_hdr1_h + chem_hdr2_h + chem_row_h

    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.5)
    cv.rect(ML, y - chem_h, CW, chem_h, fill=0)

    # Row 1: label spanning #+ Description columns
    cv.setFont("Helvetica-Bold", 9)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML + NUM_W + PAD, y - 11, "Required / Actual Chemical Composition")
    cv.drawString(ML + NUM_W + PAD, y - 22, "(In %)")
    cv.setStrokeColor(C_BORDER)
    cv.line(ML + NUM_W, y, ML + NUM_W, y - chem_hdr1_h)
    cv.line(ML, y - chem_hdr1_h, ML + CW, y - chem_hdr1_h)

    # Row 2: column headers
    hdr2_top = y - chem_hdr1_h
    chem_cols = [
        (NUM_W,  "#"),
        (DESC_W, "Elements"),
        (ELEM_W, "Si"),
        (ELEM_W, "Mg"),
        (ELEM_W, "Fe"),
        (ELEM_W, "Other"),
        (ELEM_W, "Al"),
    ]
    cx = ML
    for i, (w, lbl) in enumerate(chem_cols):
        cv.setFont("Helvetica-Bold", 9)
        cv.setFillColor(C_BLACK)
        lw = cv.stringWidth(lbl, "Helvetica-Bold", 9)
        cv.drawString(cx + w / 2 - lw / 2, hdr2_top - chem_hdr2_h + 6, lbl)
        if i < len(chem_cols) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.line(cx + w, hdr2_top, cx + w, hdr2_top - chem_hdr2_h)
        cx += w
    cv.setStrokeColor(C_BORDER)
    cv.line(ML, hdr2_top - chem_hdr2_h, ML + CW, hdr2_top - chem_hdr2_h)

    # Data row
    data_top = hdr2_top - chem_hdr2_h
    chem_vals = ["1", "Actual Values", data.tcSi, data.tcMg, data.tcFe, data.tcOther, data.tcAl]
    cx = ML
    for i, ((w, _), v) in enumerate(zip(chem_cols, chem_vals)):
        v = v or ""
        cv.setFont("Helvetica", 9)
        cv.setFillColor(C_BLACK)
        if i <= 1:
            cv.drawString(cx + PAD, data_top - chem_row_h + 6, v)
        else:
            vw = cv.stringWidth(v, "Helvetica", 9)
            cv.drawString(cx + w / 2 - vw / 2, data_top - chem_row_h + 6, v)
        if i < len(chem_cols) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.line(cx + w, data_top, cx + w, data_top - chem_row_h)
        cx += w

    y -= chem_h + 8

    # ── Mechanical Properties table ──────────────────────────────
    mech_hdr_h = 20
    mech_row_h = 20
    mech_h     = mech_hdr_h + mech_row_h

    MECH_VAL_W = ELEM_W * 2
    mech_cols = [
        (NUM_W,               "#"),
        (DESC_W,              "Mechanical Properties"),
        (MECH_VAL_W,          "B.H.N"),
        (CW - NUM_W - DESC_W - MECH_VAL_W, "H.V 10"),
    ]

    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.5)
    cv.rect(ML, y - mech_h, CW, mech_h, fill=0)

    cx = ML
    for i, (w, lbl) in enumerate(mech_cols):
        cv.setFont("Helvetica-Bold", 9)
        cv.setFillColor(C_BLACK)
        lw = cv.stringWidth(lbl, "Helvetica-Bold", 9)
        cv.drawString(cx + w / 2 - lw / 2, y - mech_hdr_h + 6, lbl)
        if i < len(mech_cols) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.line(cx + w, y, cx + w, y - mech_hdr_h)
        cx += w
    cv.setStrokeColor(C_BORDER)
    cv.line(ML, y - mech_hdr_h, ML + CW, y - mech_hdr_h)

    mech_data_top = y - mech_hdr_h
    mech_vals = ["1", "Hardness Actual Values", data.tcBHN, data.tcHV10]
    cx = ML
    for i, ((w, _), v) in enumerate(zip(mech_cols, mech_vals)):
        v = v or ""
        cv.setFont("Helvetica", 9)
        cv.setFillColor(C_BLACK)
        if i <= 1:
            cv.drawString(cx + PAD, mech_data_top - mech_row_h + 6, v)
        else:
            vw = cv.stringWidth(v, "Helvetica", 9)
            cv.drawString(cx + w / 2 - vw / 2, mech_data_top - mech_row_h + 6, v)
        if i < len(mech_cols) - 1:
            cv.setStrokeColor(C_BORDER)
            cv.line(cx + w, mech_data_top, cx + w, mech_data_top - mech_row_h)
        cx += w

    y -= mech_h + 16

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
    y -= 18

    # ── Note ─────────────────────────────────────────────────────
    cv.setFont("Helvetica", 9)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "Note: Material conforms to IS: 733 – 1983")

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
