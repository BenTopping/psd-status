from app.extensions import db
from app.models.http_record import HttpRecord


class Monitor(db.Model):
    __tablename__ = "monitor"

    id = db.Column(db.Integer, primary_key=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey("protocol.id"), nullable=False)
    http_records = db.relationship("HttpRecord", backref="monitor")
    ssl_records = db.relationship("SslRecord", backref="monitor")
    delay = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128))
    target = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, protocol_id, delay, name, target, active):
        self.protocol_id = protocol_id
        self.delay = delay
        self.name = name
        self.target = target
        self.active = active

    @staticmethod
    def create(protocol_id, delay, name, target, active):
        new_monitor = Monitor(protocol_id, delay, name, target, active)
        try:
            db.session.add(new_monitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating monitor: " + str(e))
        return new_monitor

    def as_dict(self):
        return {
            "id": str(self.id),
            "protocol_id": str(self.protocol_id),
            "delay": str(self.delay),
            "name": str(self.name),
            "target": str(self.target),
            "active": self.active,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "average_uptime": self.average_uptime_percentage(),
            "current_state": self.current_state()
        }
    
    def average_uptime_percentage(self):
        if len(self.http_records) > 0:
            success_records = len(list(filter(lambda http_record: http_record.success == True, self.http_records)))
            total_records = len(self.http_records)

            return str(
                round(100.0 * success_records / total_records, 2)
            )
        else:
            return '0'
    
    def current_state(self):
        if len(self.http_records) > 0:
            last_records = list(map(lambda x: x.as_dict(), self.http_records))[-10:]
            # Check if most recent http_record is successful
            if last_records[0]['success'] == False:
                return 'red'
            # Check if any of the last 10 records were unsuccesful
            elif True in (record['success'] == False for record in last_records):
                return 'yellow'
            else:
            # Return green if all is good
                return 'green'
        else:
            return 'red'
