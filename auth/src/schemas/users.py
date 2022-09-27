from marshmallow import fields, validate
from models import User
from settings.main import ma


class UserSchema(ma.SQLAlchemySchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(
        required=True,
        validate=[validate.Length(max=255)]
    )
    password = fields.String(
        required=True,
        validate=[validate.Length(max=128)]
    )
    first_name = fields.String(
        required=False,
        allow_none=True,
        validate=[validate.Length(max=30)]
    )
    last_name = fields.String(
        required=False,
        allow_none=True,
        validate=[validate.Length(max=150)]
    )
    birth_date = fields.Date(required=False, allow_none=True)
    phone = fields.String(
        required=False,
        allow_none=True,
        validate=[validate.Length(max=50)]
    )
    created_at = fields.Date(required=False)
    active = fields.Boolean()

    class Meta:
        model = User


class PasswordSchema(ma.SQLAlchemySchema):
    password = fields.String(
        required=True,
        validate=[validate.Length(max=128)]
    )
