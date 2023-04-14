from app.models.http_record import HttpRecord
from app.models.monitor import Monitor
from app.models.protocol import Protocol

def test_new_http_record():
    http_record = HttpRecord(1, 200.0, 201, "There was an error")

    assert http_record.monitor_id == 1
    assert http_record.response_time == 200.0
    assert http_record.status_code == 201
    assert http_record.errors == "There was an error"

def test_create_http_record(app):
    with app.app_context():
        protocol = Protocol.create("http")
        monitor = Monitor.create(protocol.id, 30, "Monitor1", 'www.test.com', True)
        HttpRecord.create(monitor.id, 200.0, 201, "There was an error")

        # Checks latest http_record created has same details as above
        db_http_record = HttpRecord.query.order_by(HttpRecord.id.desc()).first()
        assert db_http_record.monitor == monitor
        assert db_http_record.response_time == 200.0
        assert db_http_record.status_code == 201
        assert db_http_record.errors == "There was an error"
        assert db_http_record.created_at is not None

def test_http_record_as_dict():
    http_record = HttpRecord(1, 200.0, 201, "There was an error").as_dict()

    assert http_record["monitor_id"] == "1"
    assert http_record["response_time"] == "200.0"
    assert http_record["status_code"] == "201"
    assert http_record["errors"] == "There was an error"