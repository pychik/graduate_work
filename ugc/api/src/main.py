import logging

from api.v1 import kafka_producer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


logger = logging.getLogger(__name__)

app = FastAPI(title="UGC",
              description='Асинхронный сборщик UGC',
              docs_url='/api/openapi',
              openapi_url='/api/openapi.json',
              root_path='/ugc',
              default_response_class=ORJSONResponse, )

app.include_router(kafka_producer.router, prefix='/api/v1/kafka')
