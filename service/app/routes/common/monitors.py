from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.extensions import db

def handle_monitor(monitor):
    try:
        monitor = format_monitor(monitor)
    except Exception as e:
        print(e)
        return { "data" : {"message": "Invalid data"}, "status_code": 400}

    if 'id' not in monitor:
        try:
            monitor = Monitor.create(**monitor)
            return { "data": monitor.as_dict(), "status_code": 200 }
        except Exception as e:
            print(e)
            return { "data": {"message": "Invalid data"}, "status_code": 400}
    else:
        try:
            db_monitor = Monitor.query.filter_by(id=monitor['id']).first()
            if db_monitor is not None:
                Monitor.query.filter_by(id=monitor['id']).update(monitor)
                db.session.commit()
            return { "data": db_monitor.as_dict(), "status_code": 200 }
        except Exception as e:
            print(e)
            return { "data" : {"message": "Invalid data"}, "status_code": 400}

def format_monitor(monitor):
    try:
        formatted_monitor = {
            'protocol_id': monitor['protocol_id'],
            'name': monitor['name'],
            'active': monitor['active'],
            'delay': monitor['delay'],
            'target': monitor['target']
        }

        if 'id' in monitor:
            formatted_monitor['id'] = monitor['id']

        return formatted_monitor

    except Exception as e:
        raise Exception(e)
