import io
import os

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request model ─────────────────────────────────────────────────────────────

class CertificateData(BaseModel):
    billingCustomerName: str = ""
    billingAddress: str = ""
    billingState: str = ""
    billingPincode: str = ""
    billingCountry: str = ""
    shippingCustomerName: str = ""
    shippingAddress: str = ""
    shippingState: str = ""
    shippingPincode: str = ""
    shippingCountry: str = ""
    dateOfDispatch: str = ""
    invoicePONumber: str = ""
    warrantyPeriod: str = ""
    materialPartName: str = ""
    quantityKWp: str = ""
    remarks: str = ""

# ── Constants ─────────────────────────────────────────────────────────────────

C_YELLOW       = colors.HexColor("#F5C200")
C_BLACK        = colors.HexColor("#1A1A1A")
C_YELLOW_LIGHT = colors.HexColor("#FFF8D6")
C_BORDER       = colors.HexColor("#AAAAAA")
C_ORANGE       = colors.HexColor("#C8860A")

TERMS = [
    "M/s Sunrack Technologies, only provides the warranty against manufacturing "
    "defects and workmanship on the products supplied. Sunrack will, at its option, "
    "either repair the defect or replace the defective product or part there of with "
    "a new or remanufactured equivalent at cost within 15 working days of intimation.",

    "Sunrack’s total liability here under for such repair of replacement shall not "
    "exceed the original purchase price of the product. This will not provide the warranty "
    "replacements for structure products going faulty while operating due to conditions "
    "beyond specifications, improper installation, improper site conditions and/or act of "
    "god, cosmetic damage, damage from accident, negligence same shall not be covered under "
    "warranty and the service would be provided on chargeable basis as per mutual agreement",

    "Any failure/damage arising out of improper unloading, stacking or moving to the site "
    "will not be covered under warranty.",

    "In the event of any non-payment issues, this warranty becomes null and void. Shall also "
    "be void if the product has been modified, repaired, or reworked in a manner not previously "
    "authorized by Sunrack in writing.",

    "Warranty shall not cover the consumable items & accessories supplied with viz. M8 Allen "
    "Bolt + Nut, tapered upper foot. Sunrack is not responsible for delay in delivering the "
    "warranty service/spares due to natural calamity or force majeure condition.",

    "The foregoing warranties are in addition of all other warranties, whether express or implied "
    "and Sunrack does not make any warranty of Merchant ability or any warranty for fitness for a "
    "particular purpose. In no event, Sunrack be liable for or responsible to purchaser or any "
    "other party for any consequential, incidental or other damages, losses or expenses arising in "
    "connection with the use of or the inability to use the product.",

    "All Claims related to this Warranty are subjected to Indian Law.",
]

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend", "public"))

# ── Helpers ───────────────────────────────────────────────────────────────────

def _asset(name: str) -> str | None:
    p = os.path.join(PUBLIC_DIR, name)
    return p if os.path.exists(p) else None


def _logo_path() -> str | None:
    return _asset("logo.png") or _asset("logo.jpg") or _asset("logo.svg")


def _sig_path() -> str | None:
    return _asset("signature.png") or _asset("signature.jpg")


def _fmt_address(address, state, pincode, country) -> str:
    return ", ".join(p for p in [address, state, pincode, country] if p and p.strip())


def _draw_heading(c: canvas.Canvas, text: str, x: float, y: float, size: float = 11):
    """Bold underlined section heading."""
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(C_BLACK)
    c.drawString(x, y, text)
    w = c.stringWidth(text, "Helvetica-Bold", size)
    c.setStrokeColor(C_BLACK)
    c.setLineWidth(0.7)
    c.line(x, y - 2, x + w, y - 2)


def _draw_info_table(
    c: canvas.Canvas,
    rows: list[tuple[str, str]],
    x: float, y: float,
    total_w: float, label_w: float,
    fsize: float = 10,
) -> float:
    """
    Draw the bordered certificate info table.
    Returns the y position immediately below the table.
    """
    pad  = 6
    lh   = fsize + 4   # paragraph leading

    val_style = ParagraphStyle(
        "val",
        fontName="Helvetica",
        fontSize=fsize,
        leading=lh,
        textColor=C_BLACK,
    )

    # Pre-compute each row's height
    row_meta: list[tuple[str, str, float, float]] = []  # label, value, row_h, para_h
    value_w = total_w - label_w - pad * 2
    for label, value in rows:
        if value:
            para = Paragraph(value.replace("\n", "<br/>"), val_style)
            _, ph = para.wrap(value_w, 300)
        else:
            ph = lh
        row_h = max(ph + pad * 2, 22)
        row_meta.append((label, value, row_h, ph))

    table_h = sum(r[2] for r in row_meta)

    # Outer border
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.6)
    c.rect(x, y - table_h, total_w, table_h, fill=0)

    # Vertical divider (label | value)
    c.line(x + label_w, y, x + label_w, y - table_h)

    cur_y = y
    for i, (label, value, row_h, ph) in enumerate(row_meta):
        # Horizontal divider between rows (not before first row)
        if i > 0:
            c.setStrokeColor(C_BORDER)
            c.setLineWidth(0.6)
            c.line(x, cur_y, x + total_w, cur_y)

        # Label — bold, top-aligned
        c.setFont("Helvetica-Bold", fsize)
        c.setFillColor(C_BLACK)
        c.drawString(x + pad, cur_y - pad - fsize, label)

        # Value — paragraph, top-aligned
        if value:
            para = Paragraph(value.replace("\n", "<br/>"), val_style)
            para.wrap(value_w, 300)
            para.drawOn(c, x + label_w + pad, cur_y - pad - ph)

        cur_y -= row_h

    return cur_y   # y just below the table


