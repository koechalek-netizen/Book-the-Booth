from extensions import db
from app.models.user import User
from app.models.profile import Profile
from app.utils.validators import is_valid_role


class AuthController:
    """Handles registration and login. Routes stay thin, this does the work."""

    @classmethod
    def register_user(cls, data):
        role = data.get("role", "artist")
        if not is_valid_role(role):
            role = "artist"

        user = User(
            username=data["username"],
            email=data["email"],
            role=role,
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.flush()  # assigns user.id before we build the Profile

        profile = Profile(
            user_id=user.id,
            phone=data.get("phone"),
            location=data.get("location"),
        )
        db.session.add(profile)
        db.session.commit()

        return user

    @classmethod
    def authenticate_user(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None