from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

# These are declared here so that both the Flask app and various files can reference the same object
scheduler = APScheduler()
db = SQLAlchemy()
