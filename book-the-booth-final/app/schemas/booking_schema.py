from extensions import ma
from app.models.booking import Booking


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
