from models import PaymentDoc, InvalidPaymentDoc, CompanyDoc

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from settings import get_settings

DEFAULT_MONGODB_URI = "mongodb://user:password@localhost:27017"

_client: AsyncIOMotorClient | None = None


async def init_mongodb() -> AsyncIOMotorClient:
    settings = get_settings()

    mongodb_uri = settings.mongodb_uri

    client = AsyncIOMotorClient(str(mongodb_uri))

    _client = client

    await init_beanie(
        database=client.next_technologies_challenge,
        document_models=[PaymentDoc, InvalidPaymentDoc, CompanyDoc],
    )

    return client


def close_mongodb():
    if not _client:
        return

    _client.close()
