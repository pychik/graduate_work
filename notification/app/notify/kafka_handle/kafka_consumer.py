import logging
import pickle
from typing import Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from django.conf import settings

from config.helper.decorators import backoff
from notify.models import NotificationLog
from notify.utility.api_client import ApiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationKafka:
    def __init__(self, servers: list[str] = None) -> None:

        self.servers = servers if servers else [settings.KAFKA_URL]
        self.consumer = None
        self._stop_consumer = False

    def _info_loader(self, data_packet: dict) -> None:
        if not isinstance(data_packet, dict):
            logger.exception("NotificationKafka  sending log to Kafka:"
                             " \'_info_loader\' received not valid data data_packet")
            return None
        _notification_type = data_packet.get("notification_type")
        if not isinstance(_notification_type, str) and not _notification_type:
            logger.exception("NotificationKafka  sending log to Kafka:"
                             " \'_info_loader\' received not valid data \'_notification_type\'")
            return None
        _user_id = data_packet.get('user_id')
        if not isinstance(_user_id, int) and not _user_id:
            logger.exception("NotificationKafka  sending log to Kafka:"
                             " \'_info_loader\' received not valid data \'_user_id\'")
            return None
        _message = data_packet.get('message')
        if not isinstance(_message, str) and not _user_id:
            logger.exception("NotificationKafka  sending log to Kafka:"
                             " \'_info_loader\' received not valid data \'_user_id\'")
            return None

        _data_raw = self._get_user_data(user_id=_user_id)
        _email = _data_raw.get('profile').get('email')  # type: ignore
        _first_name = _data_raw.get('profile').get('first_name')  # type: ignore

        _notification_data = dict(email=_email,
                                  first_name=_first_name,
                                  message=_message)

        NotificationLog(notification_data=_notification_data, notification_type=_notification_type).save()

    @staticmethod
    def _get_user_data(user_id: int) -> dict:
        _api = ApiClient()
        _api_response = _api.request_auth(user_id=user_id)
        return _api_response

    def stop_consumer(self,) -> None:
        self._stop_consumer = True

    @backoff()
    def _get_consumer(self, topic: Optional[str] = None) -> Optional[KafkaConsumer]:
        if not topic:
            logger.warning('Topic not specified, reading is not possible')
            return None

        return KafkaConsumer(
            topic,
            bootstrap_servers=self.servers,
            auto_offset_reset='earliest',
            group_id=settings.KAFKA_GROUP_ID,
            api_version=(0, 10),
        )

    def main(self, topic: Optional[str] = None):

        if not topic:
            topic = settings.NOTIFICATION_KAFKA_TOPIK

        self.consumer = self._get_consumer(topic=topic)
        while not self._stop_consumer:
            for msg in self.consumer:
                if self._stop_consumer:
                    break
                try:
                    deserialized_data = pickle.loads(msg.value)
                    self._info_loader(deserialized_data)
                except KafkaError as ke:
                    logger.exception("NotificationKafka kafka error sending log to Kafka: %s", ke)
                    # для перезапуска контейнера
                    self.stop_consumer()
                except Exception as e:
                    logger.exception("NotificationKafka exception sending log to Kafka: %s", e)
                    continue
