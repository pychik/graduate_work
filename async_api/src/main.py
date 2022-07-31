import http
import logging
import os

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import cache, search_service
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from helpers import check_authorization


app = FastAPI(
    title=config.PROJECT_NAME,
    description='Асинхронный API для кинотеатра',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    root_path='/service',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    cache.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    search_service.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    cache.redis.close()
    await cache.redis.wait_closed()
    await search_service.es.close()


if os.getenv('CURRENT_MODE') == 'production':
    @app.middleware('http')
    async def check_user_authorization(request: Request, call_next):
        url = 'http://auth_app:8000/api/v1/users/check_token/'
        response = await check_authorization(url, request.headers)
        if response.get('success'):
            return await call_next(request)

        return Response(status_code=http.HTTPStatus.UNAUTHORIZED)


# Подключаем роутер к серверу, указав префикс /v1/films
app.include_router(films.router, prefix='/api/v1/films')
app.include_router(genres.router, prefix='/api/v1/genres')
app.include_router(persons.router, prefix='/api/v1/persons')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True
    )
