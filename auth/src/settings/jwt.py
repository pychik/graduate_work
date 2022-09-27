from flask import Flask
from flask_jwt_extended import JWTManager
from settings.redis import redis_connect


jwt = JWTManager()
jwt_redis_blocklist = redis_connect()


def init_jwt(app: Flask):
    jwt.init_app(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
