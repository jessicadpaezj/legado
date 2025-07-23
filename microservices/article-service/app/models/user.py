import uuid
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email         = db.Column(db.String(50), nullable=False)
    username      = db.Column(db.String(50), nullable=False)
    password      = db.Column(db.String(128), nullable=False)
    bio           = db.Column(db.Text)
    image         = db.Column(db.String)

    def __init__(self, email, username, password, bio=None, image=None):
        self.email    = email
        self.username = username
        self.password = password
        self.bio      = bio or ""
        self.image    = image or ""
