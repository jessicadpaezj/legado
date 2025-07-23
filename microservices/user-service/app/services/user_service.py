import bcrypt
from ..extensions import db
from ..models.user import User
from ..schemas import user_schema

class UserService:
    @staticmethod
    def _validate_create(payload: dict):
        erros = {}

        email = payload.get("email")
        if not email:
            erros["email"] = ["can't be empty"]

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            erros["email"] = ["duplicated email"]

        password = payload.get("password")
        if not password:
            erros["password"] = ["can't be empty"]

        username = payload.get("username")
        if not username:
            erros["username"] = ["can't be empty"]

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            erros["username"] = ["duplicated username"]

        return erros


    @staticmethod
    def _validate_login(payload: dict):
        erros = {}

        email = payload.get("email")
        if not email:
            erros["email"] = ["can't be empty"]

        password = payload.get("password")
        if not password:
            erros["password"] = ["can't be empty"]

        return erros


    @staticmethod
    def create(payload: dict):
        if not payload or "user" not in payload:
            return {"error": "Invalid payload - expected {'user': {...}}"}, 400

        data = payload["user"]
        errors = UserService._validate_create(data)
        if errors:
            return {"errors": errors}, 400

        password = data["password"].encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

        user = User(email=data["email"], username=data["username"], 
                    password=hashed_password, bio=data.get("bio"), image=data.get("image"))

        db.session.add(user)
        db.session.commit()

        return {"user": user_schema.dump(user)}, 201


    @staticmethod
    def login(payload: dict):
        if not payload or "user" not in payload:
            return {"error": "Invalid payload - expected {'user': {...}}"}, 400

        data = payload["user"]
        errors = UserService._validate_login(data)
        if errors:
            return {"errors": errors}, 400

        user = User.query.filter_by(email=data["email"]).first()
        if user is None:
            return {"message": "Invalid email or password"}, 401

        password = data["password"].encode("utf-8")
        if bcrypt.checkpw(password, user.password.encode("utf-8")) is False:
            return {"message": "Invalid email or password"}, 401

        result = {"user": user_schema.dump(user)}
        return result, 200
