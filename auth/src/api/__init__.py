from api.v1.auth import api as auth_ns1
from api.v1.oauth.oauth_vk import api as oauth_vk_ns1
from api.v1.oauth.oauth_yandex import api as oauth_ya_ns1
from api.v1.roles import api as role_ns1
from api.v1.roles_manager import api as role_ns2
from api.v1.users import api as users_ns1
from flask import Blueprint
from flask_restx import Api


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
authorizations = {'Bearer': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
api = Api(blueprint,
          title='Auth flask',
          version='1.0',
          description='Simple auth on Flask',
          security='Bearer',
          authorizations=authorizations)

api.add_namespace(auth_ns1)
api.add_namespace(users_ns1)
api.add_namespace(role_ns1)
api.add_namespace(role_ns2)
api.add_namespace(oauth_ya_ns1)
api.add_namespace(oauth_vk_ns1)


def init_api(app):
    app.register_blueprint(blueprint)
