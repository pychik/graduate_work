import redis
from tests.functional.settings import settings
from utils import backoff


@backoff()
def check():
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    r.ping()


if __name__ == '__main__':
    check()
