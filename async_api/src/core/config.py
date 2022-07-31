import os
from logging import config as logging_config

import environ
from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

# Настройки Env
env = environ.Env()
environ.Env.read_env()

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = env.str('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = env.str('REDIS_HOST', 'redis')
REDIS_PORT = env.int('REDIS_PORT', 6379)

# Настройки Elasticsearch
ELASTIC_HOST = env.str('ETL_HOST', 'elastic')
ELASTIC_PORT = env.int('ETL_PORT', 9200)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CACHE_TIMEOUT = 60 * 5
