from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
    cors.init_app(app, origins=app.config["CORS_ORIGIN"])

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            return response
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
        users_schema,
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
        data = request.get_json()
        existing = UserController.get_user_by_username(data["username"])
        if existing:
            return error_response("Username already taken", 409)
        user = AuthController.register_user(data)
        return jsonify(user_schema.dump(user)), 201

    @app.route("/login", methods=["POST"])
    @validate_json("username", "password")
    def login():
        data = request.get_json()
        user = AuthController.authenticate_user(data["username"], data["password"])
        if not user:
            return error_response("Invalid username or password", 401)
        return jsonify({"token": issue_token(user), "user": user_schema.dump(user)}), 200

    # ---------- Profile ----------

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def get_my_profile():
        profile = ProfileController.get_profile(get_jwt_identity())
        if not profile:
            return error_response("Profile not found", 404)
        return jsonify(profile_schema.dump(profile)), 200

    @app.route("/profile", methods=["PUT"])
    @jwt_required()
    def update_my_profile():
        profile = ProfileController.update_profile(get_jwt_identity(), request.get_json() or {})
        if not profile:
            return error_response("Profile not found", 404)
        return jsonify(profile_schema.dump(profile)), 200

    # ---------- Sessions ----------

    @app.route("/sessions", methods=["GET"])
    @jwt_required()
    def get_sessions():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        genre = request.args.get("genre")
        pagination = SessionController.get_all_sessions(page, per_page, genre)
        return jsonify(paginated_response(pagination, sessions_schema)), 200

    @app.route("/sessions/<int:session_id>", methods=["GET"])
    @jwt_required()
    def get_session(session_id):
        session = SessionController.get_session_by_id(session_id)
        if not session:
            return error_response("Session not found", 404)
        return jsonify(session_schema.dump(session)), 200

    @app.route("/sessions", methods=["POST"])
    @jwt_required()
    @role_required("studio_owner")
    @validate_json("room_name", "hourly_rate", "date_available")
    def create_session():
        try:
            session = SessionController.create_session(get_jwt_identity(), request.get_json())
        except (ValueError, KeyError) as e:
            return error_response(f"Invalid session data: {e}", 400)
        return jsonify(session_schema.dump(session)), 201

    @app.route("/sessions/<int:session_id>", methods=["PUT"])
    @jwt_required()
    @role_required("studio_owner")
    def update_session(session_id):
        session = SessionController.get_session_by_id(session_id)
        if not session:
            return error_response("Session not found", 404)
        if str(session.studio_owner_id) != get_jwt_identity():
            return error_response("You don't own this session", 403)
        session = SessionController.update_session(session_id, request.get_json() or {})
        return jsonify(session_schema.dump(session)), 200

    @app.route("/sessions/<int:session_id>", methods=["DELETE"])
    @jwt_required()
    def delete_session(session_id):
        session = SessionController.get_session_by_id(session_id)
        if not session:
            return error_response("Session not found", 404)

        claims = get_jwt()
        is_owner = str(session.studio_owner_id) == get_jwt_identity()
        is_admin = claims.get("role") == "admin"
        if not (is_owner or is_admin):
            return error_response("Not allowed to delete this session", 403)

        SessionController.delete_session(session_id)
        return "", 204

    @app.route("/sessions/<int:session_id>/bookings", methods=["GET", "OPTIONS"])
    def get_session_bookings(session_id):
        if request.method == "OPTIONS":
            return "", 200

        @jwt_required()
        def _handle_get():
            session = SessionController.get_session_by_id(session_id)
            if not session:
                return error_response("Session not found", 404)

            claims = get_jwt()
            is_owner = str(session.studio_owner_id) == get_jwt_identity()
            is_admin = claims.get("role") == "admin"
            if not (is_owner or is_admin):
                return error_response("Not allowed to view these bookings", 403)

            bookings = BookingController.get_bookings_for_session(session_id)
            return jsonify(bookings_schema.dump(bookings)), 200

        return _handle_get()
    # ---------- Bookings ----------

    @app.route("/bookings", methods=["GET"])
    @jwt_required()
    def get_my_bookings():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        pagination = BookingController.get_bookings_for_artist(get_jwt_identity(), page, per_page)
        return jsonify(paginated_response(pagination, bookings_schema)), 200

    @app.route("/bookings", methods=["POST"])
    @jwt_required()
    @role_required("artist")
    @validate_json("session_id", "rate_agreed", "session_date", "hours_booked")
    def create_booking():
        try:
            booking, err = BookingController.create_booking(get_jwt_identity(), request.get_json())
        except (ValueError, KeyError) as e:
            return error_response(f"Invalid booking data: {e}", 400)
        if err:
            return error_response(err, 409)
        return jsonify(booking_schema.dump(booking)), 201

    @app.route("/bookings/<int:booking_id>", methods=["PATCH"])
    @jwt_required()
    @validate_json("status")
    def update_booking(booking_id):
        status = request.get_json()["status"]
        if status not in ("confirmed", "cancelled"):
            return error_response("status must be 'confirmed' or 'cancelled'", 400)
        booking = BookingController.update_booking_status(booking_id, status)
        if not booking:
            return error_response("Booking not found", 404)
        return jsonify(booking_schema.dump(booking)), 200

    @app.route("/stats/revenue-by-owner", methods=["GET"])
    @jwt_required()
    @role_required("admin")
    def revenue_by_owner():
        return jsonify(BookingController.revenue_by_studio_owner()), 200

    # ---------- Admin ----------

    @app.route("/admin/users", methods=["GET"])
    @jwt_required()
    @role_required("admin")
    def admin_list_users():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        pagination = AdminController.get_all_users(page, per_page)
        return jsonify(paginated_response(pagination, users_schema)), 200

    @app.route("/admin/profiles/<int:user_id>/verify", methods=["PATCH"])
    @jwt_required()
    @role_required("admin")
    def admin_verify_profile(user_id):
        profile = AdminController.verify_studio_owner(user_id)
        if not profile:
            return error_response("Profile not found", 404)
        return jsonify(profile_schema.dump(profile)), 200

    @app.route("/admin/sessions/<int:session_id>", methods=["DELETE"])
    @jwt_required()
    @role_required("admin")
    def admin_remove_session(session_id):
        removed = AdminController.remove_session(session_id)
        if not removed:
            return error_response("Session not found", 404)
        return "", 204

    @app.route("/admin/bookings/<int:booking_id>", methods=["DELETE"])
    @jwt_required()
    @role_required("admin")
    def admin_remove_booking(booking_id):
        removed = AdminController.remove_booking(booking_id)
        if not removed:
            return error_response("Booking not found", 404)
        return "", 204

    return app