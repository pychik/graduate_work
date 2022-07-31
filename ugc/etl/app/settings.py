from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # ClickHouse
    CH_HOST: str = Field('localhost', env='CH_HOST')
    CH_PORT: int = Field(9000, env='CH_PORT')
    # Kafka
    KAFKA_TOPIC = Field('events', env='KAFKA_TOPIC')
    KAFKA_HOST = Field('kafka', env='KAFKA_HOST')
    KAFKA_PORT = Field(9092, env='KAFKA_PORT')
    KAFKA_GROUP = Field('echo-messages', env='KAFKA_GROUP')

    class Config:
        env_file = '.env'


conf = Settings()
