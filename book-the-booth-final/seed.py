"""
Populates the database with realistic demo data using Faker.
Run after migrations: `python seed.py`

Must exercise every relationship — real many-to-many Bookings, not an
empty join table.
"""

from faker import Faker

from app import create_app
from extensions import db
from app.models import User, Profile, Session, Booking

fake = Faker()


def seed():
    app = create_app()
    with app.app_context():
        # TODO:
        # 1. Optional hard reset for local dev: db.drop_all(); db.create_all()
        #    (prefer `flask db upgrade` for schema — this script just fills data)
        #
        # 2. Create an admin user + profile
        #
        # 3. Create N studio_owner users, each with a Profile,
        #    and 2-4 Sessions each (1:many)
        #
        # 4. Create M artist users, each with a Profile
        #
        # 5. Create Bookings linking artists to sessions (many:many),
        #    with realistic rate_agreed / session_date / hours_booked / status
        #
        # 6. db.session.commit()

        print("Seed complete.")


if __name__ == "__main__":
    seed()
