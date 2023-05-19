from flask import Blueprint, jsonify, request
from app.models.monitor import Monitor
from app.routes.common.monitors import handle_monitor
from app.routes import token_required

bp = Blueprint("monitor_routes", __name__)


@bp.get("/monitors")
def monitors():
    monitors = Monitor.query.all()
    monitors_dict_records = list(map(lambda monitor: monitor.as_dict(), monitors))

    return jsonify(monitors_dict_records)


@bp.post("/monitor")
@token_required
def create_monitor(current_user):
    data = request.get_json()
    result = handle_monitor(data)

    return jsonify(result["data"]), result["status_code"]
