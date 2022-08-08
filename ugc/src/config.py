# type:ignore[assignment]

from pydantic import BaseSettings, Field


class UgcSet(BaseSettings):
    KAFKA_TOPIC: str = ...
    KAFKA_HOST: str = ...
    KAFKA_PORT: int = ...
    GROUP_ID: str = "echo-messages"
    CONSUMER_TIMEOUT_MS: int = 100
    MAX_RECORDS_PER_CONSUMER: int = 100

    MONGO_HOST: str = Field('127.0.0.1', env='MONGO_HOST')
    MONGO_PORT: int = Field(27017, env='MONGO_PORT')

    class UgcErrors:
        likes_not_found: str = "Rate not found"
        reviews_not_found: str = "Reviews not found"
        rates_range: range = range(0, 11)
        bad_rates: str = f"BAd rates input. Use rate in range {rates_range[0]}..{rates_range[-1]}"

    class Config:
        case_sensitive = False


settings = UgcSet()
