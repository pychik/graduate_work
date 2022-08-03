from os import getenv
from pydantic import BaseSettings


class UgcSet(BaseSettings):
    KAFKA_TOPIC: str = getenv('KAFKA_TOPIC', 'events')
    KAFKA_HOST: str = getenv('KAFKA_HOST', '127.0.0.1')
    KAFKA_PORT: int = getenv('KAFKA_PORT', 9092)
    GROUP_ID: str = "echo-messages"
    CONSUMER_TIMEOUT_MS: int = 100
    MAX_RECORDS_PER_CONSUMER: int = 100

    MONGO_HOST: str = getenv('MONGO_HOST', '127.0.0.1')
    MONGO_PORT: int = getenv('MONGO_PORT', 27017)

    class UgcErrors:
        likes_not_found: str = "Rate not found"
        reviews_not_found: str = "Reviews not found"

    class Config:
        case_sensitive = False


settings = UgcSet()
