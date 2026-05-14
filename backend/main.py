import io

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from models import CertificateData
from pdf_builder import build_pdf

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
