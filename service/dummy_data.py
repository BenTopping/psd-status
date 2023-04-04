from app import create_app
from app.models.user import User
from app.models.protocol import Protocol
from app.models.monitor import Monitor
from app.models.http_record import HttpRecord
from app.models.ssl_record import SslRecord
from app.models import db
import random
import datetime
from faker import Faker

# A script to generate dummy data for development purposes
fake = Faker()

def insert_dummy_data():
    app = create_app()
    with app.app_context():
        # Generate users
        print("-> Generating users")
        User.create("admin", "admin")


        # Generate protocols
        print("-> Generating protocols")
        Protocol.create("http")
        Protocol.create("ssl")

        # Generate monitors
        # Would be nice to randomise the creation of these more thoroughly
        print("-> Generating monitors")
        http_protocol = Protocol.query.filter(Protocol.name == "http").first()
        ssl_protocol = Protocol.query.filter(Protocol.name == "ssl").first()
        delays = [60, 120, 300, 600, 1800, 86400, 604800]
        ## Create http monitors using known web addresses
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Google",
            target="google.com",
            active=True
        )
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Bing",
            target="bing.com",
            active=True
        )
        Monitor.create(
            protocol_id=http_protocol.id,
            delay=random.choice(delays),
            name="Ecosia",
            target="ecosia.com",
            active=True
        )
        ## Create ssl monitors
        Monitor.create(
            protocol_id=ssl_protocol.id,
            delay=delays[5],
            name="Apple",
            target="apple.com",
            active=True
        )
        Monitor.create(
            protocol_id=ssl_protocol.id,
            delay=delays[6],
            name="Microsoft",
            target="microsoft.com",
            active=True
        )

        # Generate http_records
        monitors = Monitor.query.all()
        print("-> Generating http and ssl records")
        for monitor in monitors:
            if monitor.protocol == http_protocol:
                for _ in range(100):
                    HttpRecord.create(
                        monitor.id,
                        random.randint(50, 1000),
                        random.choice([200, 201, 404, 500]),
                        fake.pystr()
                    )
            if monitor.protocol == ssl_protocol:
                start_date = datetime.datetime.now()
                end_date = datetime.datetime.now() + datetime.timedelta(days=365)
                for _ in range(5):
                    SslRecord.create(
                        monitor.id,
                        True,
                        "GenericAuthority",
                        fake.date_between(start_date, end_date)
                    )

if __name__ == "__main__":
    insert_dummy_data()