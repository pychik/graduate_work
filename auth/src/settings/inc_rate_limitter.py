from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


rate_limiter = Limiter(key_func=get_remote_address,
                       strategy='moving-window',
                       default_limits=['20/second'])


def init_rate_limiter(app):
    rate_limiter.init_app(app)
