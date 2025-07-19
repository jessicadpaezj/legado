from flask import Flask
from .config import Config
from .extensions import db, ma, jwt
from .api.article_routes import article_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(article_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    with app.app_context():
        from sqlalchemy.ext.automap import automap_base
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        app.Base = Base

    return app
