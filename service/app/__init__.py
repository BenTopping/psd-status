from flask import Flask
from flask_cors import CORS
from app.routes import authentication, monitors, protocol, http_records
from app.jobs.setup import setup_jobs
from app.extensions import db, scheduler
from app.config import Config


def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # setup database
    db.init_app(app)
    # setup routes
    setup_routes(app)
    # setup schedulers
    if app.config.get("SCHEDULER_RUN", True):
        setup_schedulers(app)

    return app


def setup_routes(app):
    # Register the imported blueprints
    app.register_blueprint(authentication.bp, url_prefix="/v1")
    app.register_blueprint(monitors.bp, url_prefix="/v1")
    app.register_blueprint(protocol.bp, url_prefix="/v1")
    app.register_blueprint(http_records.bp, url_prefix="/v1")


def setup_schedulers(app):
    # Setup the scheduler and its jobs
    scheduler.init_app(app)
    scheduler.start()
    setup_jobs()
