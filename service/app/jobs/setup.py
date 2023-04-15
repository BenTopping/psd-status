from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl
from app.extensions import scheduler


def context_http(monitor):
    with scheduler.app.app_context():
        get_http(monitor)


def context_ssl(monitor):
    with scheduler.app.app_context():
        get_ssl(monitor)


def setup_jobs():
    with scheduler.app.app_context():
        monitors = Monitor.query.all()
        http_protocol = Protocol.query.filter(Protocol.name == "http").first()
        ssl_protocol = Protocol.query.filter(Protocol.name == "ssl").first()

        for monitor in monitors:
            if monitor.protocol == http_protocol:
                scheduler.add_job(
                    id=str(monitor.id),
                    func=context_http,
                    args=[monitor],
                    trigger="interval",
                    seconds=monitor.delay,
                )
            elif monitor.protocol == ssl_protocol:
                scheduler.add_job(
                    id=str(monitor.id),
                    func=context_ssl,
                    args=[monitor],
                    trigger="interval",
                    seconds=monitor.delay,
                )
    print("-> Succesfully started scheduled jobs!")
