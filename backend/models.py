from pydantic import BaseModel


class CertificateData(BaseModel):
    certificateFormat: str = "format1"

    # ── Format 1 fields ───────────────────────────────────
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

    # ── Format 2 fields ───────────────────────────────────
    f2ProjectName: str = ""
    f2Client: str = ""
    f2SolarConsultant: str = ""
    f2SolarDeveloper: str = ""
    f2MainContractor: str = ""
    f2Location: str = ""
    f2ProductDescription: str = ""
    f2ProductWarranty: str = ""
    f2DesignWarranty: str = ""
    f2WarrantyPeriodNote: str = ""
    f2DateOfIssue: str = ""
