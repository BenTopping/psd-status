from app import create_app
from app.models.user import User
from app.models.protocol import Protocol
from app.models.monitor import Monitor
from app.models.http_record import HttpRecord
from app.models.ssl_record import SslRecord
from app.config import Config
from faker import Faker
import random
import datetime

# A script to generate dummy data for development purposes
fake = Faker()


class DummyConfig(Config):
    TESTING = True
    SCHEDULER_RUN = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/psd_status"


def insert_dummy_data():
    app = create_app(config_class=DummyConfig)
    with app.app_context():
        # Generate monitors
        # Would be nice to randomise the creation of these more thoroughly
        print("-> Generating monitors")
        http_protocol = Protocol.query.filter(Protocol.name == "http").first()
        https_protocol = Protocol.query.filter(Protocol.name == "https").first()
        delays = [60, 120, 300, 600]
        # [60, 120, 300, 600, 1800, 86400, 604800]
        # Create http monitors using known web addresses
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Google",
            target="google.com",
            active=True,
        )
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Bing",
            target="bing.com",
            active=True,
        )
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Ecosia",
            target="ecosia.com",
            active=True,
        )
        # Create ssl monitors
        Monitor.create(
            protocol_id=https_protocol.id,
            delay=random.choice(delays),
            name="Apple",
            target="apple.com",
            active=True,
        )
        Monitor.create(
            protocol_id=https_protocol.id,
            delay=random.choice(delays),
            name="Microsoft",
            target="microsoft.com",
            active=True,
        )

        # Generate http_records
        monitors = Monitor.query.all()
        print("-> Generating http and ssl records")
        for monitor in monitors:
            if monitor.protocol == http_protocol or monitor.protocol == https_protocol:
                for _ in range(100):
                    HttpRecord.create(
                        monitor.id,
                        True,
                        random.randint(1, 100) / 100,
                        random.choice([200, 201, 404, 500]),
                        fake.pystr(),
                    )
            if monitor.protocol == https_protocol:
                start_date = datetime.datetime.now()
                end_date = datetime.datetime.now() + datetime.timedelta(days=365)
                for _ in range(5):
                    SslRecord.create(
                        monitor.id,
                        True,
                        "GenericAuthority",
                        fake.date_between(start_date, end_date),
                    )


if __name__ == "__main__":
    insert_dummy_data()
