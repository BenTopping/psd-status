import pytest
import responses
import jwt
import datetime

from app import create_app, db
from app.config import Config
from app.models.user import User


class TestConfig(Config):
    TESTING = True
    SCHEDULER_RUN = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/psd_status_test"
    SECRET_KEY = "testkey"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def mocked_responses():
    """Easily mock responses from HTTP calls.
    https://github.com/getsentry/responses#responses-as-a-pytest-fixture"""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def active_jwt(app):
    with app.app_context():
        user = User.create("mock-user", "mock-user")
        return jwt.encode(
            {
                "sub": user.username,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
