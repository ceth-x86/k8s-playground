from datetime import datetime, timedelta
from threading import Lock
from collections import deque

from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

class RequestTracker:
    def __init__(self):
        self.request_timestamps = deque()
        self.lock = Lock()
        self.requests_per_minute = Gauge('requests_per_minute', 'Number of requests in the last minute')

    def record_request(self):
        with self.lock:
            now = datetime.now()
            one_minute_ago = now - timedelta(minutes=1)
            
            # Remove timestamps older than one minute
            while self.request_timestamps and self.request_timestamps[0] < one_minute_ago:
                self.request_timestamps.popleft()
            
            # Add the new timestamp
            self.request_timestamps.append(now)
            self.requests_per_minute.set(len(self.request_timestamps))
            return now

tracker = RequestTracker()

@app.route("/")
def get_current_datetime():
    now = tracker.record_request()
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