# ── PDF builder ───────────────────────────────────────────────────────────────

def build_pdf(data: CertificateData) -> bytes:
    buf = io.BytesIO()
    page_w, page_h = A4          # 595.27 × 841.89 pt
    cv = canvas.Canvas(buf, pagesize=A4)

    ML = 50                       # left margin
    MR = 50                       # right margin
    CW = page_w - ML - MR         # content width ≈ 495 pt

    y = page_h - 38               # start near top

    # ── Header ──────────────────────────────────────────────
    logo = _logo_path()
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
        # Text fallback
        cv.setFont("Helvetica-Bold", 20)
        cv.setFillColor(C_BLACK)
        cv.drawRightString(page_w - MR, y - 20, "SUNRACK")

    cv.setFont("Helvetica-Bold", 10.5)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y - 18, "S U N R A C K   T E C H N O L O G I E S")

    y -= 38

    # ── Yellow divider ───────────────────────────────────────
    cv.setStrokeColor(C_YELLOW)
    cv.setLineWidth(2.5)
    cv.line(ML, y, page_w - MR, y)
    y -= 18

    # ── Title ────────────────────────────────────────────────
    title = "WARRANTY CERTIFICATE"
    cv.setFont("Helvetica-Bold", 13)
    cv.setFillColor(C_BLACK)
    tw = cv.stringWidth(title, "Helvetica-Bold", 13)
    cv.drawString((page_w - tw) / 2, y, title)
    y -= 16

    # ── Info table ───────────────────────────────────────────
    billing_full = "\n".join(filter(None, [
        data.billingCustomerName,
        _fmt_address(data.billingAddress, data.billingState,
                     data.billingPincode, data.billingCountry),
    ]))
    shipping_full = "\n".join(filter(None, [
        data.shippingCustomerName,
        _fmt_address(data.shippingAddress, data.shippingState,
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

    y = _draw_info_table(cv, info_rows, x=ML, y=y,
                         total_w=CW, label_w=158)
    y -= 14

    # ── Material section ─────────────────────────────────────
    _draw_heading(cv, "Details of Material Supplied:", ML, y)
    y -= 16

    # Columns: # | PART NAME | QTY(kWp) | Remark's
    col_w   = [28, CW - 28 - 88 - 98, 88, 98]
    hdr_lbl = ["#", "PART NAME", "QTY(kWp)", "Remark’s"]
    hdr_h   = 22
    row_h   = 24

    # Header row
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

    # Data row
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

    # ── Terms ────────────────────────────────────────────────
    _draw_heading(cv, "Standard Terms & Conditions:", ML, y)
    y -= 14

    terms_style = ParagraphStyle(
        "terms",
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=C_BLACK,
    )

    for para_text in TERMS:
        para = Paragraph(para_text, terms_style)
        _, ph = para.wrap(CW, 500)
        if y - ph < 90:          # page break if not enough room
            cv.showPage()
            y = page_h - 50
        para.drawOn(cv, ML, y - ph)
        y -= ph + 7

    y -= 6

    # ── Signature block ──────────────────────────────────────
    cv.setFont("Helvetica-BoldOblique", 10)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "For Sunrack Technologies")
    y -= 14

    sig = _sig_path()
    if sig:
        try:
            si       = ImageReader(sig)
            sw, sh   = si.getSize()
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

    # ── Footer bar ───────────────────────────────────────────
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


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "FastAPI Running"}


@app.post("/api/generate-certificate")
def generate_certificate_json(data: CertificateData):
    """JSON endpoint — used for programmatic access."""
    return _pdf_response(data)


@app.post("/api/download-certificate")
def generate_certificate_form(
    billingCustomerName:  str = Form(""),
    billingAddress:       str = Form(""),
    billingState:         str = Form(""),
    billingPincode:       str = Form(""),
    billingCountry:       str = Form(""),
    shippingCustomerName: str = Form(""),
    shippingAddress:      str = Form(""),
    shippingState:        str = Form(""),
    shippingPincode:      str = Form(""),
    shippingCountry:      str = Form(""),
    dateOfDispatch:       str = Form(""),
    invoicePONumber:      str = Form(""),
    warrantyPeriod:       str = Form(""),
    materialPartName:     str = Form(""),
    quantityKWp:          str = Form(""),
    remarks:              str = Form(""),
):
    """Form-data endpoint — used by the frontend hidden-form download."""
    data = CertificateData(
        billingCustomerName=billingCustomerName,
        billingAddress=billingAddress,
        billingState=billingState,
        billingPincode=billingPincode,
        billingCountry=billingCountry,
        shippingCustomerName=shippingCustomerName,
        shippingAddress=shippingAddress,
        shippingState=shippingState,
        shippingPincode=shippingPincode,
        shippingCountry=shippingCountry,
        dateOfDispatch=dateOfDispatch,
        invoicePONumber=invoicePONumber,
        warrantyPeriod=warrantyPeriod,
        materialPartName=materialPartName,
        quantityKWp=quantityKWp,
        remarks=remarks,
    )
    return _pdf_response(data)


def _pdf_response(data: CertificateData):
    pdf_bytes = build_pdf(data)
    pdf_bytes = build_pdf(data)

    safe = "".join(
        ch for ch in (data.billingCustomerName or "Certificate")
        if ch.isalnum() or ch in " _-"
    ).strip() or "Certificate"
    filename = f"Warranty_Certificate_{safe}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
