try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError:  # pragma: no cover - optional until dependency install
    SQLAlchemy = None

try:
    from flask_migrate import Migrate
except ImportError:  # pragma: no cover - optional until dependency install
    Migrate = None


db = SQLAlchemy() if SQLAlchemy is not None else None
migrate = Migrate() if Migrate is not None else None


def init_db(app):
    if db is not None:
        db.init_app(app)
    if migrate is not None and db is not None:
        migrate.init_app(app, db)
