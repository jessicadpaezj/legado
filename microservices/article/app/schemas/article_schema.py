from marshmallow import fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.article import Article

class ArticleSchema(SQLAlchemyAutoSchema):
    tagList = fields.Method("_get_tag_list")

    class Meta:
        model = Article
        load_instance = True
        include_fk = True
        ordered = True
        exclude = ("tags", "id")  # ocultamos detalles internos

    def _get_tag_list(self, obj):
        return [tag.name for tag in obj.tags]

    @post_dump(pass_original=True)
    def wrap(self, data, original, **kwargs):
        # Ajustamos al formato {"article": {...}}
        return {"article": data}

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
