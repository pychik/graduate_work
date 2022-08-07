import logging

from api.v1 import kafka_producer
from api.v1 import rating
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from db import mongo


logger = logging.getLogger(__name__)

app = FastAPI(title="UGC Service",
              description='Асинхронный сборщик UGC',
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              root_path='/ugc',
              default_response_class=ORJSONResponse,)


@app.on_event("startup")
async def startup():
    mongo.mongo = AsyncIOMotorClient(f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}")


app.include_router(kafka_producer.router, prefix='/api/kafka')
app.include_router(rating.router, prefix='/api/v1/rating')
