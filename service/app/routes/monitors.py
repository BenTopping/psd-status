from flask import Blueprint, jsonify
from app.models.monitor import Monitor
from app.models.http_record import HttpRecord

bp = Blueprint("monitor_routes", __name__)

@bp.get("/monitors")
def monitors():
    monitors = Monitor.query.all()
    monitors_dict_records = list(map(lambda monitor: monitor_dict(monitor), monitors))

    return jsonify(monitors_dict_records)


def monitor_dict(monitor: Monitor):
    monitor_dict = monitor.as_dict()
    monitor_dict['http_records'] = list(map(lambda x: x.as_dict(), monitor.http_records))[-10:]
    monitor_dict['average_uptime'] = monitor.average_uptime_percentage()
    monitor_dict['current_state'] = monitor.current_state()
    return monitor_dict

