# Background Processing Application

This project demonstrates a simple Flask web application that has been extended to include background processing capabilities using Redis. It also includes a Kubernetes Job that utilizes Redis to perform a batch calculation.

The project is organized into several folders:

- `app/`: Contains the Python application code and Dockerfile for the main Flask app.
- `fibonacci-job/`: Contains the Python application and Dockerfile for the one-off Fibonacci calculation job.
- `fibonacci-worker/`: Contains the Python application and Dockerfile for the Fibonacci worker that processes jobs from the Redis queue.
- `k8s/`: Contains all Kubernetes deployment files (main app, Redis, one-off job, and cronjob).

## Components

### Simple Python Web Application with Redis

The main Flask web application now uses Redis for background job management.
- The root endpoint (`/`) returns the current date and time along with the number of jobs currently in the Redis queue.
- A new endpoint (`/process`) enqueues a simple job into the Redis queue.
- An endpoint (`/enqueue/<int:number>`) enqueues a specific number into the Redis queue. This number represents the position in the Fibonacci sequence to be calculated by the worker.
- An endpoint (`/fibonacci/<int:position>`) retrieves a calculated Fibonacci number from Redis.

### Redis Service

A Redis service has been deployed to support the background processing for the simple web application and the Fibonacci job.

### Fibonacci Calculation Job (One-off)

This is a Kubernetes `Job` that calculates the first 10 Fibonacci numbers and stores them in Redis. This is a one-time job.

### Fibonacci Worker (CronJob)

This is a Kubernetes `CronJob` that runs every minute. It checks the `job_queue` in Redis for a number, and if it finds one, it calculates the Fibonacci number for that position and stores the result back in Redis. This acts as a background worker processing jobs enqueued via the `/enqueue/<int:number>` endpoint.

## Deployment and Usage

### Simple Python Web Application

1.  **Build the Docker Image:**
    ```bash
    docker build -t simple-app:latest background-processing/app
    ```
2.  **Deploy to Kubernetes (App and Redis):**
    ```bash
    kubectl apply -f background-processing/k8s/deployment.yaml
    kubectl apply -f background-processing/k8s/redis-deployment.yaml
    ```
3.  **Access the Application (OrbStack):**
    The `LoadBalancer` service in OrbStack will show its external IP as `<pending>`. You can access the application directly using its ClusterIP.
    Using the ClusterIP found via `kubectl get services`, for example:
    ```
    http://192.168.194.218:80
    ```
    Alternatively, you can use the OrbStack provided hostname:
    ```
    http://simple-app-service-lb.k8s.orb.local
    ```
    To add jobs for the worker to process, navigate to `/enqueue/<number>` on either of the above URLs (e.g., `http://192.168.194.218:80/enqueue/15`).

### Fibonacci Calculation Job (One-off)

1.  **Build the Docker Image:**
    ```bash
    docker build -t fibonacci-job:latest background-processing/fibonacci-job/app
    ```
2.  **Run the Kubernetes Job:**
    ```bash
    kubectl apply -f background-processing/k8s/job.yaml
    ```
    You can check the job status with `kubectl get jobs`. To view logs: `kubectl logs <pod-name-of-job>`.
    After the job completes, you can connect to Redis to verify the stored Fibonacci numbers.

### Fibonacci Worker (CronJob)

1.  **Build the Docker Image:**
    ```bash
    docker build -t fibonacci-worker:latest background-processing/fibonacci-worker/app
    ```
2.  **Run the Kubernetes CronJob:**
    ```bash
    kubectl apply -f background-processing/k8s/cronjob.yaml
    ```
    You can check the cronjob status with `kubectl get cronjobs`. The job will be created every minute. You can see the pods it creates with `kubectl get pods`. To view the logs from a worker pod, use `kubectl logs <pod-name-of-worker>`.


