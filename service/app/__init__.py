from flask import Flask
from app.routes import test
from app.jobs.setup import setup_jobs
from app.extensions import db, scheduler
from app.config import Config

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
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
    app.register_blueprint(test.bp)

def setup_schedulers(app):
    scheduler.init_app(app)
    scheduler.start()
    setup_jobs()
