from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.protocols.http import get_http
from app.protocols.ssl import get_ssl

def setup_jobs(scheduler):
    with scheduler.app.app_context():
        monitors = Monitor.query.all()
        http_protocol = Protocol.query.filter(Protocol.name == "http").first()
        ssl_protocol = Protocol.query.filter(Protocol.name == "ssl").first()

        for monitor in monitors:
            if monitor.protocol == http_protocol:
                scheduler.add_job(id=str(monitor.id), func=get_http, args=[monitor], trigger='interval', seconds=monitor.delay)
            elif monitor.protocol == ssl_protocol:
                scheduler.add_job(id=str(monitor.id), func=get_ssl, args=[monitor], trigger='interval', seconds=monitor.delay)
    print("-> Succesfully started scheduled jobs!")
    
            