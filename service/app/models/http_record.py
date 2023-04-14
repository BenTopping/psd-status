from app.extensions import db

class HttpRecord(db.Model):
    __tablename__ = "http_record"

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitor.id'), nullable=False)
    response_time = db.Column(db.Float)
    status_code = db.Column(db.Integer)
    errors = db.Column(db.String(128))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, monitor_id, response_time, status_code, errors):
        self.monitor_id = monitor_id
        self.response_time = response_time
        self.status_code = status_code
        self.errors = errors

    @staticmethod
    def create(monitor_id, response_time, status_code, errors):
        new_http_record = HttpRecord(monitor_id, response_time, status_code, errors)
        try:
            db.session.add(new_http_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating http record: " + str(e))
        return new_http_record

    def as_dict(self):
      return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

