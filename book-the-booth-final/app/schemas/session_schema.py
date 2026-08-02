from extensions import ma
from app.models.session import Session


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        load_instance = True
        include_fk = True


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
