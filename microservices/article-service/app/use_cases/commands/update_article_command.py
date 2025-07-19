from sqlalchemy.orm import Session
from app.models import Article

class UpdateArticleCommand:
    def __init__(self, article_id, title=None, description=None, body=None):
        self.article_id = article_id
        self.title = title
        self.description = description
        self.body = body

    def execute(self, db_session: Session):
        article = db_session.query(Article).filter(Article.id == self.article_id).first()
        if not article:
            raise Exception("Article not found")
        if self.title:
            article.title = self.title
        if self.description:
            article.description = self.description
        if self.body:
            article.body = self.body
        db_session.commit()
        return article
