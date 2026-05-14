import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
)

from constants import C_BLACK, C_BORDER, C_YELLOW
from models import CertificateData
from pdf_helpers import logo_path, sig_path

PW, PH = A4
ML, MR = 50, 50
CW = PW - ML - MR

_HEADER_RESERVED = 62
_FOOTER_RESERVED = 32


def _draw_page(cv, doc):
    cv.saveState()

    # ── Header box ──────────────────────────────────────────
    hbox_top = PH - 10
    hbox_h   = 42
    hbox_bot = hbox_top - hbox_h

    cv.setStrokeColor(C_BORDER)
    cv.setLineWidth(0.8)
    cv.rect(ML, hbox_bot, CW, hbox_h, fill=0)

    cv.setFont("Helvetica-Bold", 12)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML + 8, hbox_bot + 14, "S U N R A C K   T E C H N O L O G I E S")

    logo = logo_path()
    if logo:
        try:
            img = ImageReader(logo)
            iw, ih = img.getSize()
            lh = 28
            lw = round((iw / ih) * lh)
            cv.drawImage(logo, PW - MR - lw - 8, hbox_bot + 7,
                         width=lw, height=lh,
                         preserveAspectRatio=True, mask="auto")
        except Exception:
            pass

    # Yellow line below header box
    cv.setStrokeColor(C_YELLOW)
    cv.setLineWidth(2.5)
    cv.line(ML, hbox_bot - 3, PW - MR, hbox_bot - 3)

    # ── Footer ──────────────────────────────────────────────
    fy = 18
    cv.setStrokeColor(C_YELLOW)
    cv.setLineWidth(1.5)
    cv.line(ML, fy + 14, PW - MR, fy + 14)

    cv.setFont("Helvetica-Bold", 7.5)
    cv.setFillColor(C_BLACK)
    cv.drawString(ML, fy, "SUNRACK TECHNOLOGIES LLP, BOISAR, PALGHAR")

    cv.restoreState()


