"""
Small helpers so every list endpoint returns pagination metadata in the
same shape, and every error response looks the same.
"""


def paginated_response(pagination, schema):
    """
    Takes a Flask-SQLAlchemy Pagination object (from Model.query.paginate(...))
    and a many=True marshmallow schema, and returns the dict your route
    should jsonify().

    Usage:
        pagination = Session.query.filter_by(status="open") \\
            .paginate(page=page, per_page=per_page, error_out=False)
        return jsonify(paginated_response(pagination, sessions_schema))
    """
    return {
        "items": schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
    }


def error_response(message, status_code=400):
    """Usage: return error_response("Session is fully booked", 409)"""
    return {"error": message}, status_code
