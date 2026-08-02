from extensions import db, bcrypt


class User(db.Model):
    """
    One table for all three roles (artist / studio_owner / admin), told
    apart by `role`. Kept as a single table rather than subclasses so JWT
    claims and the @role_required decorator stay simple.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="artist")
    # role is one of: "artist", "studio_owner", "admin"
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # --- relationships ---
    # 1:1 -> Profile
    profile = db.relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    # 1:many -> Session (populated when role == "studio_owner")
    sessions_owned = db.relationship(
        "Session", back_populates="studio_owner", cascade="all, delete-orphan"
    )
    # many:many -> Session, via Booking (populated when role == "artist")
    bookings = db.relationship(
        "Booking", back_populates="artist", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
