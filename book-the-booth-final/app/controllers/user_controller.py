from app.models.user import User


class UserController:
    """Read access to user records — not auth, not admin moderation."""

    @classmethod
    def get_user_by_id(cls, user_id):
        return User.query.get(user_id)

    @classmethod
    def get_user_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_current_user(cls, jwt_identity):
        # jwt identity is stored as a string; ids are ints
        return User.query.get(int(jwt_identity))