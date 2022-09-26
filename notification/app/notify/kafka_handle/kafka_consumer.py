import logging
import pickle
from typing import Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from django.conf import settings

from config.helper.decorators import backoff
from notify.models import NotificationLog


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationKafka:
    def __init__(self, servers: list[str] = None) -> None:

        self.servers = servers if servers else [settings.KAFKA_URL]
        self.consumer = None
        self._stop_consumer = False

    @staticmethod
    def _info_loader(data_packet: dict) -> None:
        if isinstance(data_packet, dict) \
            and (data_packet.get('notification_data').get('firstname')
                 is not None and data_packet.get('notification_data').get('email')
                 is not None and data_packet.get('notification_type') is not None):
            _notification_type = data_packet.get("notification_type")
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # NotificationTypes
            # billing_payment_status = ('billing_payment_status', 'billing_payment_status')
            # billing_auto_payment = ('billing_auto_payment', 'billing_auto_payment')
            # billing_subscription_expires = ('billing_subscription_expires', 'billing_subscription_expires')
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            _notification_data = data_packet.get("notification_data")
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # dict(notification_data=datadict)
            # datadict
            #   firstname
            #   email
            #   payment_status or subscription_type
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

            NotificationLog(notification_data=_notification_data, notification_type=_notification_type).save()
        else:
            logger.exception("NotificationKafka  sending log to Kafka: \'_info_loader\' received not valid data")

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
                    # ?? для перезапуска контейнера
                    self.stop_consumer()
                except Exception as e:
                    logger.exception("NotificationKafka exception sending log to Kafka: %s", e)
                    continue
