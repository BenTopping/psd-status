from flask import Blueprint, jsonify, request
from app.models.monitor import Monitor
from app.routes.common.monitors import handle_monitor
from app.routes import token_required

bp = Blueprint("monitor_routes", __name__)


@bp.get("/monitors")
def monitors():
    args = request.args
    # The monitor ids to get the http records from
    monitor_ids = args.get("ids")
    # Active filter (true/false)
    active = args.get("active", type=bool)
    monitors = []
    if monitor_ids is not None:
        monitor_ids = monitor_ids.split(",")
        for id in monitor_ids:
            monitor = Monitor.query.filter(
                Monitor.id == id,
            ).first()

            if monitor is None:
                return jsonify({"message": f"Unable to find monitor with id {id}"}), 400

            if active is not None and monitor.active != active:
                return (
                    jsonify(
                        {
                            "message": f"Unable to find monitor with id {id} and active state: {active}"
                        }
                    ),
                    400,
                )

            monitors.append(monitor)
    else:
        # If no ids are specified default to returning all
        if active is not None:
            print(active)
            monitors = Monitor.query.filter(Monitor.active == active).all()
        else:
            monitors = Monitor.query.all()

    monitors_dict_records = list(map(lambda monitor: monitor.as_dict(), monitors))

    return jsonify(monitors_dict_records)


@bp.post("/monitor")
@token_required
def create_monitor(current_user):
    data = request.get_json()
    result = handle_monitor(data)

    return jsonify(result["data"]), result["status_code"]
