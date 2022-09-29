from datetime import timedelta
from itertools import islice

from apps.transactions.models import UserSubscription, UserSubscriptionStatuses
from conf.kafka import BillingKafkaProducer
from conf.settings import CHUNK_SIZE_DEFAULT
from django.utils import timezone


def chunks(iterable, n):
    """
    Хелпер, позволяет делить на N частей итерируемый объект.
    """
    it = iter(iterable)

    if isinstance(iterable, dict):
        for i in range(0, len(iterable), n):
            yield {k: iterable[k] for k in islice(it, n)}
    else:
        # Для всех остальных: list, tuple, Queryset и etc
        chunk = list(islice(it, n))
        while chunk:
            yield chunk
            chunk = list(islice(it, n))


def cancellation_subscription_expiration() -> None:
    """
    Находим все активные подписки, по которым окончился актуальный срок действия.
    Отправляется запрос в Kafka, где доступ будет убран.
    Далее деактивируем действующую подписку.
    Формат сообщения, который будет отправлен в топик Кафки:
    {
        "user_id": int,
        "subscription_name": str,
        "subscription_description": str,
        "enable": boolean
    }
    """
    kafka_client = BillingKafkaProducer()

    accounts = UserSubscription.objects.filter(
        status=UserSubscriptionStatuses.active,
        expires_at__lte=timezone.now()
    ).select_related('subscription')

    for chunk in chunks(accounts, CHUNK_SIZE_DEFAULT):
        for account in chunk:
            value = dict(
                user_id=account.user_id,
                subscription_name=account.subscription.name,
                subscription_description=account.subscription.description,
                enable=False
            )
            kafka_client.push('auth', value=value)
            account.status = UserSubscriptionStatuses.expired
            account.save()


def subscription_expiration_alert(days: int = 2):
    """
    Оповещает пользователей о скором завершения действия активной подписки.
    По умолчанию, все активные подписки, по которым срок действия истекает через 2 дня.
    """
    kafka_client = BillingKafkaProducer()

    accounts = UserSubscription.objects.filter(
        status=UserSubscriptionStatuses.active,
        expires_at__gte=timezone.now() - timedelta(days=days),
        notification_status=False
    ).select_related('subscription')

    for chunk in chunks(accounts, CHUNK_SIZE_DEFAULT):
        for account in chunk:
            value = dict(
                user_id=account.user_id,
                notification_type='billing_subscription_expires'
            )
            kafka_client.push('notification', value=value)
            account.notification_status = True
            account.save()
