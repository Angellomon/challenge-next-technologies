from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: AnyUrl = AnyUrl("mongodb://user:password@localhost:27017")


def get_settings() -> Settings:
    return Settings()
