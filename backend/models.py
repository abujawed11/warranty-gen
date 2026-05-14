from pydantic import BaseModel


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
