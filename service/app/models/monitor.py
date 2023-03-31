from app.models import db


class Monitor(db.Model):
    __tablename__ = "monitor"

    id = db.Column(db.Integer, primary_key=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocol.id'), nullable=False)
    protocol = db.relationship("Protocol", backref=db.backref("protocol"))
    delay = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128))
    target = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), server_onupdate=db.func.now())

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

    def as_dict(self):
      return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
