from slugify import slugify
from ..extensions import db
from ..models.article import Article
from ..models.tag import Tag

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
    def list():
        return Article.query.all()
    
    @staticmethod
    def list2():
        return Article.query.all()

    @staticmethod
    def get(slug: str):
        return Article.query.filter_by(slug=slug).first_or_404()

    @staticmethod
    def create(payload: dict):
        tag_names = payload.pop("tagList", [])
        tags = ArticleService._get_or_create_tags(tag_names)
        slug = ArticleService._unique_slug(payload["title"])
        article = Article(slug=slug, tags=tags, **payload)
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def update(slug: str, payload: dict):
        tag_names = payload.pop("tagList", None)
        article = Article.query.filter_by(slug=slug).first_or_404()
        for key, value in payload.items():
            setattr(article, key, value)
        if tag_names is not None:
            article.tags = ArticleService._get_or_create_tags(tag_names)
        db.session.commit()
        return article

    @staticmethod
    def delete(slug: str):
        article = Article.query.filter_by(slug=slug).first_or_404()
        db.session.delete(article)
        db.session.commit()
