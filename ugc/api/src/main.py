import logging
import os

from api.v1 import kafka_producer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

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

app = FastAPI(title="UGC",
              description='Асинхронный сборщик UGC',
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              root_path='/ugc',
              default_response_class=ORJSONResponse, )

app.include_router(kafka_producer.router, prefix='/api/v1/kafka')
