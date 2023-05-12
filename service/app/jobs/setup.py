from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl
from app.extensions import scheduler
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


def context_http(monitor):
    with scheduler.app.app_context():
        get_http(monitor)


def context_ssl():
    with scheduler.app.app_context():
        monitors = (
            Monitor.query.join(Protocol)
            .filter(
                Protocol.name == "https",
            )
            .all()
        )
        for monitor in monitors:
            get_ssl(monitor)


def setup_jobs():
    with scheduler.app.app_context():
        monitors = (
            Monitor.query.join(Protocol)
            .filter(or_(Protocol.name == "http", Protocol.name == "https"))
            .options(joinedload(Monitor.protocol))
            .all()
        )

        # Setup http and https jobs
        for monitor in monitors:
            scheduler.add_job(
                id=str(monitor.id),
                func=context_http,
                args=[monitor],
                trigger="interval",
                seconds=monitor.delay,
            )

        # Setup SSL job to run once a day (86400 seconds)
        scheduler.add_job(
            id="ssl_job",
            func=context_ssl,
            trigger="interval",
            seconds=86400,
        )

    print("-> Succesfully started scheduled jobs!")
