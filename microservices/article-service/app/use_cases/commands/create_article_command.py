from sqlalchemy.orm import Session
from app.models import Article

class CreateArticleCommand:
    def __init__(self, title, description, body, author_id):
        self.title = title
        self.description = description
        self.body = body
        self.author_id = author_id

    def execute(self, db_session: Session):
        new_article = Article(
            title=self.title,
            description=self.description,
            body=self.body,
            author_id=self.author_id
        )
        db_session.add(new_article)
        db_session.commit()
        return new_article
