import io

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from models import CertificateData
from pdf_builder import build_pdf
from pdf_builder_v2 import build_pdf_v2
from pdf_builder_test import build_pdf_test

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI Running"}


@app.post("/api/generate-certificate")
def generate_certificate_json(data: CertificateData):
    return _pdf_response(data)


@app.post("/api/download-certificate")
def generate_certificate_form(
    certificateFormat:    str = Form("format1"),
    # Format 1 fields
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
    # Format 2 fields
    f2ProjectName:        str = Form(""),
    f2Client:             str = Form(""),
    f2SolarConsultant:    str = Form(""),
    f2SolarDeveloper:     str = Form(""),
    f2MainContractor:     str = Form(""),
    f2Location:           str = Form(""),
    f2ProductDescription: str = Form(""),
    f2ProductWarranty:    str = Form(""),
    f2DesignWarranty:     str = Form(""),
    f2WarrantyPeriodNote: str = Form(""),
    f2DateOfIssue:        str = Form(""),
    # Format 3 fields
    tcRefNumber:          str = Form(""),
    tcDate:               str = Form(""),
    tcCustomerName:       str = Form(""),
    tcCustomerAddress:    str = Form(""),
    tcCustomerGstin:      str = Form(""),
    tcProjectName:        str = Form(""),
    tcSupplierName:       str = Form("SUNRACK TECHNOLOGIES LLP"),
    tcSupplierAddress:    str = Form("Flat no. 13 A/18 Krishna Gopal Krishna Nagar, Khairapada, Boisar, Dist. Palghar, Maharashtra-401501"),
    tcSupplierGstin:      str = Form("27AEEFS1875H1ZR"),
    tcPoNumber:           str = Form(""),
    tcPoDate:             str = Form(""),
    tcDispatchDate:       str = Form(""),
    tcMaterialPartName:   str = Form(""),
    tcQuantityKWp:        str = Form(""),
    tcRemarks:            str = Form(""),
    tcSi:                 str = Form(""),
    tcMg:                 str = Form(""),
    tcFe:                 str = Form(""),
    tcOther:              str = Form(""),
    tcAl:                 str = Form(""),
    tcBHN:                str = Form(""),
    tcHV10:               str = Form(""),
):
    data = CertificateData(
        certificateFormat=certificateFormat,
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
        f2ProjectName=f2ProjectName,
        f2Client=f2Client,
        f2SolarConsultant=f2SolarConsultant,
        f2SolarDeveloper=f2SolarDeveloper,
        f2MainContractor=f2MainContractor,
        f2Location=f2Location,
        f2ProductDescription=f2ProductDescription,
        f2ProductWarranty=f2ProductWarranty,
        f2DesignWarranty=f2DesignWarranty,
        f2WarrantyPeriodNote=f2WarrantyPeriodNote,
        f2DateOfIssue=f2DateOfIssue,
        tcRefNumber=tcRefNumber,
        tcDate=tcDate,
        tcCustomerName=tcCustomerName,
        tcCustomerAddress=tcCustomerAddress,
        tcCustomerGstin=tcCustomerGstin,
        tcProjectName=tcProjectName,
        tcSupplierName=tcSupplierName,
        tcSupplierAddress=tcSupplierAddress,
        tcSupplierGstin=tcSupplierGstin,
        tcPoNumber=tcPoNumber,
        tcPoDate=tcPoDate,
        tcDispatchDate=tcDispatchDate,
        tcMaterialPartName=tcMaterialPartName,
        tcQuantityKWp=tcQuantityKWp,
        tcRemarks=tcRemarks,
        tcSi=tcSi,
        tcMg=tcMg,
        tcFe=tcFe,
        tcOther=tcOther,
        tcAl=tcAl,
        tcBHN=tcBHN,
        tcHV10=tcHV10,
    )
    return _pdf_response(data)


def _first_word(name: str) -> str:
    return name.strip().split()[0] if name.strip() else ""


def _pdf_response(data: CertificateData):
    if data.certificateFormat == "format2":
        pdf_bytes = build_pdf_v2(data)
        client  = _first_word(data.f2Client) or "Unknown"
        project = "".join(ch for ch in data.f2ProjectName if ch.isalnum() or ch in "_-").strip() or "NoProject"
        filename = f"Warranty_Certificate_{client}_{project}.pdf"
    elif data.certificateFormat == "format3":
        pdf_bytes = build_pdf_test(data)
        customer = _first_word(data.tcCustomerName) or "Unknown"
        po       = "".join(ch for ch in data.tcPoNumber if ch.isalnum() or ch in "_-").strip() or "NoPO"
        filename = f"Test_Certificate_{customer}_{po}.pdf"
    else:
        pdf_bytes = build_pdf(data)
        billing  = _first_word(data.billingCustomerName)  or "Unknown"
        shipping = _first_word(data.shippingCustomerName) or "Unknown"
        po       = "".join(ch for ch in data.invoicePONumber if ch.isalnum() or ch in "_-").strip() or "NoPO"
        filename = f"Warranty_Certificate_{billing}_{shipping}_{po}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
