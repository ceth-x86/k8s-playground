from datetime import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def get_current_datetime():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_datetime_app2": current_time}


@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/readyz")
def readyz():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
