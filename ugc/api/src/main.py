import logging
import os

from api.v1 import bookmarks, kafka_producer, rating
from config import settings
from db import mongo
from db.helpers import create_indexes
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from motor.motor_asyncio import AsyncIOMotorClient

UGC_SENTRY_DSN = os.environ.get('UGC_SENTRY_DSN', '')

logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=UGC_SENTRY_DSN,
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    traces_sample_rate=1.0
)

app = FastAPI(title="UGC Service",
              description='Асинхронный сборщик UGC',
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              default_response_class=ORJSONResponse,)


@app.on_event("startup")
async def startup():
    mongo.mongo = AsyncIOMotorClient(f"mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}")
    await create_indexes()


app.include_router(kafka_producer.router, prefix='/api/kafka')
app.include_router(rating.router, prefix='/api/v1/rating')
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks')
