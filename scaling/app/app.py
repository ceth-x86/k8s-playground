from datetime import datetime, timedelta
from threading import Lock

from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# a thread-safe dictionary to store request timestamps
request_timestamps = []
lock = Lock()

requests_per_minute = Gauge('requests_per_minute', 'Number of requests in the last minute')

@app.route("/")
def get_current_datetime():
    with lock:
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        # Remove timestamps older than one minute
        while request_timestamps and request_timestamps[0] < one_minute_ago:
            request_timestamps.pop(0)
        # Add the new timestamp
        request_timestamps.append(now)
        requests_per_minute.set(len(request_timestamps))
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return {"current_datetime": current_time}


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/readyz")
def readyz():
    return "OK", 200


@app.route("/test")
def test():
    return "hello"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

