"""
Shared extension instances — created here WITHOUT an app, bound to the
app later in app/__init__.py via `.init_app(app)`. Keeps models free to
import `db` without ever importing the app factory (avoids circular imports).
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
cors = CORS()
