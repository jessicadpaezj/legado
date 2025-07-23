from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.article import Article
from .author_schema import AuthorSchema

class ArticleSchema(SQLAlchemyAutoSchema):
    tagList        = fields.Method("_tags")
    createdAt      = fields.DateTime(attribute="created_at")
    updatedAt      = fields.DateTime(attribute="updated_at")
    favorited      = fields.Constant(False)
    favoritesCount = fields.Constant(0)
    cursor         = fields.Method("_cursor")
    author         = fields.Nested(AuthorSchema)

    class Meta:
        model         = Article
        load_instance = True
        include_fk    = True
        ordered       = True
        exclude       = ("tags", "created_at", "updated_at", "user_id")

    def _tags(self, obj):
        return [t.name for t in obj.tags]

    def _cursor(self, obj):
        return {"data": obj.created_at.isoformat()} if obj.created_at else None

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
