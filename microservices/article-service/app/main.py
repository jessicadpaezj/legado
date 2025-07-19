from flask import Flask, jsonify
from app.db import get_db
from app.use_cases.commands.create_article_command import CreateArticleCommand
from app.use_cases.commands.update_article_command import UpdateArticleCommand
from app.use_cases.commands.delete_article_command import DeleteArticleCommand
from app.use_cases.queries.get_article_query import GetArticleQuery
from app.use_cases.queries.list_articles_query import ListArticlesQuery

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Article Microservice is running!"), 200

@app.route('/articles', methods=['POST'])
def create_article():
    db = next(get_db())
    command = CreateArticleCommand(title="Example Title", description="Example Description", body="Example Body", author_id=1)
    command.execute(db)
    return "Article created successfully!"

@app.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    db = next(get_db())
    command = UpdateArticleCommand(article_id=article_id, title="Updated Title")
    command.execute(db)
    return "Article updated successfully!"

@app.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    db = next(get_db())
    command = DeleteArticleCommand(article_id=article_id)
    command.execute(db)
    return "Article deleted successfully!"

@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    db = next(get_db())
    query = GetArticleQuery(article_id=article_id)
    article = query.execute(db)
    return article

@app.route('/articles', methods=['GET'])
def list_articles():
    db = next(get_db())
    query = ListArticlesQuery()
    articles = query.execute(db)
    return articles

if __name__ == '__main__':
    app.run(debug=True, port=3000)
