import os


DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_DATABASE = os.environ.get('POSTGRES_DB', 'movies_auth')
DB_USER = os.environ.get('POSTGRES_USER', 'movies_auth')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'movies_auth')
DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

CURRENT_MODE = os.environ.get('CURRENT_MODE', 'dev')
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Auth')


class Configuration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'very_secret')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'very_salt')
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = 'headers'
    ACCESS_TOKEN_EXPIRE_TIME = 60 * 60

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'

    APP_HOST = os.environ.get('API_HOST', 'localhost')
    APP_PORT = os.environ.get('API_PORT', 82)
    APP_WORKERS = os.environ.get('APP_WORKERS', 2)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    RESTX_ERROR_404_HELP = False

    PAGINATION_PER_PAGE = os.environ.get('PAGINATION_PER_PAGE', 10)

    JAEGER_HOST = os.environ.get('JAEGER_HOST', 'jaeger')
    JAEGER_PORT = int(os.environ.get('JAEGER_PORT', 6831))


class ProductionConfig(Configuration):
    FLASK_ENV = 'production'


class DevelopmentConfig(Configuration):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Configuration):
    TESTING = True
    FLASK_ENV = 'development'

    APP_HOST = os.environ.get('API_HOST', 'localhost')
    APP_PORT = os.environ.get('API_PORT', 82)
    SERVER_NAME = f'{APP_HOST}:{APP_PORT}'


MODES = {
    'prod': ProductionConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig,
}
configuration: MODES = MODES[CURRENT_MODE]()
