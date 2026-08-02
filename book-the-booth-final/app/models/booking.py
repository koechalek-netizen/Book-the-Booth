from extensions import db


class Booking(db.Model):
    """
    The many-to-many join between Artist (User) and Session — not a thin
    join table. It carries the actual deal terms agreed at booking time:
    rate_agreed, session_date, hours_booked, status.
    """

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)

    rate_agreed = db.Column(db.Numeric(8, 2), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    hours_booked = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")
    # "pending" | "confirmed" | "cancelled"

    artist = db.relationship("User", back_populates="bookings")
    session = db.relationship("Session", back_populates="bookings")

    def __repr__(self):
        return f"<Booking artist_id={self.artist_id} session_id={self.session_id}>"
