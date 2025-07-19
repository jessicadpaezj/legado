from flask import g
from slugify import slugify

from ..extensions import db
from ..models.article import Article
from ..models.tag import Tag
from ..schemas import article_schema, articles_schema

class ArticleService:
    @staticmethod
    def _get_or_create_tags(tag_names):
        tags = []
        for name in tag_names or []:
            tag = Tag.query.filter_by(name=name).one_or_none()
            if not tag:
                tag = Tag(name=name)
            tags.append(tag)
        return tags


    @staticmethod
    def _unique_slug(title):
        base = slugify(title)
        slug = base
        i = 1
        while Article.query.filter_by(slug=slug).first():
            slug = f"{base}-{i}"
            i += 1
        return slug


    @staticmethod
    def _validate(payload: dict):
        errors = {}

        title = payload.get("title")
        if not title:
            errors["title"] = ["can't be empty"]

        existing_article = Article.query.filter_by(title=title).first()
        if existing_article is not None:
            errors["title"] = ["article name exists"]

        description = payload.get("description")
        if not description:
            errors["description"] = ["can't be empty"]

        body = payload.get("body")
        if not body:
            errors["body"] = ["can't be empty"]

        return errors


    @staticmethod
    def get_all():
        articles = Article.query.all()
        payload = {
            "articles": articles_schema.dump(articles),
            "articlesCount": len(articles),
        }
        return payload, 200


    @staticmethod
    def get(slug: str):
        article = Article.query.filter_by(slug=slug).first()
        if article is None:
            return {"error": "Article not found"}, 404

        return {"article": article_schema.dump(article)}, 200


    @staticmethod
    def create(payload: dict):
        if not payload or "article" not in payload:
            return {"error": "Invalid payload - expected {'article': {...}}"}, 400

        data = payload["article"]
        errors = ArticleService._validate(data)
        if errors:
            return {"errors": errors}, 400

        tag_names = data.pop("tagList", [])
        tags      = ArticleService._get_or_create_tags(tag_names)
        slug      = ArticleService._unique_slug(data["title"])
        article   = Article(slug=slug, tags=tags, author_id=g.current_user.id, **data)

        db.session.add(article)
        db.session.commit()
        return {"article": article_schema.dump(article)}, 201


    @staticmethod
    def update(slug: str, payload: dict):
        if not payload or "article" not in payload:
            return {"error": "Invalid payload - expected {'article': {...}}"}, 400

        article = Article.query.filter_by(slug=slug).first()
        if article is None:
            return {"error": "Article not found"}, 404

        data: dict  = payload.get("article")
        title       = data.get("title")

        if title:
            new_slug = slugify(title)
            new_article = Article.query.filter_by(slug=new_slug).first()
            if new_article and article != new_article:
                return {"error": "Article with this title already exists"}, 400

            if title != article.title:
                article.title = title
                article.slug  = ArticleService._unique_slug(title)

        description = data.get("description")
        if description:
            article.description = description

        body = data.get("body")
        if body:
            article.body = body

        db.session.commit()
        return {"article": article_schema.dump(article)}, 200


    @staticmethod
    def delete(slug: str):
        article = Article.query.filter_by(slug=slug).first()
        if article is None:
            return {"error": "Article not found"}, 404

        db.session.delete(article)
        db.session.commit()
        return {}, 204
