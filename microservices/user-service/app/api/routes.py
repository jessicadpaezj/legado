from flask import Blueprint, request
from ..services.user_service import UserService

blueprint = Blueprint("users", __name__)


@blueprint.post("/users")
def createUser():
    return UserService.create(request.get_json())


@blueprint.post("/users/login")
def login():
    return UserService.login(request.get_json())
