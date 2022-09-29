
import logging

from celery_once import QueueOnce
from conf.celery import TaskQueue, app
from conf.kafka import BillingKafkaProducer

from apps.transactions.helpers import (
    cancellation_subscription_expiration,
    subscription_expiration_alert,
)
from conf.celery import TaskQueue, app


@app.task(base=QueueOnce, queue=TaskQueue.QUEUE_DEFAULT)
def task_send_kafka(topic: str, data: dict):
    kafka = BillingKafkaProducer()
    kafka.push(topic=topic, value=data)
    logging.info(f'Sent to kafka topic {topic}')



@app.task(ignore_result=True, queue=TaskQueue.QUEUE_DEFAULT)
def task_subscription_expiration():
    """
    Таска отменяет подписки, по которым окончился актуальный срок.
    """
    cancellation_subscription_expiration()


@app.task(ignore_result=True, queue=TaskQueue.QUEUE_DEFAULT)
def task_subscription_expiration_alert(days: int = 2):
    """
    Таска оповещает пользователей, о скором окончании их подписки.
    По умолчанию, все активные подписки, по которым срок действия истекает через 2 дня.
    """
    subscription_expiration_alert(days=days)
