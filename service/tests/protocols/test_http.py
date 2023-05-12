from app.protocols.http import get_http
from app.models.monitor import Monitor
from app.models.protocol import Protocol

import responses
import requests


def test_get_http_when_valid(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        mocked_responses.add(
            responses.GET, f"{monitor.protocol.name}://{monitor.target}", status=200
        )

        http_record = get_http(monitor)

        assert http_record.monitor
        assert http_record.status_code == 200
        assert http_record.errors == ""


def test_get_http_when_invalid_monitor(app, mocked_responses):
    protocol = Protocol.create("random")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        response = get_http(monitor)

        assert response["errors"] == "Invalid protocol"


def test_get_http_when_http_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        mocked_responses.add(
            responses.GET, f"{monitor.protocol.name}://{monitor.target}", status=500
        )

        http_record = get_http(monitor)

        assert http_record.monitor
        assert http_record.status_code == 500
        assert http_record.response_time > 0
        assert http_record.errors == "HTTP Error"


def test_get_http_when_connection_error(app, mocked_responses):
    protocol = Protocol.create("https")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        mocked_responses.add(
            responses.GET,
            f"{monitor.protocol.name}://{monitor.target}",
            body=requests.ConnectionError(),
        )

        http_record = get_http(monitor)

        assert http_record.monitor
        assert http_record.status_code is None
        assert http_record.response_time is None
        assert http_record.errors == "Connection Error"


def test_get_http_when_timeout_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        mocked_responses.add(
            responses.GET,
            f"{monitor.protocol.name}://{monitor.target}",
            body=requests.Timeout(),
        )

        http_record = get_http(monitor)

        assert http_record.monitor
        assert http_record.status_code is None
        assert http_record.response_time is None
        assert http_record.errors == "Timeout Error"


def test_get_http_when_request_exception_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        mocked_responses.add(
            responses.GET,
            f"{monitor.protocol.name}://{monitor.target}",
            body=requests.RequestException(),
        )

        http_record = get_http(monitor)

        assert http_record.monitor
        assert http_record.status_code is None
        assert http_record.response_time is None
        assert http_record.errors == "Request exception"
