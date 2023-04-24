import requests
from app.models.monitor import Monitor
from app.models.protocol import Protocol
from app.models.http_record import HttpRecord


# Given a monitor object make a get http request and record
# Ensure that the monitor protocol is joined before running
def get_http(monitor: Monitor):
    if monitor.protocol.name not in ["http", "https"]:
        return { 'errors': "Invalid protocol" }

    url = f"{monitor.protocol.name}://{monitor.target}"
    success = False
    response_time = None
    status_code = None
    errors = ""

    try:
        r = requests.get(url)
        response_time = r.elapsed.total_seconds()
        status_code = r.status_code
        r.raise_for_status()
        success = True
    except requests.exceptions.HTTPError as errh:
        errors = "HTTP Error: " + str(errh)
    except requests.exceptions.ConnectionError as errc:
        errors = "Connection Error: " + str(errc)
    except requests.exceptions.Timeout as errt:
        errors = "Timeout Error: " + str(errt)
    except requests.exceptions.RequestException as err:
        errors = "Request exception: " + str(err)

    http_record = HttpRecord.create(
        monitor.id, success, response_time, status_code, errors
    )

    return http_record
