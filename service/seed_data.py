from app import create_app
from app.models.user import User
from app.models.protocol import Protocol
from app.config import Config


class SeedConfig(Config):
    TESTING = True
    SCHEDULER_RUN = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/psd_status"


def insert_seed_data():
    app = create_app(config_class=SeedConfig)
    with app.app_context():
        # Generate users
        print("-> Generating users")
        User.create("admin", "admin")

        # Generate protocols
        print("-> Generating protocols")
        Protocol.create("http")
        Protocol.create("https")


if __name__ == "__main__":
    insert_seed_data()
