from flask import Blueprint, jsonify, request
from app.models.http_record import HttpRecord
from app.models.monitor import Monitor
from sqlalchemy.orm import joinedload

bp = Blueprint("http_record_routes", __name__)


@bp.get("/http_records")
def http_records():
    args = request.args
    # The monitor ids to get the http records from
    monitor_ids = args.get("monitor_ids")
    # Maximum amount of http records to get defaults to unlimited
    limit = args.get("limit")

    if monitor_ids is None:
        return jsonify({"message": "monitor_ids required"}), 400

    monitor_ids = monitor_ids.split(",")
    http_records = []
    for id in monitor_ids:
        monitor = (
            Monitor.query.join(HttpRecord)
            .filter(
                Monitor.id == id,
            )
            .options(joinedload(Monitor.http_records))
            .first()
        )
        if monitor is None:
            return jsonify({"message": f"Unable to find monitor with id {id}"}), 400
        if limit is not None:
            # Gets last 'limit' number of records
            http_records.extend(
                list(map(lambda x: x.as_dict(), monitor.http_records))[-int(limit):]
            )
        else:
            http_records.extend(list(map(lambda x: x.as_dict(), monitor.http_records)))

    return jsonify(http_records)
