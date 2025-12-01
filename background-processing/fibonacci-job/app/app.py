import os
import redis
import time

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_client = redis.Redis(host=redis_host, port=6379, db=0)

    print("Calculating Fibonacci numbers...")
    for i in range(10):
        fib_val = fibonacci(i)
        print(f"Fibonacci({i}) = {fib_val}")
        redis_client.set(f"fib:{i}", fib_val)

    print("Finished writing Fibonacci numbers to Redis.")

if __name__ == "__main__":
    main()
