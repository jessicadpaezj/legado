from datetime import datetime
from slugify import slugify
from ..extensions import db
from .tag import Tag, article_tags

class Article(db.Model):
    __tablename__ = "articles"

    user_id       = db.Column(db.String(120), db.ForeignKey("users.id"), nullable=False)
    id            = db.Column(db.String(120), primary_key=True)
    slug          = db.Column(db.String(120), unique=True, nullable=False)
    title         = db.Column(db.String(120), nullable=False)
    description   = db.Column(db.String(255), nullable=False)
    body          = db.Column(db.Text, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tags = db.relationship(
        "Tag", secondary=article_tags, back_populates="articles", lazy="joined"
    )

    def __init__(self, title, description, body, author_id, tags=None):
        self.title = title
        self.description = description
        self.body = body
        self.user_id = author_id
        # slug podría no ser único si hay títulos repetidos; manejaremos en servicio.
        self.slug = slugify(title)
        if tags:
            self.tags = tags
