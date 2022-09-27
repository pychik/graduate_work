import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('SECRET_KEY')
YOOKASSA_ID = os.environ.get('YOOKASSA_ID')
YOOKASSA_API_SECRET = os.environ.get('YOOKASSA_API_SECRET')
REDIRECT_URL = "http://127.0.0.1:7777"

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'drf_yasg',

    'apps.offer.apps.OfferConfig',
    'apps.restapi.apps.RestapiConfig',
    'apps.transactions.apps.TransactionsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
include(
    'components/database.py',
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}

# Internationalization
INTERNAL_IPS = [
    '127.0.0.1',
]

# CELERY SETTINGS
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'localhost')
# Данная команда нужна будет, кода у нас разные воркеры
# CELERY_TASK_ALWAYS_EAGER = False if CELERY_BROKER_URL else True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# RESULT_BACKEND
CELERY_RESULT_BACKEND = 'django-db'

CELERY_ONCE = {
    'backend': 'celery_once.backends.File',
    'settings': {
        'location': '/tmp/celery_once',  # noqa
        'default_timeout': 60 * 60
    }
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Kafka
KAFKA_URL = os.environ.get('KAFKA_URL', '')
KAFKA_DEFAULT_SERIALIZER = os.environ.get('KAFKA_DEFAULT_SERIALIZER', 'json')
KAFKA_DEFAULT_PREFIX_TOPIC = os.environ.get('KAFKA_DEFAULT_PREFIX_TOPIC', 'billing')

# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHELL_PLUS = "ipython"


REFUND_GRACE_PERIOD = {'days': 3}
