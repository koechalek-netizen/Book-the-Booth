"""
Small, dependency-free validation helpers. Nothing here talks to the
database — that belongs in the controllers.
"""

import re
from datetime import datetime

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(email) and bool(_EMAIL_RE.match(email))


def is_positive_number(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_valid_role(role):
    return role in ("artist", "studio_owner", "admin")


def parse_date(value):
    """
    Incoming JSON only has strings — "2026-08-10" — but a SQLAlchemy Date
    column needs an actual date object, on SQLite AND on Postgres.
    Raises ValueError (caught by the route) if the format is wrong.
    """
    if hasattr(value, "year"):  # already a date/datetime object
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()