def build_pdf_v2(data: CertificateData) -> bytes:
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=ML,
        rightMargin=MR,
        topMargin=_HEADER_RESERVED + 8,
        bottomMargin=_FOOTER_RESERVED + 10,
    )

    # ── Styles ──────────────────────────────────────────────
    normal = ParagraphStyle(
        "n2", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=C_BLACK, spaceAfter=3,
    )
    sec_heading = ParagraphStyle(
        "sh2", fontName="Helvetica-Bold", fontSize=10, leading=15,
        textColor=C_BLACK, spaceBefore=8, spaceAfter=3,
    )
    subheading = ParagraphStyle(
        "sbh2", fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=C_BLACK, spaceAfter=2,
    )
    bullet_s = ParagraphStyle(
        "blt2", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=C_BLACK, leftIndent=16, spaceAfter=3,
    )
    title_s = ParagraphStyle(
        "ttl2", fontName="Helvetica-Bold", fontSize=13, leading=18,
        textColor=C_BLACK, alignment=1, spaceBefore=0, spaceAfter=8,
    )
    tbl_label = ParagraphStyle(
        "tl2", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=C_BLACK,
    )
    tbl_value = ParagraphStyle(
        "tv2", fontName="Helvetica", fontSize=9, leading=12, textColor=C_BLACK,
    )
    issued_bold = ParagraphStyle(
        "isb2", fontName="Helvetica-Bold", fontSize=9.5, leading=14, textColor=C_BLACK,
    )
    issued_norm = ParagraphStyle(
        "isn2", fontName="Helvetica", fontSize=9.5, leading=14, textColor=C_BLACK,
    )

    # ── Story ───────────────────────────────────────────────
    story = []

    # Title
    story.append(Paragraph("WARRANTY CERTIFICATE", title_s))

    # Info table
    LABEL_W = 155
    VALUE_W = CW - LABEL_W

    rows = [
        ("PROJECT NAME",        data.f2ProjectName),
        ("CLIENT",              data.f2Client),
        ("SOLAR CONSULTANT",    data.f2SolarConsultant),
        ("SOLAR DEVELOPER",     data.f2SolarDeveloper),
        ("MAIN CONTRACTOR",     data.f2MainContractor),
        ("LOCATION",            data.f2Location),
        ("PRODUCT DESCRIPTION", data.f2ProductDescription),
        ("PRODUCT WARRANTY",    data.f2ProductWarranty),
        ("DESIGN WARRANTY",     data.f2DesignWarranty),
        ("WARRANTY PERIOD",     data.f2WarrantyPeriodNote),
    ]
    tbl_data = [
        [Paragraph(lbl, tbl_label), Paragraph(val or "", tbl_value)]
        for lbl, val in rows
    ]
    tbl = Table(tbl_data, colWidths=[LABEL_W, VALUE_W])
    tbl.setStyle(TableStyle([
        ("GRID",          (0, 0), (-1, -1), 0.6, C_BORDER),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8))

    # Intro
    story.append(Paragraph("<b>M/s Sunrack Technologies</b>", subheading))
    story.append(Paragraph(
        'This Warranty Certificate (“Warranty”) is issued by <b>M/s Sunrack Technologies</b>, '
        'hereinafter referred to as <b>“Sunrack”</b>, for its solar structure products '
        '(“Product”) supplied to the customer.',
        normal,
    ))
    story.append(Spacer(1, 4))

    # Section 1
    story.append(Paragraph("<b>1. Warranty Coverage</b>", sec_heading))
    story.append(Paragraph(
        'Sunrack provides this warranty solely against <b>manufacturing defects and workmanship</b> '
        'in the products supplied.', normal,
    ))
    story.append(Paragraph('In the event of a valid claim, Sunrack shall, at its sole discretion:', normal))
    story.append(Paragraph('• Repair the defective component; or', bullet_s))
    story.append(Paragraph('• Replace the defective product or part with a new or remanufactured equivalent.', bullet_s))
    story.append(Paragraph(
        'Such action will be taken <b>within 15 (fifteen) working days</b> from the date of written '
        'intimation and acknowledgment by Sunrack.', normal,
    ))
    story.append(Paragraph(
        "Sunrack's <b>total liability</b> for such repair or replacement shall <b>not exceed the "
        "original purchase price</b> of the product in question.", normal,
    ))
    story.append(Paragraph(
        'Warranty is directly transferred from the raw material supplier Arcelor Mittal/Nalco and '
        'will be adhered to the documentation provided for C5 level corrosion.', normal,
    ))
    story.append(Spacer(1, 4))

    # Section 2
    story.append(Paragraph("<b>2. Exclusions from Warranty</b>", sec_heading))
    story.append(Paragraph(
        'This warranty shall be deemed <b>void</b> and <b>not applicable</b> in the following cases:', normal,
    ))
    for item in [
        'Structural failures arising from conditions beyond product specifications, improper installation, '
        'unsuitable site conditions, or environmental stressors not accounted for in the original design.',
        'Damage caused by <b>Acts of God</b> such as earthquakes, floods, storms, lightning, or other natural disasters.',
        'Cosmetic wear and tear including rust, discoloration, surface blemishes, or fading that does not impact structural integrity.',
        'Physical damage resulting from <b>accidents, negligence, third-party handling</b>, or improper maintenance.',
        'Any damage arising during <b>unloading, stacking, or site transportation</b>, unless handled by Sunrack or its authorized representatives.',
        '<b>Unauthorized modifications, reworking, or repairs</b> carried out without prior written approval from Sunrack.',
        'Non-compliance with recommended installation manuals or engineering drawings.',
        'Warranty shall be rendered <b>null and void</b> in case of <b>non-payment or partial payment</b> of agreed dues.',
        'Service delays due to <b>force majeure conditions</b>, including strikes, supply chain disruptions, or government regulations.',
    ]:
        story.append(Paragraph(f'• {item}', bullet_s))
    story.append(Spacer(1, 4))

    # Section 3
    story.append(Paragraph("<b>3. Exclusions of Consumables and Accessories</b>", sec_heading))
    story.append(Paragraph(
        'This warranty <b>does not cover</b> the following items, which are considered consumables or ancillary parts:', normal,
    ))
    for item in [
        '<b>Bolts, nuts, fasteners, clamps, washers, rivets</b>, and similar hardware items.',
        '<b>Cable trays, conduit supports, wire management clips</b>, and accessories unless specified otherwise in writing.',
        '<b>Packaging material</b>, wooden pallets, wrapping film, or protective foam used during transport.',
        'Items provided by third-party vendors or procured locally by the client, even if recommended by Sunrack.',
        '<b>Accessories not manufactured by Sunrack</b>, even if supplied as part of the package.',
    ]:
        story.append(Paragraph(f'• {item}', bullet_s))
    story.append(Paragraph(
        "All these items are excluded from warranty and shall be replaced or maintained at the customer's cost.", normal,
    ))
    story.append(Spacer(1, 4))

    # Section 4
    story.append(Paragraph("<b>4. Limitation of Liability</b>", sec_heading))
    for item in [
        "Sunrack's responsibility is strictly limited to the <b>repair or replacement of defective parts</b> as defined under this warranty.",
        '<b>No claims will be entertained</b> for project delays, indirect losses, or business interruptions resulting from the failure or delay of any Sunrack product.',
        'Sunrack shall not be liable for <b>loss of revenue, loss of contracts, loss of data, or third-party liabilities</b> incurred by the purchaser.',
        'The purchaser shall indemnify and hold Sunrack harmless from any claims arising due to improper installation or misuse.',
        'Sunrack shall not be held responsible for <b>electrical, civil, or mechanical failures</b> in systems integrated with Sunrack structures, which are outside the design scope.',
        'This warranty does <b>not cover logistics, handling, removal, or reinstallation costs</b> at the site unless specifically agreed in writing.',
        'Sunrack makes <b>no express or implied warranties</b> beyond those stated herein, including but not limited to warranties of merchantability or fitness for a particular purpose.',
        "In no event shall Sunrack's total liability exceed the original invoice value of the product supplied under this warranty.",
    ]:
        story.append(Paragraph(f'• {item}', bullet_s))
    story.append(Spacer(1, 4))

    # Section 5
    story.append(Paragraph("<b>5. Governing Law</b>", sec_heading))
    story.append(Paragraph(
        'All claims, disputes, or legal proceedings arising from or relating to this Warranty shall be '
        'governed by and construed in accordance with the <b>laws of the Republic of India</b>. '
        'The competent courts of <b>Mumbai, India</b> shall have exclusive jurisdiction.',
        normal,
    ))
    story.append(Spacer(1, 12))

    # Issued By / Signature block
    story.append(Paragraph("<b>Issued By:</b>", issued_bold))
    story.append(Paragraph("<b>M/s Sunrack Technologies</b>", issued_bold))
    story.append(Paragraph("Authorized Signatory", issued_norm))

    sig = sig_path()
    if sig:
        try:
            si = ImageReader(sig)
            sw, sh = si.getSize()
            sig_h = 52
            sig_w = round((sw / sh) * sig_h)
            story.append(Image(sig, width=sig_w, height=sig_h))
        except Exception:
            pass

    if data.f2DateOfIssue:
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"Date of Issue: {data.f2DateOfIssue}", issued_norm))

    doc.build(story, onFirstPage=_draw_page, onLaterPages=_draw_page)
    buf.seek(0)
    return buf.read()
