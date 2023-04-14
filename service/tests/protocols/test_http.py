from app.protocols.http import get_http
from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.models.http_record import HttpRecord

import responses
import requests

def test_get_http_when_valid(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
    with app.app_context():
        mocked_responses.add(responses.GET, f"https://{monitor.target}", status=200)
        
        get_http(monitor)

        # Checks it creates a database record with the correct data
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor
        assert db_http_record.status_code == 200
        assert db_http_record.errors == ""

def test_get_http_when_http_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
    with app.app_context():
        mocked_responses.add(responses.GET, f"https://{monitor.target}", status=500)
        
        get_http(monitor)

        # Checks it creates a database record with the correct data
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor
        assert db_http_record.status_code == 500
        assert db_http_record.response_time > 0
        assert db_http_record.errors == "HTTP Error: 500 Server Error: Internal Server Error for url: https://www.test.com/"

def test_get_http_when_connection_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
    with app.app_context():
        mocked_responses.add(responses.GET, f"https://{monitor.target}", body=requests.ConnectionError())
        
        get_http(monitor)

        # Checks it creates a database record with the correct data
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor
        assert db_http_record.status_code == None
        assert db_http_record.response_time == None
        assert db_http_record.errors == "Connection Error: "

def test_get_http_when_timeout_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
    with app.app_context():
        mocked_responses.add(responses.GET, f"https://{monitor.target}", body=requests.Timeout())
        
        get_http(monitor)

        # Checks it creates a database record with the correct data
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor
        assert db_http_record.status_code == None
        assert db_http_record.response_time == None
        assert db_http_record.errors == "Timeout Error: "

def test_get_http_when_request_exception_error(app, mocked_responses):
    protocol = Protocol.create("http")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
    with app.app_context():
        mocked_responses.add(responses.GET, f"https://{monitor.target}", body=requests.RequestException())
        
        get_http(monitor)

        # Checks it creates a database record with the correct data
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor
        assert db_http_record.status_code == None
        assert db_http_record.response_time == None
        assert db_http_record.errors == "Request exception: "


