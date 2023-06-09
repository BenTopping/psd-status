from app.models.monitor import Monitor
from app.extensions import db
from app.jobs.setup import handle_http_job
from pymysql import MySQLError


def handle_monitor(monitor):
    try:
        monitor = format_monitor(monitor)
    except Exception as e:
        print(e)
        return {"data": {"message": "Invalid data"}, "status_code": 400}

    if "id" not in monitor:
        try:
            # Create monitor in db
            monitor = Monitor.create(**monitor)
            # Create scheduler job
            handle_http_job(monitor)
            return {"data": monitor.as_dict(), "status_code": 200}
        except MySQLError as e:
            return {"data": {"message": e.args[0]}, "status_code": 400}
        except Exception as e:
            return {"data": {"message": str(e)}, "status_code": 400}
    else:
        try:
            # Check monitor exists
            db_monitor = Monitor.query.filter_by(id=monitor["id"]).first()
            if db_monitor is not None:
                # Update monitor in db
                Monitor.query.filter_by(id=monitor["id"]).update(monitor)
                db.session.commit()
            # Update scheduler job
            handle_http_job(db_monitor)
            return {"data": db_monitor.as_dict(), "status_code": 200}
        except MySQLError as e:
            return {"data": {"message": e.args[0]}, "status_code": 400}
        except Exception as e:
            return {"data": {"message": str(e)}, "status_code": 400}


def format_monitor(monitor):
    # TODO add validation here so we don't rely on database validation
    try:
        formatted_monitor = {
            "protocol_id": monitor["protocol_id"],
            "name": monitor["name"],
            "active": monitor["active"],
            "delay": monitor["delay"],
            "target": monitor["target"],
        }

        if "id" in monitor:
            formatted_monitor["id"] = monitor["id"]

        return formatted_monitor

    except Exception as e:
        raise Exception(e)
