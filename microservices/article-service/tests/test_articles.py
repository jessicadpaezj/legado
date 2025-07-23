import pytest
import bcrypt
from flask import g
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.config import Config

@pytest.fixture
def client():
    Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def get_or_create_user(app):
    with app.app_context():
        email = "a@b.com"
        password = "pass"

        user  = User.query.filter_by(email=email).first()
        if user:
            return user

        encoded_password = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode("utf-8")

        user = User(email=email, username="test_user", password=hashed_password)

        db.session.add(user)
        db.session.commit()
        return user


def get_token_from_user(app, user: User):
    with app.app_context():
        return create_access_token(identity=user.id)


# --- TEST CASES ---
def test_list_articles_empty(client):
    resp = client.get("/articles")
    assert resp.status_code == 200
    assert resp.json["articles"] == []
    assert resp.json["articlesCount"] == 0


def test_create_article_missing_payload(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    resp = client.post("/articles", headers={"Authorization": f"Token {token}"}, json={})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_create_article_missing_fields(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    # Missing title, description, body
    resp = client.post("/articles", headers={"Authorization": f"Token {token}"}, json={"article": {}})
    assert resp.status_code == 400
    assert "errors" in resp.json
    assert set(resp.json["errors"]).issuperset({"title", "description", "body"})


def test_create_article_success(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    payload = {"article": {"title": "New", "description": "desc", "body": "body"}}
    resp = client.post("/articles", headers={"Authorization": f"Token {token}"}, json=payload)
    assert resp.status_code == 201
    assert "article" in resp.json
    assert resp.json["article"]["title"] == "New"


def test_create_article_duplicate_title(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    with client.application.app_context():
        article = Article(slug="title", title="Title", description="desc", body="body", author_id=user.id)
        db.session.add(article)
        db.session.commit()

    payload = {"article": {"title": article.title, "description": "desc2", "body": "body2"}}
    resp = client.post("/articles", headers={"Authorization": f"Token {token}"}, json=payload)
    assert resp.status_code == 400
    assert "title" in resp.json["errors"]


def test_get_article_not_found(client):
    resp = client.get("/articles/unknown")
    assert resp.status_code == 404
    assert "error" in resp.json


def test_get_article_success(client):
    user = get_or_create_user(client.application)

    with client.application.app_context():
        article = Article(slug="title", title="Title", description="desc", body="body", author_id=user.id)
        db.session.add(article)
        db.session.commit()

    resp = client.get(f"/articles/{article.slug}")
    assert resp.status_code == 200
    assert resp.json["article"]["title"] == "Title"


def test_update_article_not_found(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    resp = client.put("/articles/unknown", headers={"Authorization": f"Token {token}"}, json={"article": {"title": "New"}})
    assert resp.status_code == 404
    assert "error" in resp.json


def test_update_article_duplicate_title(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    with client.application.app_context():
        article1 = Article(slug="title1", title="Title1", description="desc1", body="body1", author_id=user.id)
        article2 = Article(slug="title2", title="Title2", description="desc2", body="body2", author_id=user.id)
        db.session.add(article1)
        db.session.add(article2)
        db.session.commit()

    payload = {"article": {"title": f"{article2.title}"}}
    resp = client.put(f"/articles/{article1.slug}", headers={"Authorization": f"Token {token}"}, json=payload)
    assert resp.status_code == 400
    assert "error" in resp.json


def test_update_article_success(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    with client.application.app_context():
        article = Article(slug="title", title="Title", description="desc", body="body", author_id=user.id)
        db.session.add(article)
        db.session.commit()

    payload = {"article": {"title": "Updated", "description": "desc2", "body": "body2"}}
    resp = client.put(f"/articles/{article.slug}", headers={"Authorization": f"Token {token}"}, json=payload)
    assert resp.status_code == 200
    assert resp.json["article"]["title"] == "Updated"


def test_delete_article_not_found(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    resp = client.delete("/articles/unknown", headers={"Authorization": f"Token {token}"})
    assert resp.status_code == 404
    assert "error" in resp.json


def test_delete_article_success(client):
    user = get_or_create_user(client.application)
    token = get_token_from_user(client.application, user)

    with client.application.app_context():
        article = Article(slug="slug", title="Title", description="desc", body="body", author_id=user.id)
        db.session.add(article)
        db.session.commit()

    resp = client.delete(f"/articles/{article.slug}", headers={"Authorization": f"Token {token}"})
    assert resp.status_code == 204
    assert resp.data == b''
