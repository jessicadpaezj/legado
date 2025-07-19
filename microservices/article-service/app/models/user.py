from ..extensions import db

class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.String(36), primary_key=True)
    username      = db.Column(db.String(50), nullable=False)
    bio           = db.Column(db.Text)
    image         = db.Column(db.String)
