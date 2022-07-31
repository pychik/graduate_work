from functools import wraps
from http.client import FORBIDDEN

from flask_jwt_extended import get_jwt_identity
from flask_restx import abort


def jwt_roles_accepted(model, *roles: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_id = get_jwt_identity()
            user = model.get_by_pk(user_id)
            if not user or not user.roles:
                abort(FORBIDDEN, errors=['Доступ запрещен.'])

            user_roles = set(role.name for role in user.roles)
            if not user_roles.intersection(roles):
                abort(FORBIDDEN, errors=['Доступ запрещен.'])

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
