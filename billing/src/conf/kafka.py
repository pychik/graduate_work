import logging
import pickle
from typing import Any, ByteString, Dict

from conf.helper.decorators import backoff
from conf.settings import KAFKA_DEFAULT_PREFIX_TOPIC
from django.conf import settings
from kafka import KafkaProducer


logger = logging.getLogger()


class BillingKafkaProducer:
    def __init__(self, servers: list = [settings.KAFKA_URL]) -> None:
        self.servers = servers
        self.producer = self.get_producer()

    @backoff()
    def get_producer(self):
        # bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
        return KafkaProducer(bootstrap_servers=self.servers)

    def push(self, topic: str, value: Any[Dict[str, str], ByteString], key: Any[ByteString, str] = None, **kwargs):
        if not self.producer:
            logger.warning('Kafka producer not set.')
            return

        if key:
            if isinstance(key, str):
                key = key.encode('utf-8')

        if isinstance(value, dict):
            topic = f'{KAFKA_DEFAULT_PREFIX_TOPIC}-{topic}'

        value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)

        self.producer.send(topic, value=value, key=key, **kwargs)
