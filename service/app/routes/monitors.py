from flask import Blueprint, jsonify, request
from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.routes.common.monitors import handle_monitor
import json
from app.routes import token_required

bp = Blueprint("monitor_routes", __name__)

@bp.get("/monitors")
def monitors():
    monitors = Monitor.query.all()
    monitors_dict_records = list(map(lambda monitor: monitor_dict(monitor), monitors))

    return jsonify(monitors_dict_records)

@bp.post("/monitor")
# @token_required
def create_monitor():
    data = request.get_json()
    result = handle_monitor(data)

    return jsonify(result[0]), result[1]

@bp.get("/protocols")
def protocols():
    protocols = Protocol.query.all()
    protocols_dict_records = list(map(lambda protocol: protocol.as_dict(), protocols))

    return jsonify(protocols_dict_records)

def monitor_dict(monitor: Monitor):
    monitor_dict = monitor.as_dict()
    monitor_dict['http_records'] = list(map(lambda x: x.as_dict(), monitor.http_records))[-10:]
    if len(monitor.ssl_records) > 0:
        monitor_dict['ssl_expiry_date'] = monitor.ssl_records[-1].expiry_date
    return monitor_dict

