from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method="sha256")

    @staticmethod
    def create(username, password):
        new_user = User(username, password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("! Error creating user: " + str(e))
        return new_user

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def as_dict(self):
        return dict(id=self.id, username=self.username)
