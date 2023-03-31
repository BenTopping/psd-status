from flask import Flask
from app.models import db

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/psd_status"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # setup database
    db.init_app(app)
    # setup routes
    setup_routes(app)
    # setup schedulers
    setup_schedulers(app)

    return app


def setup_routes(app):
    from app.routes import test

    app.register_blueprint(test.bp)


def setup_schedulers(app):
    pass
