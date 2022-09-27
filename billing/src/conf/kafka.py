import logging
import pickle
from typing import ByteString, Dict, Union

from conf.helper.decorators import backoff
from conf.settings import KAFKA_DEFAULT_PREFIX_TOPIC
from django.conf import settings
from kafka import KafkaProducer


logger = logging.getLogger()


class BillingKafkaProducer:
    def __init__(self, servers: list[str] = None) -> None:
        if not servers:
            servers = [settings.KAFKA_URL]
        self.servers = servers
        self.producer = self.get_producer()

    @backoff()
    def get_producer(self):
        # bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
        return KafkaProducer(bootstrap_servers=self.servers)

    def push(
        self,
        topic: str,
        value: Union[Dict[ByteString, ByteString], Dict[str, str]],
        key: Union[ByteString, str] = None, **kwargs
    ):
        if not self.producer:
            logger.warning('Kafka producer not set.')
            return

        if key:
            if isinstance(key, str):
                key = key.encode('utf-8')

        if isinstance(value, dict):
            value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)  # type: ignore
        topic = f'{KAFKA_DEFAULT_PREFIX_TOPIC}-{topic}'

        self.producer.send(topic, value=value, key=key, **kwargs)
