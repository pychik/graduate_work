from datetime import datetime, timedelta
from http.client import CREATED, NOT_FOUND, OK

from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, abort, fields
from flask_security.utils import verify_password
from helpers.parsers import login_parser, signup_parser
from helpers.utility import create_new_user, get_user_device_type
from models import User, UserSessions
from settings.config import Configuration
from settings.jwt import jwt_redis_blocklist


api = Namespace('auth', description='Authorization')
signup_schema = api.model('Signup', {
    'pk': fields.String(readonly=True, description='Unique identifier'),
    'email': fields.String(required=True, description='Email'),
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'birth_date': fields.Date(required=False),
    'phone': fields.String(required=False),
})
login_schema = api.model('Tokens', {
    'access_token': fields.String(readonly=True, description='Access token'),
    'refresh_token': fields.String(required=True, description='Refresh token'),
})
refresh_schema = api.model('AccessToken', {
    'access_token': fields.String(readonly=True, description='Access token'),
})
refresh_schema_expected = api.model('RefreshToken', {
    'refresh_token': fields.String(readonly=True, description='Refresh token'),
})

delete_schema = api.model('Info', {
    'message': fields.String(readonly=True, description='revocation status'),
})


@api.route('/sign-up/')
class SignUp(Resource):
    @api.doc(description='Sign up')
    @api.expect(signup_parser)
    @api.marshal_with(signup_schema, code=CREATED)
    def post(self):
        data = signup_parser.parse_args()
        user = create_new_user(data)
        return user, CREATED


@api.route('/login/')
class Login(Resource):
    @api.doc(description='Login')
    @api.expect(login_parser)
    @api.marshal_with(login_schema, code=OK)
    def post(self):
        data = login_parser.parse_args()

        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            abort(NOT_FOUND, errors=['Пользователь не найден'])

        check_password = verify_password(data.get('password'), user.password)
        if not check_password:
            abort(NOT_FOUND, errors=['Некорректные данные для авторизации'])

        token = user.get_jwt_token()
        new_session = UserSessions(
            user_id=user.pk,
            user_agent=request.headers.get('User-Agent'),
            last_login=datetime.utcnow(),
            user_device_type=get_user_device_type(request.headers.get('User-Agent'))
        )
        new_session.save()
        return token, OK


@api.route('/logout/')
class LogOut(Resource):
    @api.doc('Logout')
    @api.marshal_with(delete_schema, code=OK)
    @jwt_required()
    def delete(self):
        token = get_jwt()
        jti = token['jti']
        ttype = token['type']
        jwt_redis_blocklist.set(jti, '', ex=Configuration.ACCESS_TOKEN_EXPIRE_TIME)
        return dict(message=f'{ttype.capitalize()} token successfully revoked')


@api.route('/refresh/')
class RefreshToken(Resource):
    @api.marshal_with(refresh_schema)
    @api.expect(refresh_schema_expected)
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        expire_time = timedelta(seconds=Configuration.ACCESS_TOKEN_EXPIRE_TIME)
        access_token = create_access_token(identity=identity, expires_delta=expire_time)
        return dict(access_token=access_token), OK
