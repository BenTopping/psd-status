import requests
from app.models.monitor import Monitor
from app.models.http_record import HttpRecord

# Given a monitor object make a get http request and record
def get_http(monitor: Monitor):
    url = f"https://{monitor.target}"
    response_time = None
    status_code = None
    errors = ""

    try:
        r = requests.get(url)
        response_time = r.elapsed.total_seconds()
        status_code = r.status_code
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        errors = "HTTP Error: " + str(errh)
    except requests.exceptions.ConnectionError as errc:
        errors = "Connection Error: " + str(errc)
    except requests.exceptions.Timeout as errt:
        errors = "Timeout Error: " + str(errt)
    except requests.exceptions.RequestException as err:
        errors = "Request exception: " + str(err)

    http_record = HttpRecord.create(monitor.id, response_time, status_code, errors)

    return http_record
