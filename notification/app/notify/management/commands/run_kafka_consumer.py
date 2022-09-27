from django.core.management.base import BaseCommand
from notify.kafka_handle.kafka_consumer import NotificationKafka


class Command(BaseCommand):
    help = 'Runs notification kafka consumer infinite process in separate from notification thread'

    def handle(self, *args, **options):
        _notification_consumer = NotificationKafka()
        _notification_consumer.main()
