from flask import Blueprint, jsonify
from app.models.http_record import HttpRecord
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl

bp = Blueprint("routes", __name__)


@bp.get("/")
def get_test():
    http_records = HttpRecord.query.all()
    http_dict_records = list(map(lambda x: x.as_dict(), http_records))

    return jsonify(http_dict_records) 
    # return jsonify(User.query.one().as_dict())
