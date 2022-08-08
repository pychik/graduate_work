import json
from datetime import datetime
from typing import List

from fastapi import APIRouter
from models.models import Event, UserValues
from service.kafka_setter import process_get_messages, process_load_kafka


router = APIRouter()


@router.post("/ugc-producer",
             summary='Прием аналитических данных',
             description='Сбор данных от пользователя',
             tags=['UGC'],
             status_code=204)
async def kafka_load(event: Event):
    """
    Produce a test ugc messages into kafka.
    """
    data = event.dict()
    data['date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_info = json.dumps(data).encode()
    return await process_load_kafka(value=my_info)


@router.get("/ugc-consumer",
            response_model=List[UserValues],
            summary='Получение данных из хранилища',
            description='Проверка работы хранилища Kafka',
            tags=['UGC'],
            status_code=200)
async def get_messages_from_kafka():
    """
    Consume a list of messages from kafka.
    """

    return await process_get_messages()
