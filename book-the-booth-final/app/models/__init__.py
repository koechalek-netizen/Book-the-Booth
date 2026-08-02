"""
Import every model here so Flask-Migrate can detect them via `from app.models import *`
inside app/__init__.py, without each route file needing its own long import list.
"""

from app.models.user import User
from app.models.profile import Profile
from app.models.session import Session
from app.models.booking import Booking

__all__ = ["User", "Profile", "Session", "Booking"]
