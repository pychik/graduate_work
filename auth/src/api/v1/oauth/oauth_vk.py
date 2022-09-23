import urllib.parse
from datetime import datetime, timedelta
from http.client import NOT_FOUND, OK

from core.api.client import ApiRestClient
from core.api.router import APIRouter
from core.consts import VK_SERVICE
from flask import redirect, request, url_for
from flask_restx import Namespace, Resource, abort, fields, reqparse
from helpers.utility import create_new_user, create_or_update_user_service, generate_password
from models import OauthServices, User, UserSessions


api = Namespace('oauth/vk', description='VK OAuth')

authorize_parser = reqparse.RequestParser(bundle_errors=True)
authorize_parser.add_argument(
    'code',
    required=True,
    type=str,
    help='code',
    location='args'
)
authorize_schema = api.model('Tokens', {
    'access_token': fields.String(readonly=True, description='Access token'),
    'refresh_token': fields.String(required=True, description='Refresh token'),
    'temporary_password': fields.String(required=False,
                                        description='Temporary password')
})


@api.route('/authorize/', endpoint='vk-authorize')
class Authorize(Resource):
    @api.doc(description='Oauth authorize')
    @api.expect(authorize_parser)
    @api.marshal_with(authorize_schema, code=OK)
    def get(self):
        temporary_password = None
        code = authorize_parser.parse_args().get('code')

        router = APIRouter(service=VK_SERVICE)
        client = ApiRestClient(router)

        user_data = client.get_vk_user_credentials(code=code)
        if user_data.get('error'):
            return user_data

        email = user_data.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            temporary_password = generate_password()
            data = dict(
                email=email,
                password=temporary_password,
                active=True
            )
            user = create_new_user(data)

        user_oauth_service = dict(
            user_id=user.pk,
            service=VK_SERVICE,
            access_token=user_data.get('access_token'),
            token_type=user_data.get('token_type'),
            access_token_expires=datetime.utcnow() + timedelta(
                seconds=user_data.get('expires_in')),
        )
        # Создаем, либо обновляем OAuth сервис пользователя
        create_or_update_user_service(user_oauth_service)

        # Создаем новую сессию
        new_session = UserSessions(
            user_id=user.pk,
            user_agent=request.headers.get('User-Agent'),
            last_login=datetime.utcnow()
        )
        new_session.save()

        tokens = user.get_jwt_token()
        if temporary_password:
            tokens.update(temporary_password=temporary_password)
        return tokens, OK


@api.route('/redirect/')
class RedirectLink(Resource):

    @api.doc(description='VK oauth redirect link')
    def get(self):
        settings = OauthServices.get_service(service=VK_SERVICE)
        if not settings:
            abort(NOT_FOUND, errors=['Настройки сервиса не найдены!'])

        redirect_uri = url_for('api.vk-authorize').lstrip('/')
        redirect_uri = f'{request.host_url}{redirect_uri}'

        params = dict(client_id=settings.client_id,
                      client_secret=settings.client_secret,
                      display='page',
                      scope='email',
                      redirect_uri=redirect_uri,
                      response_type='code')

        url = f'{settings.host}/authorize?'
        return redirect(url + urllib.parse.urlencode(params))
