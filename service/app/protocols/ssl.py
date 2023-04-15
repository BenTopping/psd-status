import ssl
import socket
import datetime
from app.models.monitor import Monitor
from app.models.ssl_record import SslRecord


# Given a monitor object make a get http request and record
def get_ssl(monitor: Monitor):
    context = ssl.create_default_context()
    ssl_dateformat = r"%b %d %H:%M:%S %Y %Z"

    with context.wrap_socket(socket.socket(), server_hostname=monitor.target) as s:
        s.connect((monitor.target, 443))
        cert = s.getpeercert()

    if cert is not None:
        issuer = dict(x[0] for x in cert["issuer"])
        authority = issuer["commonName"]
        expiry_date = datetime.datetime.strptime(cert["notAfter"], ssl_dateformat)
        ssl_record = SslRecord.create(monitor.id, True, authority, expiry_date)
    else:
        ssl_record = SslRecord.create(monitor.id, False, "", None)

    return ssl_record
