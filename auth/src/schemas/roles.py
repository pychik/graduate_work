from marshmallow import fields
from marshmallow.validate import Length
from models import Role
from settings.main import ma


class RoleSchema(ma.SQLAlchemySchema):
    name = fields.Str(required=True, validate=[Length(min=4, max=50)])
    description = fields.Str(
        required=False,
        allow_none=True,
        validate=[Length(max=255)]
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Role
