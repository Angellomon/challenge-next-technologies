from data import get_headers_and_data_from_csv, transform_data_to_json
from schemas import validate_payments, extract_companies
from database import init_mongodb, close_mongodb
from models import PaymentDoc, InvalidPaymentDoc, CompanyDoc
import asyncio


async def setup_companies():
    headers, data = get_headers_and_data_from_csv()

    json_data = transform_data_to_json(headers, data)

    companies = extract_companies(json_data)

    await CompanyDoc.insert_many(
        [CompanyDoc(**company.model_dump()) for company in companies]
    )


async def setup_data():
    headers, data = get_headers_and_data_from_csv()

    json_data = transform_data_to_json(headers, data)


    payments, invalid_payments = validate_payments(json_data)

    await PaymentDoc.insert_many(
        [PaymentDoc(**payment.model_dump()) for payment in payments]
    )
    await InvalidPaymentDoc.insert_many(
        [
            InvalidPaymentDoc(**invalid_payment.model_dump())
            for invalid_payment in invalid_payments
        ]
    )


async def main():
    await init_mongodb()

    await setup_data()
    await setup_companies()

    close_mongodb()


if __name__ == "__main__":
    asyncio.run(main())
