from flask import Blueprint, jsonify, request
from app.models.monitor import Monitor
from app.routes.common.monitors import handle_monitor
from app.routes import token_required

bp = Blueprint("monitor_routes", __name__)


@bp.get("/monitors")
def monitors():
    monitors = Monitor.query.all()
    monitors_dict_records = list(map(lambda monitor: monitor_dict(monitor), monitors))

    return jsonify(monitors_dict_records)


@bp.post("/monitor")
@token_required
def create_monitor(current_user):
    data = request.get_json()
    result = handle_monitor(data)

    return jsonify(result["data"]), result["status_code"]


def monitor_dict(monitor: Monitor):
    monitor_dict = monitor.as_dict()
    monitor_dict["http_records"] = list(
        map(lambda x: x.as_dict(), monitor.http_records)
    )[-10:]
    if len(monitor.ssl_records) > 0:
        monitor_dict["ssl_expiry_date"] = monitor.ssl_records[-1].expiry_date
    return monitor_dict
