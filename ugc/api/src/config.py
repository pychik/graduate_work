from os import getenv
from pydantic import BaseSettings


class KafkaSet(BaseSettings):
    KAFKA_TOPIC: str = getenv('KAFKA_TOPIC', 'events')
    KAFKA_HOST: str = getenv('KAFKA_HOST', '127.0.0.1')
    KAFKA_PORT: int = getenv('KAFKA_PORT', 9092)
    GROUP_ID: str = "echo-messages"
    CONSUMER_TIMEOUT_MS: int = 100
    MAX_RECORDS_PER_CONSUMER: int = 100

    class Config:
        case_sensitive = False


settings = KafkaSet()
