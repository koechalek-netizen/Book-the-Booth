"""
A small decorator for routes that need a JSON body with specific keys
present, so every route isn't hand-rolling the same "is this field
missing" checks.
"""

from functools import wraps

from flask import request, jsonify


def validate_json(*required_fields):
    """
    Usage:
        @app.route("/sessions", methods=["POST"])
        @jwt_required()
        @validate_json("room_name", "hourly_rate", "date_available")
        def create_session():
            ...

    Returns 400 with the list of missing fields if the JSON body doesn't
    have all of them; otherwise calls the wrapped function normally.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True) or {}
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
            return fn(*args, **kwargs)

        return wrapper

    return decorator