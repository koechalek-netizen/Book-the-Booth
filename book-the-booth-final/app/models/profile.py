from extensions import db


class Profile(db.Model):
    """
    One-to-one with User. Every account gets exactly one profile for
    contact details and (for studio owners) verification state.
    """

    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    phone = db.Column(db.String(20))
    location = db.Column(db.String(120))
    is_verified = db.Column(db.Boolean, default=False)
    # admin flips this to True once a studio owner account is confirmed legitimate

    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile user_id={self.user_id}>"
