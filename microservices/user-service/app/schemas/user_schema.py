from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.user import User

class UserSchema(SQLAlchemyAutoSchema):
    token = fields.Method("_token")

    class Meta:
        model   = User
        exclude = ("id", "password", )
        ordered = True

    def _token(self, obj):
        from flask_jwt_extended import create_access_token
        return create_access_token(identity=obj.id)

user_schema = UserSchema()
