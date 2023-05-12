from app.models.ssl_record import SslRecord
from app.models.monitor import Monitor
from app.models.protocol import Protocol
import datetime


def test_new_ssl_record():
    expiry_date = datetime.datetime.now()
    ssl_record = SslRecord(1, True, "test authority", expiry_date)

    assert ssl_record.monitor_id == 1
    assert ssl_record.success is True
    assert ssl_record.authority == "test authority"
    assert ssl_record.expiry_date == expiry_date


def test_create_ssl_record(app):
    with app.app_context():
        protocol = Protocol.create("ssl")
        monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
        # The db may round the seconds so we dont want to check milliseconds
        expiry_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        SslRecord.create(monitor.id, True, "test authority", expiry_date)

        # Checks latest ssl_record created has same details as above
        db_ssl_record = SslRecord.query.order_by(SslRecord.id.desc()).first()
        assert db_ssl_record.monitor == monitor
        assert db_ssl_record.success is True
        assert db_ssl_record.authority == "test authority"
        # We format to str as the db record expiry_date isnt an instance of datetime
        assert str(db_ssl_record.expiry_date) == str(expiry_date)
        assert db_ssl_record.created_at is not None


def test_ssl_record_as_dict():
    expiry_date = datetime.datetime.now()
    ssl_record = SslRecord(1, True, "test authority", expiry_date).as_dict()

    assert ssl_record["monitor_id"] == "1"
    assert ssl_record["success"] is True
    assert ssl_record["authority"] == "test authority"
    assert ssl_record["expiry_date"] == str(expiry_date)
    assert ssl_record["created_at"] is not None
