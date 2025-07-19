from flask import Blueprint, request, abort, jsonify
from ..services.article_service import ArticleService
from ..schemas import article_schema, articles_schema

article_bp = Blueprint("articles", __name__)

# GET /api/articles
@article_bp.get("/articles")
def list_articles():
    articles = ArticleService.list2()
    return articles_schema.dump(articles), 200

# GET /api/articles/<slug>
@article_bp.get("/articles/<string:slug>")
def get_article(slug):
    article = ArticleService.get(slug)
    return article_schema.dump(article), 200

# POST /api/articles
@article_bp.post("/articles")
def create_article():
    json_data = request.get_json()
    if not json_data or "article" not in json_data:
        abort(400, "Invalid payload – expected {'article': {...}}")
    article = ArticleService.create(json_data["article"])
    return article_schema.dump(article), 201

# PUT /api/articles/<slug>
@article_bp.put("/articles/<string:slug>")
@article_bp.patch("/articles/<string:slug>")
def update_article(slug):
    json_data = request.get_json()
    if not json_data or "article" not in json_data:
        abort(400, "Invalid payload – expected {'article': {...}}")
    article = ArticleService.update(slug, json_data["article"])
    return article_schema.dump(article), 200

# DELETE /api/articles/<slug>
@article_bp.delete("/articles/<string:slug>")
def delete_article(slug):
    ArticleService.delete(slug)
    return {}, 204
