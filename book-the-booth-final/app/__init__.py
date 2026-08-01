from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import Config
from extensions import db, ma, jwt, migrate, bcrypt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Models must be imported somewhere Flask-Migrate can see them.
    from app.models import User, Profile, Session, Booking  # noqa: F401

    from app.controllers import (
        AuthController,
        UserController,
        ProfileController,
        SessionController,
        BookingController,
        AdminController,
    )
    from app.schemas import (
        user_schema,
        profile_schema,
        session_schema,
        sessions_schema,
        booking_schema,
        bookings_schema,
    )
    from app.auth import issue_token, role_required
    from app.utils import validate_json, paginated_response, error_response

    @app.route("/")
    def index():
        return jsonify({"message": "Book the Booth API"})

    # ---------- Auth ----------

    @app.route("/register", methods=["POST"])
    @validate_json("username", "email", "password")
    def register():
        """TODO: user = AuthController.register_user(request.json); return user_schema.dump(user), 201"""
        pass

    @app.route("/login", methods=["POST"])
    @validate_json("username", "password")
    def login():
        """
        TODO:
        data = request.json
        user = AuthController.authenticate_user(data["username"], data["password"])
        if not user:
            return error_response("Invalid username or password", 401)
        return jsonify({"token": issue_token(user)}), 200
        """
        pass

    # ---------- Profile ----------

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def get_my_profile():
        """TODO: ProfileController.get_profile(get_jwt_identity())"""
        pass

    @app.route("/profile", methods=["PUT"])
    @jwt_required()
    def update_my_profile():
        """TODO: ProfileController.update_profile(get_jwt_identity(), request.json)"""
        pass

    # ---------- Sessions ----------

    @app.route("/sessions", methods=["GET"])
    @jwt_required()
    def get_sessions():
        """
        TODO:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        genre = request.args.get("genre")
        pagination = SessionController.get_all_sessions(page, per_page, genre)
        return jsonify(paginated_response(pagination, sessions_schema))
        """
        pass

    @app.route("/sessions/<int:session_id>", methods=["GET"])
    @jwt_required()
    def get_session(session_id):
        """TODO: SessionController.get_session_by_id(session_id)"""
        pass

    @app.route("/sessions", methods=["POST"])
    @jwt_required()
    @role_required("studio_owner")
    @validate_json("room_name", "hourly_rate", "date_available")
    def create_session():
        """TODO: SessionController.create_session(get_jwt_identity(), request.json)"""
        pass

    @app.route("/sessions/<int:session_id>", methods=["PUT"])
    @jwt_required()
    @role_required("studio_owner")
    def update_session(session_id):
        """TODO: confirm this owner owns the session, then SessionController.update_session(...)"""
        pass

    @app.route("/sessions/<int:session_id>", methods=["DELETE"])
    @jwt_required()
    def delete_session(session_id):
        """TODO: allow studio_owner (their own session) or admin"""
        pass

    @app.route("/sessions/stats/booking-counts", methods=["GET"])
    @jwt_required()
    def sessions_booking_counts():
        """TODO: SessionController.sessions_with_booking_counts() — deep query #1"""
        pass

    # ---------- Bookings ----------

    @app.route("/bookings", methods=["GET"])
    @jwt_required()
    def get_my_bookings():
        """
        TODO:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        pagination = BookingController.get_bookings_for_artist(get_jwt_identity(), page, per_page)
        return jsonify(paginated_response(pagination, bookings_schema))
        """
        pass

    @app.route("/bookings", methods=["POST"])
    @jwt_required()
    @role_required("artist")
    @validate_json("session_id", "rate_agreed", "session_date", "hours_booked")
    def create_booking():
        """TODO: BookingController.create_booking(get_jwt_identity(), request.json)"""
        pass

    @app.route("/bookings/<int:booking_id>", methods=["PATCH"])
    @jwt_required()
    def update_booking(booking_id):
        """TODO: confirm/cancel — BookingController.update_booking_status(...)"""
        pass

    @app.route("/stats/revenue-by-owner", methods=["GET"])
    @jwt_required()
    @role_required("admin")
    def revenue_by_owner():
        """TODO: BookingController.revenue_by_studio_owner() — deep query #2, admin only"""
        pass

    # ---------- Admin ----------

    @app.route("/admin/users", methods=["GET"])
    @jwt_required()
    @role_required("admin")
    def admin_list_users():
        """TODO: AdminController.get_all_users(...)"""
        pass

    @app.route("/admin/profiles/<int:user_id>/verify", methods=["PATCH"])
    @jwt_required()
    @role_required("admin")
    def admin_verify_profile(user_id):
        """TODO: AdminController.verify_studio_owner(user_id)"""
        pass

    @app.route("/admin/sessions/<int:session_id>", methods=["DELETE"])
    @jwt_required()
    @role_required("admin")
    def admin_remove_session(session_id):
        """TODO: AdminController.remove_session(session_id)"""
        pass

    @app.route("/admin/bookings/<int:booking_id>", methods=["DELETE"])
    @jwt_required()
    @role_required("admin")
    def admin_remove_booking(booking_id):
        """TODO: AdminController.remove_booking(booking_id)"""
        pass

    return app
