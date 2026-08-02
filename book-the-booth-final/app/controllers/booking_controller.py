from extensions import db
from app.models.booking import Booking
from app.models.session import Session
from app.models.user import User
from app.utils.validators import parse_date


class BookingController:
    """Reserving Sessions as Bookings, plus the revenue aggregation query."""

    @classmethod
    def get_bookings_for_artist(cls, artist_id, page=1, per_page=10):
        query = Booking.query.filter_by(artist_id=int(artist_id)).order_by(Booking.session_date.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def get_bookings_for_session(cls, session_id):
        return Booking.query.filter_by(session_id=session_id).all()

    @classmethod
    def create_booking(cls, artist_id, data):
        session = Session.query.get(data["session_id"])
        if not session:
            return None, "Session not found"
        if session.status != "open":
            return None, "This session is not open for booking"

        booking = Booking(
            artist_id=int(artist_id),
            session_id=session.id,
            rate_agreed=data["rate_agreed"],
            session_date=parse_date(data["session_date"]),
            hours_booked=data["hours_booked"],
            status="pending",
        )
        db.session.add(booking)
        db.session.commit()
        return booking, None

    @classmethod
    def update_booking_status(cls, booking_id, status):
        booking = Booking.query.get(booking_id)
        if not booking:
            return None
        booking.status = status
        db.session.commit()
        return booking

    @classmethod
    def revenue_by_studio_owner(cls):
        """Deep query #3: join across 3 tables + aggregation."""
        results = (
            db.session.query(
                User.username,
                db.func.sum(Booking.rate_agreed * Booking.hours_booked).label("revenue"),
            )
            .join(Session, Session.studio_owner_id == User.id)
            .join(Booking, Booking.session_id == Session.id)
            .group_by(User.id)
            .all()
        )
        return [{"studio_owner": username, "revenue": float(revenue)} for username, revenue in results]