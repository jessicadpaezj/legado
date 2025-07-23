import pytest

from app import create_app, db
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


# --- TEST CASES ---
def test_create_user_missing_payload(client):
    resp = client.post("/users", json={})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_create_user_missing_fields(client):
    payload = {"user": {}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 400
    assert "errors" in resp.json
    assert set(resp.json["errors"]).issuperset({"email", "username", "password"})


def test_create_user_duplicate_email(client):
    with client.application.app_context():
        user = User(email="a@b.com", username="user1", password="pass")
        db.session.add(user)
        db.session.commit()

    payload = {"user": {"email": user.email, "username": "user2", "password": "pass"}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 400
    assert "email" in resp.json["errors"]


def test_create_user_duplicate_username(client):
    with client.application.app_context():
        user = User(email="a2@b.com", username="user", password="pass")
        db.session.add(user)
        db.session.commit()

    payload = {"user": {"email": "a3@b.com", "username": user.username, "password": "pass"}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 400
    assert "username" in resp.json["errors"]


def test_create_user_success(client):
    payload = {"user": {"email": "a@b.com", "username": "user", "password": "pass"}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201
    assert "user" in resp.json
    assert resp.json["user"]["email"] == "a@b.com"
    assert resp.json["user"]["username"] == "user"
    assert "token" in resp.json["user"]


def test_login_missing_payload(client):
    resp = client.post("/users/login", json={})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_login_missing_fields(client):
    payload = {"user": {}}
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 400
    assert "errors" in resp.json
    assert set(resp.json["errors"]).issuperset({"email", "password"})


def test_login_invalid_email(client):
    payload = {"user": {"email": "notfound@b.com", "password": "pass"}}
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 401
    assert "message" in resp.json


def test_login_invalid_password(client):
    # Create user
    payload = {"user": {"email": "a@b.com", "username": "user", "password": "pass"}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201

    # Try login with wrong password
    payload = {"user": {"email": "a@b.com", "password": "wrong"}}
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 401
    assert "message" in resp.json


def test_login_success(client):
    # Create user
    payload = {"user": {"email": "a@b.com", "username": "user", "password": "pass"}}
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201

    # Login
    payload = {"user": {"email": "a@b.com", "password": "pass"}}
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 200
    assert "user" in resp.json
    assert resp.json["user"]["email"] == "a@b.com"
    assert resp.json["user"]["username"] == "user"
