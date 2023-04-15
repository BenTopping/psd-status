from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

scheduler = APScheduler()
db = SQLAlchemy()
