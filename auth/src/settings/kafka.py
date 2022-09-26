import pickle
import logging
from typing import Dict, Optional

from helpers.decorators import backoff
from kafka import KafkaConsumer
from settings.config import Configuration
from flask import Flask
import click
from settings.datastore import user_datastore
from settings.datastore import security



logger = logging.getLogger()


class AuthKafkaConsumer:
    """Kafka Consumer.
    Читает billing-auth топик, добавляет либо убирает роль пользователя.
    В случаи отсутствия роли, роль будет создана.
    """
    def __init__(self, servers: list[str] = [Configuration.KAFKA_URL]) -> None:
        self.servers = servers
        self.consumer = None

    @backoff()
    def _get_consumer(self, topic: Optional[str] = None) -> Optional[KafkaConsumer]:
        # bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
        if not topic:
            logger.warning('Topic not specified, reading is not possible')
            return

        return KafkaConsumer(
            topic,
            bootstrap_servers=self.servers,
            auto_offset_reset='earliest',
            group_id='auth_billing_group',
            api_version=(0, 10)
        )

    def billing(self, topic: Optional[str] = None):
        if not topic:
            topic: str = Configuration.KAFKA_DEFAULT_BILLING_TOPIC
        self.consumer = self._get_consumer(topic=topic)

        for message in self.consumer:
            data = pickle.loads(message.value)
            user = user_datastore.find_user(pk=data.get('user_id', None))

            if not user:
                user_id = data.get('user_id', None)
                logger.warning(f'user id - {user_id} not found')
                return

            user_roles = set(role.name for role in user.roles)
            if role_name := data.get('subscription_name', None):
                role = user_datastore.find_or_create_role(
                        name=role_name,
                        description=data.get('subscription_description', None)
                    )

                if role and data.get('enable', None):
                    if role_name not in user_roles:
                        user.add_role(role, security)
                else:
                    if role_name in user_roles:
                        user.delete_role(role, security)

def init_kafka_commands(app:Flask):

    @app.cli.command()
    @click.argument('method')
    def init_kafka_consumer(method: str) -> None:
        customer = AuthKafkaConsumer()
        cls_method = getattr(customer, 'billing', None)
        if not cls_method:
            logger.error(f'Method - {method} not allowed.')
            return
        cls_method()
