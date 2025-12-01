from datetime import datetime
import os
import redis

from flask import Flask

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@app.route("/")
def get_current_datetime():
    jobs = redis_client.llen("job_queue")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "current_datetime": current_time,
        "jobs_in_queue": jobs,
    }

@app.route("/process")
def process():
    job_id = redis_client.rpush("job_queue", "job")
    return {"status": "job enqueued", "job_id": job_id}

@app.route("/fibonacci/<int:position>")
def get_fibonacci(position):
    fib_key = f"fib:{position}"
    fib_value = redis_client.get(fib_key)
    
    if fib_value:
        return {"position": position, "fibonacci_number": int(fib_value)}
    else:
        return {"error": f"Fibonacci number at position {position} not found in Redis."}, 404

@app.route("/enqueue/<int:number>")
def enqueue_number(number):
    redis_client.rpush("job_queue", number)
    return {"status": "number enqueued", "number": number}


@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/readyz")
def readyz():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
