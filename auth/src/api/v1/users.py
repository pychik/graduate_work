from http.client import NOT_FOUND, OK, UNPROCESSABLE_ENTITY

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, abort, fields
from flask_security.utils import hash_password, verify_password
from helpers.decorators import jwt_roles_accepted
from helpers.parsers import list_parser, password_update_parser
from marshmallow import ValidationError
from models import User, UserSessions


api = Namespace('users', description='Users profile')
user_schema = api.model('Profile', {
    'email': fields.String(required=True, description='Email'),
    'first_name': fields.String(readonly=True),
    'last_name': fields.String(readonly=True),
    'birth_date': fields.Date(readonly=True),
    'phone': fields.String(readonly=True),
})

user_sessions_schema = api.model('UserSessions', {
    'user_agent': fields.String(readonly=True),
    'user_device_type': fields.String(readonly=True),
    'last_login': fields.DateTime(readonly=True)

})

pagination_schema = api.model('UserSessionPaginate', {
    'total': fields.Integer(readonly=True),
    'page': fields.Integer(readonly=True),
    'per_page': fields.Integer(readonly=True),
    'pages': fields.Integer(readonly=True),
    'items': fields.List(fields.Nested(user_sessions_schema))
})


@api.route('/profile/')
class Profile(Resource):

    @api.doc(description='Profile info')
    @api.marshal_with(user_schema, envelope='profile')
    @jwt_required()
    @jwt_roles_accepted(User, 'admin', 'manager', 'user')
    def get(self):
        pk = get_jwt_identity()
        return User.query.get_or_404(pk)

    @api.doc(description='Update profile password')
    @api.expect(password_update_parser)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin', 'manager', 'user')
    def put(self):
        from schemas.users import PasswordSchema

        data = password_update_parser.parse_args()
        user = User.query.get_or_404(get_jwt_identity())

        check_password = verify_password(data.get('old_password'), user.password)
        if not check_password:
            abort(NOT_FOUND, errors=['Указан не верный пароль учетной записи!'])

        try:
            validated_data = PasswordSchema().load(dict(password=data.get('new_password')))
            new_hash_password = hash_password(validated_data.get('password'))
            user.update(password=new_hash_password)
        except ValidationError as err:
            abort(UNPROCESSABLE_ENTITY, errors=err.messages)
        return 'Success!', OK


@api.route('/profile/sessions/')
class ProfileSessions(Resource):
    @api.doc(description='Profile sessions')
    @api.expect(list_parser)
    @api.marshal_with(pagination_schema)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin', 'manager', 'user')
    def get(self):
        args = list_parser.parse_args()
        pk = get_jwt_identity()
        queryset = UserSessions.query.filter_by(user_id=pk).order_by(UserSessions.last_login.desc())
        return queryset.paginate(args['page'], args['per_page'], error_out=False)


@api.route('/check_token/')
class UserCheck(Resource):
    @api.doc(description='Check user authorization')
    # @jwt_required()
    def post(self):
        return {'success': True}, 200
