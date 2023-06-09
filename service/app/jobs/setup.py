from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl
from app.extensions import scheduler
from sqlalchemy.orm import joinedload


def context_http(monitor):
    with scheduler.app.app_context():
        get_http(monitor)


def context_ssl():
    with scheduler.app.app_context():
        monitors = (
            Monitor.query.join(Protocol)
            .filter(Protocol.name == "https", Monitor.active == True)  # noqa: E712
            .all()
        )
        for monitor in monitors:
            get_ssl(monitor)


def handle_http_job(monitor):
    with scheduler.app.app_context():
        # We need to requery the monitor to check it exists and to load its protocol
        # TODO there is probably a nice way of joining protocol to the existing object
        monitor = (
            Monitor.query.join(Protocol)
            .filter(
                Monitor.id == monitor.id,
            )
            .options(joinedload(Monitor.protocol))
            .one()
        )

    # If the job doesn't exist we want to create it
    if scheduler.get_job(str(monitor.id)) is None:
        if monitor.active is True:
            scheduler.add_job(
                id=str(monitor.id),
                func=context_http,
                args=[monitor],
                trigger="interval",
                seconds=monitor.delay,
            )
    else:
        # If the job exists we want to update it if it is active
        if monitor.active is True:
            scheduler.modify_job(
                id=str(monitor.id),
                func=context_http,
                args=[monitor],
                trigger="interval",
                seconds=monitor.delay,
            )
        else:
            # If the job exists and it is not active we want to remove it
            scheduler.remove_job(id=str(monitor.id))


def setup_jobs():
    with scheduler.app.app_context():
        monitors = (
            Monitor.query.join(Protocol)
            .filter(
                (Protocol.name == "http") | (Protocol.name == "https"),
                Monitor.active == True,  # noqa: E712
            )
            .options(joinedload(Monitor.protocol))
            .all()
        )

        # Setup http and https jobs
        for monitor in monitors:
            handle_http_job(monitor)

        # Setup SSL job to run once a day (86400 seconds)
        scheduler.add_job(
            id="ssl_job",
            func=context_ssl,
            trigger="interval",
            seconds=86400,
        )

    print("-> Succesfully started scheduled jobs!")
