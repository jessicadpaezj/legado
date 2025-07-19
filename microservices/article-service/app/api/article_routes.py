from flask import Blueprint, request, abort, g
from ..auth import authenticate
from ..services.article_service import ArticleService
from ..schemas import article_schema, articles_schema

article_bp = Blueprint("articles", __name__)
protected  = ["POST", "PUT", "PATCH", "DELETE"]


@article_bp.get("/articles")
def list_articles():
    return ArticleService.get_all()


@article_bp.get("/articles/<string:slug>")
def get_article(slug: str):
    return ArticleService.get(slug)


@article_bp.post("/articles")
def create_article():
    authenticate()
    return ArticleService.create(request.get_json())


@article_bp.put("/articles/<string:slug>")
@article_bp.patch("/articles/<string:slug>")
def update_article(slug: str):
    authenticate()
    return ArticleService.update(slug, request.get_json())


@article_bp.delete("/articles/<string:slug>")
def delete_article(slug: str):
    authenticate()
    return ArticleService.delete(slug)
