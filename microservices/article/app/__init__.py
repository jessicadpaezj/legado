from flask import Flask
from .config import Config
from .extensions import db, ma
from .api.article_routes import article_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(article_bp, url_prefix="/api")

    # Simple health‑check
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    with app.app_context():
        from sqlalchemy.ext.automap import automap_base
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        app.Base = Base

    return app
