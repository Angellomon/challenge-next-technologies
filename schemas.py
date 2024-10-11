from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    voided = "voided"
    pending = "pending_payment"
    paid = "paid"
    pre_authorized = "pre_authorized"
    refunded = "refunded"
    charged_back = "charged_back"
    expired = "expired"
    partially_refunded = "partially_refunded"


class PaymentCreate(BaseModel):
    id: str = Field(min_length=1)
    name: str
    company_id: str
    amount: float
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime | None = None


class InvalidPaymentCreate(BaseModel):
    id: str | None = Field(None)
    name: str | None = None
    company_id: str | None = None
    amount: float | None = None
    status: str | None = None
    created_at: datetime | None = None
    paid_at: datetime | None = None


class CompanyCreate(BaseModel):
    id: str
    name: str


# TODO: impl proper error management
def process_errors(errors, data):
    return InvalidPaymentCreate(**data)


def validate_payments(
    data: list[any],
) -> tuple[list[PaymentCreate], list[InvalidPaymentCreate]]:
    payments = []
    invalid_payments = []

    for element in data:
        try:
            payments.append(PaymentCreate(**element))
        except ValueError as err:
            errors = err.errors()
            print(f"invalid data found in {element}")
            print(f"errors: {errors}")

            invalid_payment = process_errors(errors, element)
            invalid_payments.append(invalid_payment)

            print("element not added to database, pending proper fix")

    return payments, invalid_payments


def extract_companies(
    data: list[any], invalid_id_values=[None, "*******"]
) -> list[CompanyCreate]:
    companies_dict = {}

    for element in data:
        _id = element["company_id"]
        if _id not in companies_dict and _id not in invalid_id_values:
            companies_dict[_id] = element["name"]

    return [
        CompanyCreate(
            **{"id": elem[0], "name": elem[1]},
        )
        for elem in companies_dict.items()
    ]
