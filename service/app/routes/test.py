from flask import Blueprint, jsonify
from app.models.http_record import HttpRecord
from app.routes import token_required

bp = Blueprint("routes", __name__)


@bp.get("/")
@token_required
def get_test(current_user):
    http_records = HttpRecord.query.all()
    http_dict_records = list(map(lambda x: x.as_dict(), http_records))

    return jsonify(http_dict_records)
    # return jsonify(User.query.one().as_dict())
