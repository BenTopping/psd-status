from flask import Blueprint, jsonify, current_app, request
import jwt
import datetime
from app.models.user import User

bp = Blueprint("auth_routes", __name__)


@bp.post("/login")
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({"message": "Invalid credentials", "authenticated": False}), 401

    token = jwt.encode(
        {
            "sub": user.username,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({"token": token})
