import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def _normalize_database_url(database_url: str | None) -> str | None:
    if not database_url:
        return None
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "shelter.db"))
    DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL"))
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f"sqlite:///{Path(DB_PATH)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").strip().lower() == "true"
    FLASK_RUN_HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    FLASK_RUN_PORT = int(os.getenv("FLASK_RUN_PORT", "5000"))
    TEMPLATE_DIR = BASE_DIR / "templates"
    STATIC_DIR = BASE_DIR / "static"
