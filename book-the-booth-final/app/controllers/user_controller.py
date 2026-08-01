from app.models.user import User


class UserController:
    """Read access to user records — not auth, not admin moderation."""

    @classmethod
    def get_user_by_id(cls, user_id):
        """TODO: User.query.get(user_id)"""
        pass

    @classmethod
    def get_current_user(cls, jwt_identity):
        """TODO: User.query.get(int(jwt_identity)) — jwt identity is stored as a string"""
        pass
