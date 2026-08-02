"""
@jwt_required() only proves *who you are*. This answers *what you're
allowed to do* — an artist hitting an admin-only route should get a 403,
not a 401.

Usage (decorator order matters — jwt_required goes closest to the route):

    @app.route("/admin/sessions/<int:session_id>", methods=["DELETE"])
    @jwt_required()
    @role_required("admin")
    def admin_delete_session(session_id):
        ...
"""

from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator