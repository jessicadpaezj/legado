from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

db = SQLAlchemy(session_options={"expire_on_commit": False})
ma = Marshmallow()
jwt = JWTManager()
