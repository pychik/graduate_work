import redis
from helpers.utility import backoff
from settings.config import Configuration


@backoff()
def redis_connect(redis_uri: str = Configuration.REDIS_URI):
    return redis.from_url(redis_uri)
