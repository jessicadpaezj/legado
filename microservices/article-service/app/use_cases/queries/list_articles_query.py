from sqlalchemy.orm import Session
from app.models import Article

class ListArticlesQuery:
    def __init__(self, filters=None):
        self.filters = filters

    def execute(self, db_session: Session):
        query = db_session.query(Article)
        if self.filters:
            for key, value in self.filters.items():
                query = query.filter(getattr(Article, key) == value)
        return query.all()
