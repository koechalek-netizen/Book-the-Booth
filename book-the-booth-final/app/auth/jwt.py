"""
Centralizes token creation so every login route builds the JWT the same
way. The token's identity is the user's id (as a string — newer
flask-jwt-extended versions require this); role/username ride along as
additional claims for @role_required and quick display without another
DB lookup.

Remember: a JWT is signed, not encrypted. Anyone can decode the payload.
Never put anything secret in additional_claims.
"""

from flask_jwt_extended import create_access_token


def issue_token(user):
    """
    TODO:
    return create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "username": user.username},
    )
    """
    pass
