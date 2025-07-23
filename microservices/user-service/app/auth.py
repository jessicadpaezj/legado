from flask import request, g, abort
from flask_jwt_extended import decode_token
from .models.user import User

def authenticate():
    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Token "):
        abort(401, "Missing Token")

    try:
        token = auth.split(" ", 1)[1]
        payload = decode_token(token, allow_expired=False)
    except Exception:
        print("Invalid token")
        abort(401, "Invalid token")

    id = payload["sub"]

    user = User.query.filter_by(id=id).first()
    if not user:
        abort(401, "User not found")

    g.current_user = user
