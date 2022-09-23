from flask_restx import inputs, reqparse
from settings.config import configuration


list_parser = reqparse.RequestParser(bundle_errors=True)
list_parser.add_argument(
    'page',
    type=int,
    default=1,
    help='page',
    location='args'
)
list_parser.add_argument(
    'per_page',
    type=int,
    default=configuration.PAGINATION_PER_PAGE,
    help='Count items per page',
    location='args'
)


role_new_parser = reqparse.RequestParser(bundle_errors=True)
role_new_parser.add_argument(
    'name',
    required=True,
    type=str,
    help='Role name',
    location='json'
)
role_new_parser.add_argument(
    'description',
    required=False,
    type=str,
    help='Role description',
    location='json'
)


signup_parser = reqparse.RequestParser(bundle_errors=True)
signup_parser.add_argument(
    'email',
    required=True,
    type=inputs.email(),
    help='Email',
    location='json'
)
signup_parser.add_argument(
    'password',
    required=True,
    type=str,
    help='Password',
    location='json'
)
signup_parser.add_argument(
    'first_name',
    required=False,
    type=str,
    help='Firstname',
    location='json'
)
signup_parser.add_argument(
    'last_name',
    required=False,
    type=str,
    help='Lastname',
    location='json'
)
signup_parser.add_argument(
    'birth_date',
    required=False,
    type=str,
    help='Birthday',
    location='json'
)
signup_parser.add_argument(
    'phone',
    required=False,
    type=str,
    help='Phone number',
    location='json'
)


login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument(
    'email',
    required=True,
    type=inputs.email(),
    help='Email',
    location='json'
)
login_parser.add_argument(
    'password',
    required=True,
    type=str,
    help='Password',
    location='json'
)

password_update_parser = reqparse.RequestParser(bundle_errors=True)
password_update_parser.add_argument(
    'old_password',
    required=True,
    type=str,
    help='Old password',
    location='json'
)
password_update_parser.add_argument(
    'new_password',
    required=True,
    type=str,
    help='New password',
    location='json'
)


role_manager_parser = reqparse.RequestParser(bundle_errors=True)
role_manager_parser.add_argument(
    'user_pk',
    required=True,
    type=int,
    help='User ID',
    location='json'
)
role_manager_parser.add_argument(
    'role',
    required=True,
    type=str,
    help='Role',
    location='json'
)

callback_code_parser = reqparse.RequestParser(bundle_errors=True)
callback_code_parser.add_argument(
    'code',
    required=True,
    type=int,
    help='Callback code',
    location='args'
)
