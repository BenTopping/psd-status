from functools import wraps
from flask import jsonify, current_app, request
import jwt
from app.models.user import User


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        invalid_msg = {
            "message": "Invalid token. Authentication required",
            "authenticated": False,
        }
        expired_msg = {
            "message": "Expired token. Reauthentication required.",
            "authenticated": False,
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user = User.query.filter_by(username=data["sub"]).first()
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify(invalid_msg), 401

    return _verify
