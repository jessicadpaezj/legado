from sqlalchemy.orm import Session
from app.models import Article

class GetArticleQuery:
    def __init__(self, article_id):
        self.article_id = article_id

    def execute(self, db_session: Session):
        article = db_session.query(Article).filter(Article.id == self.article_id).first()
        if not article:
            raise Exception("Article not found")
        return article
