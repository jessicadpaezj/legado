from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.user import User

class AuthorSchema(SQLAlchemyAutoSchema):
    following = fields.Constant(False)

    class Meta:
        model   = User
        fields  = ("username", "bio", "image", "following")
        ordered = True
