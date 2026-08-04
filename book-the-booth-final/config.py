"""
App configuration, pulled from environment variables (.env, git-ignored).
Postgres-only, per the project brief — no SQLite fallback.
"""

import os
from dotenv import load_dotenv

load_dotenv()

_required = ["DATABASE_URI", "SECRET_KEY", "JWT_SECRET_KEY"]
_missing = [key for key in _required if not os.environ.get(key)]
if _missing:
    raise RuntimeError(
        f"Missing required environment variable(s): {', '.join(_missing)}. "
        "Copy .env.example to .env and fill these in."
    )


class Config:
    _db_uri = os.environ["DATABASE_URI"]
    # Render (and Heroku) hand out "postgres://" URLs, but SQLAlchemy 1.4+
    # requires the "postgresql://" scheme. Normalize it here so it works
    # locally AND on Render without needing two different .env values.
    if _db_uri.startswith("postgres://"):
        _db_uri = _db_uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "*")