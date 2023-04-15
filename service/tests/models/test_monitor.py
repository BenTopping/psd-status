from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.models.http_record import HttpRecord
from app.models.ssl_record import SslRecord
import datetime


def test_new_monitor():
    # It initialises the object with the correct values
    monitor = Monitor(1, 30, "Monitor1", "www.test.com", True)

    assert monitor.protocol_id == 1
    assert monitor.delay == 30
    assert monitor.name == "Monitor1"
    assert monitor.target == "www.test.com"
    assert monitor.active is True


def test_create_monitor(app):
    # It creates the object with the correct values in the database
    with app.app_context():
        protocol = Protocol.create("Protocol1")
        Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)

        # Checks latest monitor created has same details as above
        db_monitor = Monitor.query.order_by(Monitor.id.desc()).first()

        assert db_monitor.protocol == protocol
        assert db_monitor.delay == 30
        assert db_monitor.name == "Monitor1"
        assert db_monitor.target == "www.test.com"
        assert db_monitor.active is True
        assert db_monitor.created_at is not None
        assert db_monitor.updated_at is not None


def test_monitor_as_dict():
    # It creates a dictionary with the correct values
    monitor = Monitor(1, 30, "Monitor1", "www.test.com", True).as_dict()

    assert monitor["protocol_id"] == "1"
    assert monitor["delay"] == "30"
    assert monitor["name"] == "Monitor1"
    assert monitor["target"] == "www.test.com"
    assert monitor["active"] == "True"


def test_monitor_http_records(app):
    # It has the correct assiociated http records
    with app.app_context():
        protocol = Protocol.create("http")
        monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
        another_monitor = Monitor.create(
            protocol.id, 60, "Monitor2", "www.test2.com", False
        )

        expected_records = []
        for _ in range(10):
            expected_records.append(HttpRecord.create(monitor.id, True, 20, 200, ""))
        for _ in range(10):
            # Create unrelated records
            HttpRecord.create(another_monitor.id, True, 20, 200, "")

        assert monitor.http_records == expected_records


def test_monitor_ssl_records(app):
    # It has the correct assiociated ssl records
    with app.app_context():
        protocol = Protocol.create("ssl")
        monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
        another_monitor = Monitor.create(
            protocol.id, 60, "Monitor2", "www.test2.com", False
        )

        expected_records = []
        for _ in range(10):
            expected_records.append(
                SslRecord.create(
                    monitor.id, True, "Example Auth", datetime.datetime.now()
                )
            )
        for _ in range(10):
            # Create unrelated records
            SslRecord.create(
                another_monitor.id, True, "Example Auth", datetime.datetime.now()
            )

        assert monitor.ssl_records == expected_records
