import pytest
import responses

from app import create_app, db
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SCHEDULER_RUN = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/psd_status_test"


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
