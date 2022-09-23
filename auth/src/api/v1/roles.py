from http.client import BAD_REQUEST, CREATED, NO_CONTENT

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort, fields
from helpers.decorators import jwt_roles_accepted
from helpers.parsers import list_parser, role_new_parser
from helpers.responses import ADD_RESPONSES, DELETE_RESPONSES, MAIN_RESPONSES, READ_RESPONSES
from marshmallow import ValidationError
from models import Role as RoleModel, User


api = Namespace('roles', description='Роли пользователей')
api_schema = api.model('Role', {
    'pk': fields.Integer(readonly=True, description='ID роли'),
    'name': fields.String(required=True, description='Название'),
    'description': fields.String(required=False, description='Описание'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
})
list_schema = api.model('RolePaginate', {
    'total': fields.Integer(readonly=True),
    'page': fields.Integer(readonly=True),
    'per_page': fields.Integer(readonly=True),
    'pages': fields.Integer(readonly=True),
    'items': fields.List(fields.Nested(api_schema))
})


@api.route('/', endpoint='roles')
class RoleList(Resource):
    @api.doc(description='Список', responses=READ_RESPONSES)
    @api.expect(list_parser)
    @api.marshal_list_with(list_schema)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin', 'manager')
    def get(self):
        args = list_parser.parse_args()
        queryset = RoleModel.query.order_by(RoleModel.created_at.asc())
        return queryset.paginate(
            page=args['page'], per_page=args['per_page'], error_out=False
        )

    @api.doc(description='Создание', responses=ADD_RESPONSES)
    @api.expect(role_new_parser)
    @api.marshal_with(api_schema, code=CREATED)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin', 'manager')
    def post(self):
        from schemas.roles import RoleSchema

        try:
            data = role_new_parser.parse_args()
            validated_data = RoleSchema().load(data)
            return RoleModel.create(**validated_data), CREATED
        except ValidationError as err:
            abort(BAD_REQUEST, errors=err.messages)
        except Exception as err:
            abort(BAD_REQUEST, errors=str(err))


@api.route('/<int:pk>/', endpoint='roles-detail')
@api.param('pk', 'ID роли')
class Role(Resource):
    @api.doc(description='Получение', responses=READ_RESPONSES)
    @api.marshal_with(api_schema)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def get(self, pk):
        return RoleModel.query.get_or_404(pk)

    @api.doc(description='Обновление', responses=MAIN_RESPONSES)
    @api.expect(role_new_parser)
    @api.marshal_with(api_schema)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def put(self, pk):
        from schemas.roles import RoleSchema

        try:
            role = RoleModel.query.get_or_404(pk)
            data = role_new_parser.parse_args()
            validated_data = RoleSchema().load(data)
            role.update(commit=True, **validated_data)
            return role
        except ValidationError as err:
            abort(BAD_REQUEST, errors=[err.messages])
        except Exception as err:
            abort(BAD_REQUEST, errors=[str(err)])

    @api.doc(description='Удаление', responses=DELETE_RESPONSES)
    @api.marshal_with(api_schema)
    @jwt_required()
    @jwt_roles_accepted(User, 'admin')
    def delete(self, pk):
        role = RoleModel.query.get_or_404(pk)
        role.delete()
        return 'deleted', NO_CONTENT
