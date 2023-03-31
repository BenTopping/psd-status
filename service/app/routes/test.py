from flask import Blueprint, jsonify
from app.models.user import User

bp = Blueprint("routes", __name__)


@bp.get("/")
def get_test():
    return jsonify(User.query.one().as_dict())
