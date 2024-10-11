from datetime import datetime

from beanie import Document
from pydantic import Field


from schemas import PaymentStatus


class PaymentDoc(Document):
    id: str = Field()
    name: str
    company_id: str
    amount: float
    status: PaymentStatus
    created_at: datetime
    paid_at: datetime | None = None

    class Settings:
        name = "Charges"


class InvalidPaymentDoc(Document):
    id: str | None = Field(None)
    name: str | None = None
    company_id: str | None = None
    amount: float | None = None
    status: str | None = None
    created_at: datetime | None = None
    paid_at: datetime | None = None

    class Settings:
        name = "InvalidCharges"


class CompanyDoc(Document):
    id: str
    name: str

    class Settings:
        name = "Companies"
