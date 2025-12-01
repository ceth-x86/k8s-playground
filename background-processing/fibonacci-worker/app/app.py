import os
import redis
import time

def fibonacci(n):
    if n < 0:
        return None
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_client = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

    print("Checking for jobs in the queue...")
    job_number = redis_client.lpop("job_queue")

    if job_number:
        try:
            position = int(job_number)
            print(f"Calculating Fibonacci for position: {position}")
            fib_val = fibonacci(position)

            if fib_val is not None:
                redis_client.set(f"fib:{position}", fib_val)
                print(f"Fibonacci({position}) = {fib_val} has been calculated and stored in Redis.")
            else:
                print(f"Invalid position number received: {position}")

        except ValueError:
            print(f"Could not convert job to integer: {job_number}")
    else:
        print("No jobs in the queue.")

if __name__ == "__main__":
    main()
