from ..extensions import db

article_tags = db.Table(
    "article_tags",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    articles = db.relationship(
        "Article", secondary=article_tags, back_populates="tags", lazy="joined"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
