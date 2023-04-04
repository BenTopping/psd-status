from app.models import db


class HttpRecord(db.Model):
    __tablename__ = "http_record"

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitor.id'), nullable=False)
    response_time = db.Column(db.Integer, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    errors = db.Column(db.String(128))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, monitor_id, response_time, status_code, errors):
        self.monitor_id = monitor_id
        self.response_time = response_time
        self.status_code = status_code
        self.errors = errors

    @staticmethod
    def create(monitor_id, response_time, status_code, errors): 
        new_monitor = HttpRecord(monitor_id, response_time, status_code, errors)
        try:
            db.session.add(new_monitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating http record: " + str(e))

    def as_dict(self):
      return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

