from flask import Flask

from . import models
from .config import Config
from .db import init_db
from .routes.api import api_bp
from .routes.auth import auth_bp
from .routes.auth_api import api_auth_bp
from .routes.management_api import management_api_bp
from .routes.management_web import management_web_bp
from .routes.web import web_bp
from .services.auth import register_auth_handlers
from .services.factory import build_recommendation_service, recommend_shelters


def create_app(config_class=Config) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(config_class.TEMPLATE_DIR),
        static_folder=str(config_class.STATIC_DIR),
    )
    app.config.from_object(config_class)
    init_db(app)
    register_auth_handlers(app)

    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(management_web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_auth_bp, url_prefix="/api/auth")
    app.register_blueprint(management_api_bp, url_prefix="/api")
    return app


__all__ = ["Config", "build_recommendation_service", "create_app", "recommend_shelters"]
