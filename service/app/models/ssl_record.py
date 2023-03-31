from app.models import db


class SslRecord(db.Model):
    __tablename__ = "ssl_record"

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitor.id'), nullable=False)
    monitor = db.relationship("Monitor", backref="ssl_record")
    success = db.Column(db.Boolean, nullable=False)
    expiry_date = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, monitor_id, success, expiry_date):
        self.monitor_id = monitor_id
        self.success = success
        self.expiry_date = expiry_date

    @staticmethod
    def create(monitor_id, success, expiry_date): 
        new_monitor = SslRecord(monitor_id, success, expiry_date)
        try:
            db.session.add(new_monitor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating ssl record: " + str(e))

    def as_dict(self):
      return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


