from datetime import datetime
from ..extensions import db
from .tag import article_tags
from .user import User
import uuid

class Article(db.Model):
    __tablename__ = "articles"

    id            = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug          = db.Column(db.String(120), unique=True, nullable=False)
    title         = db.Column(db.String(120), nullable=False)
    description   = db.Column(db.String(255), nullable=False)
    body          = db.Column(db.Text, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id       = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    author        = db.relationship(User, lazy="joined")

    tags = db.relationship("Tag", secondary=article_tags, back_populates="articles", lazy="joined")

    def __init__(self, slug, title, description, body, author_id, tags=None):
        self.slug        = slug
        self.title       = title
        self.description = description
        self.body        = body
        self.user_id     = author_id
        self.tags        = tags or []
