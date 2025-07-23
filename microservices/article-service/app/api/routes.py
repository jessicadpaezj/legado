from flask import Blueprint, request
from ..auth import authenticate
from ..services.article_service import ArticleService

blueprint = Blueprint("articles", __name__)


@blueprint.get("/articles")
def list_articles():
    return ArticleService.get_all()


@blueprint.get("/articles/<string:slug>")
def get_article(slug: str):
    return ArticleService.get(slug)


@blueprint.post("/articles")
def create_article():
    authenticate()
    return ArticleService.create(request.get_json())


@blueprint.put("/articles/<string:slug>")
@blueprint.patch("/articles/<string:slug>")
def update_article(slug: str):
    authenticate()
    return ArticleService.update(slug, request.get_json())


@blueprint.delete("/articles/<string:slug>")
def delete_article(slug: str):
    authenticate()
    return ArticleService.delete(slug)
