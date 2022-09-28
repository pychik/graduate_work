import logging

from celery_once import QueueOnce
from conf.celery import TaskQueue, app
from conf.kafka import BillingKafkaProducer


@app.task(base=QueueOnce, queue=TaskQueue.QUEUE_DEFAULT)
def task_send_kafka(topic: str, data: dict):
    kafka = BillingKafkaProducer()
    kafka.push(topic=topic, value=data)
    logging.info(f'Sent to kafka topic {topic}')
