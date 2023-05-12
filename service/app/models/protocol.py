from app.extensions import db


class Protocol(db.Model):
    __tablename__ = "protocol"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    monitors = db.relationship("Monitor", backref="protocol")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(name):
        new_protocol = Protocol(name)
        try:
            db.session.add(new_protocol)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating protocol: " + str(e))
        return new_protocol

    def as_dict(self):
        return {"id": self.id, "name": self.name}
