from app.extensions import db


class SslRecord(db.Model):
    __tablename__ = "ssl_record"

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey("monitor.id"), nullable=False)
    success = db.Column(db.Boolean, nullable=False)
    authority = db.Column(db.String(128), nullable=False)
    expiry_date = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def __init__(self, monitor_id, success, authority, expiry_date):
        self.monitor_id = monitor_id
        self.success = success
        self.authority = authority
        self.expiry_date = expiry_date

    @staticmethod
    def create(monitor_id, success, authority, expiry_date):
        new_ssl_record = SslRecord(monitor_id, success, authority, expiry_date)
        try:
            db.session.add(new_ssl_record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating ssl record: " + str(e))
        return new_ssl_record

    def as_dict(self):
        return {
            "id": str(self.id),
            "monitor_id": str(self.monitor_id),
            "success": self.success,
            "authority": self.authority,
            "expiry_date": str(self.expiry_date),
            "created_at": str(self.created_at),
        }
