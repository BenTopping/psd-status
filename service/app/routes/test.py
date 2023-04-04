from flask import Blueprint, jsonify
from app.models.monitor import Monitor
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl

bp = Blueprint("routes", __name__)


@bp.get("/")
def get_test():
    monitor = Monitor.query.filter(Monitor.name == "Google").first()
    ssl_record = get_ssl(monitor)
    return jsonify(ssl_record.as_dict()) 
    # return jsonify(User.query.one().as_dict())
