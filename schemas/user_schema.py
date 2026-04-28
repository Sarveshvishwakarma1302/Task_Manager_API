from marshmallow import Schema, fields, validate, validates, ValidationError
from models.user import User

class UserRegisterSchema(Schema):
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=20)
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=6)
    )

    role = fields.String(
        required=True,
        validate=validate.OneOf(["admin", "user"])
    )

    # COMBINED VALIDATION
    @validates("username")
    def validate_username(self, value, **kwargs):

        # length check (optional, already above but safe)
        if len(value) < 3:
            raise ValidationError("Username too short")

        if " " in value:
            raise ValidationError("Username should not contain spaces")

        if User.query.filter_by(username=value).first():
            raise ValidationError("Username already exists")

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)