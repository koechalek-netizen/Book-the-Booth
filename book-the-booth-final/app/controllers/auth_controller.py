from extensions import db
from app.models.user import User
from app.models.profile import Profile


class AuthController:
    """Handles registration and login. Routes stay thin, this does the work."""

    @classmethod
    def register_user(cls, data):
        """
        TODO:
        - validate role via app.utils.validators.is_valid_role (default "artist")
        - user = User(username=data["username"], email=data["email"], role=data.get("role", "artist"))
        - user.set_password(data["password"])
        - db.session.add(user); db.session.flush()   # get user.id before commit
        - profile = Profile(user_id=user.id, phone=data.get("phone"), location=data.get("location"))
        - db.session.add(profile); db.session.commit()
        - return user
        """
        pass

    @classmethod
    def authenticate_user(cls, username, password):
        """
        TODO:
        - user = User.query.filter_by(username=username).first()
        - if user and user.check_password(password): return user
        - return None (don't reveal which part failed)
        """
        pass
