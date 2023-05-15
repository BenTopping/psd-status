from app.extensions import db


class Monitor(db.Model):
    __tablename__ = "monitor"

    id = db.Column(db.Integer, primary_key=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey("protocol.id"), nullable=False)
    http_records = db.relationship("HttpRecord", backref="monitor")
    ssl_records = db.relationship("SslRecord", backref="monitor")
    delay = db.Column(db.Integer, nullable=False)
    name = db.Column(
        db.String(128),
        nullable=False,
        unique=True,
    )
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
            raise e

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
        }

    def average_uptime_percentage(self):
        if len(self.http_records) > 0:
            success_records = len(
                list(
                    filter(
                        lambda http_record: http_record.success is True,
                        self.http_records,
                    )
                )
            )
            total_records = len(self.http_records)

            return str(round(100.0 * success_records / total_records, 2))
        else:
            return "0"
