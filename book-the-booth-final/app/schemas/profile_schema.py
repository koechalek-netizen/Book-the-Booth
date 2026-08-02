from extensions import ma
from app.models.profile import Profile


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        include_fk = True


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
