from app.extensions import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create(username, name): 
        new_user = User(username, name)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating user: " + str(e))

    def as_dict(self):
      return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
