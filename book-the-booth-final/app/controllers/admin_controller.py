from extensions import db
from app.models.user import User
from app.models.profile import Profile
from app.models.session import Session
from app.models.booking import Booking


class AdminController:
    """
    Actions only an admin can take: verifying studio owner accounts and
    pulling down listings/bookings that break platform rules.
    """

    @classmethod
    def get_all_users(cls, page=1, per_page=20):
        return User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @classmethod
    def verify_studio_owner(cls, user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return None
        profile.is_verified = True
        db.session.commit()
        return profile

    @classmethod
    def remove_session(cls, session_id):
        session = Session.query.get(session_id)
        if not session:
            return False
        db.session.delete(session)  # cascades to its Bookings
        db.session.commit()
        return True

    @classmethod
    def remove_booking(cls, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False
        db.session.delete(booking)
        db.session.commit()
        return True