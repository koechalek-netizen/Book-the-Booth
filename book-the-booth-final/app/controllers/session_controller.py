from extensions import db
from app.models.session import Session
from app.models.booking import Booking
from app.models.user import User
from app.models.profile import Profile
from app.utils.validators import parse_date


class SessionController:
    """CRUD for Session listings, plus deep-query endpoints."""

    @classmethod
    def get_all_sessions(cls, page=1, per_page=10, genre=None, status="open"):
        query = Session.query
        if status:
            query = query.filter_by(status=status)
        if genre:
            query = query.filter_by(genre_focus=genre)
        query = query.order_by(Session.date_available.asc())
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get_session_by_id(cls, session_id):
        return Session.query.get(session_id)

    @classmethod
    def create_session(cls, studio_owner_id, data):
        session = Session(
            studio_owner_id=int(studio_owner_id),
            room_name=data["room_name"],
            genre_focus=data.get("genre_focus"),
            hourly_rate=data["hourly_rate"],
            date_available=parse_date(data["date_available"]),
            status=data.get("status", "open"),
        )
        db.session.add(session)
        db.session.commit()
        return session

    @classmethod
    def update_session(cls, session_id, data):
        session = Session.query.get(session_id)
        if not session:
            return None

        for field in ("room_name", "genre_focus", "hourly_rate", "status"):
            if field in data:
                setattr(session, field, data[field])
        if "date_available" in data:
            session.date_available = parse_date(data["date_available"])

        db.session.commit()
        return session

    @classmethod
    def delete_session(cls, session_id):
        session = Session.query.get(session_id)
        if not session:
            return False
        db.session.delete(session)
        db.session.commit()
        return True

    @classmethod
    def sessions_with_booking_counts(cls):
        """Deep query #1: aggregation + outer join + group_by."""
        results = (
            db.session.query(Session, db.func.count(Booking.id).label("booking_count"))
            .outerjoin(Booking, Booking.session_id == Session.id)
            .group_by(Session.id)
            .all()
        )
        return [
            {
                "session_id": session.id,
                "room_name": session.room_name,
                "genre_focus": session.genre_focus,
                "booking_count": count,
            }
            for session, count in results
        ]

    @classmethod
    def open_sessions_by_verified_owners(cls):
        """Deep query #2: relationship filter with nested .has()."""
        return Session.query.filter(
            Session.status == "open",
            Session.studio_owner.has(User.profile.has(Profile.is_verified == True)),  # noqa: E712
        ).all()