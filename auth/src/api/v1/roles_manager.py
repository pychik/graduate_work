import http
from http.client import BAD_REQUEST

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort, fields
from helpers.decorators import jwt_roles_accepted
from helpers.parsers import role_manager_parser
from helpers.responses import DELETE_RESPONSES, MAIN_RESPONSES
from marshmallow import ValidationError
from models import Role as RoleModel, User
from settings.datastore import security


api = Namespace('roles/manager', description='Управление ролями пользователей')
api_schema = api.model('InfoRole', {
    'message': fields.String(readonly=True, description='Сообщение')
})


@api.route('/access/', endpoint='roles-access')
class RoleManage(Resource):
    @api.doc(description='Добавление роли пользователю', responses=MAIN_RESPONSES)
    @api.expect(role_manager_parser)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def post(self):
        data = role_manager_parser.parse_args()
        try:
            user = User.query.get_or_404(data.get('user_pk', None))
            role = RoleModel.get_by_name(data.get('role', None))
            user.add_role(role, security)
            return {'message': 'Роль пользователю присвоена.'}, http.HTTPStatus.OK
        except ValidationError as err:
            abort(BAD_REQUEST, errors=err.messages)
        except Exception as err:
            abort(BAD_REQUEST, errors=[str(err)])

    @api.doc(description='Удаление роли пользователя', responses=DELETE_RESPONSES)
    @api.expect(role_manager_parser)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def delete(self):
        data = role_manager_parser.parse_args()
        try:
            user = User.query.get_or_404(data.get('user_pk', None))
            role = RoleModel.get_by_name(data.get('role', None))
            user.delete_role(role, security)
            return {'message': 'Роль у пользователя отобрана.'}, http.HTTPStatus.NO_CONTENT
        except Exception as err:
            abort(BAD_REQUEST, errors=[str(err)])


@api.route('/check/', endpoint='roles-check')
class RoleCheck(Resource):
    @api.doc(description='Проверка наличия роли у пользователя', responses=MAIN_RESPONSES)
    @api.expect(role_manager_parser)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def post(self):
        data = role_manager_parser.parse_args()
        try:
            user = User.query.get_or_404(data.get('user_pk', None))
            role = RoleModel.get_by_name(data.get('role', None))
            if user.has_role(role):
                return {'message': True}, http.HTTPStatus.OK
            return {'message': False}, http.HTTPStatus.OK
        except ValidationError as err:
            abort(BAD_REQUEST, errors=err.messages)
        except Exception as err:
            abort(BAD_REQUEST, errors=[str(err)])
