from extensions import db
from app.models.profile import Profile


class ProfileController:
    """CRUD for the 1:1 User <-> Profile relationship."""

    @classmethod
    def get_profile(cls, user_id):
        return Profile.query.filter_by(user_id=int(user_id)).first()

    @classmethod
    def update_profile(cls, user_id, data):
        profile = Profile.query.filter_by(user_id=int(user_id)).first()
        if not profile:
            return None

        if "phone" in data:
            profile.phone = data["phone"]
        if "location" in data:
            profile.location = data["location"]

        db.session.commit()
        return profile