from app.protocols.ssl import get_ssl
from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.models.ssl_record import SslRecord
import datetime
from unittest import mock


def test_get_ssl_when_valid(app):
    protocol = Protocol.create("ssl")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        with mock.patch("ssl.create_default_context") as mock_ssl:
            mock_ssl.return_value.wrap_socket.return_value.__enter__.return_value.getpeercert.return_value = {
                "issuer": [[["commonName", "testAuthority"]]],
                "notAfter": "Mar  3 18:56:17 2024 GMT",
            }
            get_ssl(monitor)

            # Check connect was called with the correct values
            mock_ssl.return_value.wrap_socket.return_value.__enter__.return_value.connect.assert_called_with(
                (monitor.target, 443)
            )
            # Checks it creates a database record with the correct data
            db_ssl_record = SslRecord.query.order_by(SslRecord.id.desc()).first()
            assert db_ssl_record.monitor
            assert db_ssl_record.success is True
            assert db_ssl_record.authority == "testAuthority"
            assert db_ssl_record.expiry_date == datetime.datetime(
                2024, 3, 3, 18, 56, 17
            )


def test_get_ssl_when_cert_is_none(app):
    protocol = Protocol.create("ssl")
    monitor = Monitor.create(protocol.id, 30, "Monitor1", "www.test.com", True)
    with app.app_context():
        with mock.patch("ssl.create_default_context") as mock_ssl:
            mock_ssl.return_value.wrap_socket.return_value.__enter__.return_value.getpeercert.return_value = (
                None
            )
            get_ssl(monitor)

            # Check connect was called with the correct values
            mock_ssl.return_value.wrap_socket.return_value.__enter__.return_value.connect.assert_called_with(
                (monitor.target, 443)
            )
            # Checks it creates a database record with the correct data
            db_ssl_record = SslRecord.query.order_by(SslRecord.id.desc()).first()
            assert db_ssl_record.monitor
            assert db_ssl_record.success is False
            assert db_ssl_record.authority == ""
            assert db_ssl_record.expiry_date is None
