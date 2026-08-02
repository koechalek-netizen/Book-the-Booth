from extensions import db


class Session(db.Model):
    """
    A bookable studio time slot. One studio owner (User) posts many
    Sessions -> one-to-many. Artists reserve Sessions via Booking, the
    many-to-many association object.
    """

    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    studio_owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    room_name = db.Column(db.String(100), nullable=False)
    genre_focus = db.Column(db.String(50))
    hourly_rate = db.Column(db.Numeric(8, 2), nullable=False)
    date_available = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="open")  # "open" | "closed"

    studio_owner = db.relationship("User", back_populates="sessions_owned")
    bookings = db.relationship(
        "Booking", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Session {self.room_name} ({self.status})>"
