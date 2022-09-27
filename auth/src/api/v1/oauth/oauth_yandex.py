from datetime import datetime, timedelta
from http.client import NOT_FOUND, OK
from urllib.parse import urlencode

from core.api.client import ApiRestClient
from core.api.router import APIRouter
from core.consts import YANDEX_SERVICE
from flask import redirect, request
from flask_restx import Namespace, Resource, abort, fields
from helpers.parsers import callback_code_parser
from helpers.utility import (
    create_new_user,
    create_or_update_user_service,
    generate_password,
    get_user_device_type,
)
from models import OauthServices, User, UserSessions


api = Namespace('oauth/yandex', description='Yandex OAuth')

oauth_schema = api.model('Tokens', {
    'access_token': fields.String(readonly=True, description='Access token'),
    'refresh_token': fields.String(readonly=True, description='Refresh token'),
    'temporary_password': fields.String(
        readonly=True, description='Temporary password')
})


@api.route('/redirect/')
class YandexOauth(Resource):
    @api.doc(description='Yandex oauth redirect link')
    def get(self):
        yandex_settings = OauthServices.get_service(service=YANDEX_SERVICE)

        if not yandex_settings:
            abort(NOT_FOUND, errors=['Настройки сервиса не найдены!'])

        url = f'{yandex_settings.host}/authorize?'
        params = dict(
            response_type='code',
            client_id=yandex_settings.client_id
        )

        url = url + urlencode(params)
        return redirect(url)


@api.route('/code/')
class Code(Resource):
    @api.doc(description='Authorization with Yandex service.')
    @api.expect(callback_code_parser)
    @api.marshal_with(oauth_schema, code=OK)
    def get(self):
        temporary_password = None
        args = callback_code_parser.parse_args()
        router = APIRouter(service=YANDEX_SERVICE)
        client = ApiRestClient(router)

        user_credentials = client.get_yandex_user_credentials(secret_code=str(args.get('code')))
        user_info = client.get_yandex_user_info(access_token=user_credentials.get('access_token'))
        user = User.query.filter_by(email=user_info.get('default_email')).first()

        # Создаем пользователя, если ранее не был зарегистрирован.
        if not user:
            temporary_password = generate_password()
            data = dict(
                email=user_info.get('default_email'),
                password=temporary_password,
                first_name=user_info.get('first_name', None),
                last_name=user_info.get('last_name', None),
                active=True
            )
            user = create_new_user(data)

        user_oauth_service = dict(
            user_id=user.pk,
            service=YANDEX_SERVICE,
            access_token=user_credentials.get('access_token'),
            refresh_token=user_credentials.get('refresh_token'),
            token_type=user_credentials.get('token_type'),
            access_token_expires=datetime.utcnow() + timedelta(
                seconds=user_credentials.get('expires_in')),
            refresh_token_expires=datetime.utcnow() + timedelta(
                seconds=user_credentials.get('expires_in'))
        )
        # Создаем, либо обновляем OAuth сервис пользователя
        create_or_update_user_service(user_oauth_service)
        # Создаем новую сессию
        new_session = UserSessions(
            user_id=user.pk,
            user_agent=request.headers.get('User-Agent'),
            last_login=datetime.utcnow(),
            user_device_type=get_user_device_type(request.headers.get('User-Agent'))
        )
        new_session.save()
        response = user.get_jwt_token()
        if temporary_password:
            response.update(temporary_password=temporary_password)
        return response
