# Scaling Application

This directory contains a simple Flask application demonstrating horizontal scaling and Prometheus integration.

## How Prometheus Monitoring Works (Pull Model)

Prometheus operates on a "pull" model for collecting metrics. This means:

1.  **Application Exposes Metrics:** Your Flask application, known as a "target" to Prometheus, exposes its metrics via a specific HTTP endpoint (in this case, `/metrics`). When requested, it provides the current state of its metrics in a plain text format.

2.  **Prometheus Scrapes Metrics:** The Prometheus server is configured to periodically scrape (or "pull") these metrics from its targets. It actively makes HTTP requests to your application's `/metrics` endpoint at a defined `scrape_interval` (e.g., every 15 seconds).

3.  **Kubernetes Service Discovery:** Prometheus leverages Kubernetes' service discovery mechanism to find your application pods. It looks for specific annotations on your pods (like `prometheus.io/scrape: "true"`, `prometheus.io/port`, and `prometheus.io/path`) to identify which pods to scrape and how to connect to their metrics endpoint.

4.  **Data Storage:** Once scraped, Prometheus stores this time-series data in its own database, along with various labels (e.g., `app`, `instance`, `job`, `kubernetes_pod_name`) that provide context about the source of the metric.

This pull model simplifies application configuration, centralizes control at the Prometheus server, and provides clear visibility when an application or metric endpoint becomes unavailable.

## Deployment to Kubernetes with Prometheus

Follow these steps to deploy the application and Prometheus to your Kubernetes cluster:

### Prerequisites

*   A running Kubernetes cluster.
*   `kubectl` configured to communicate with your cluster.
*   Docker installed and configured.

### 1. Build and Push Docker Image

Navigate to the `scaling/app` directory and build your Docker image. Replace `your-docker-username` with your Docker Hub username and `your-image-name` with a name for your application image (e.g., `my-scaling-app`).

```bash
cd scaling/app
docker build -t your-docker-username/k8s-scaling:latest .
docker push your-docker-username/k8s-scaling:latest
```

**Note:** If you are using a local Kubernetes cluster like Minikube or Kind, you might need to load the image into the cluster's Docker daemon instead of pushing to a remote registry.
For Minikube:
```bash
eval $(minikube docker-env)
docker build -t k8s-scaling:latest .
```
Then, update `scaling/k8s/deployment.yaml` to use `image: k8s-scaling:latest` and `imagePullPolicy: Never`.

### 2. Update Kubernetes Deployment YAML

Before applying, ensure the `image` field in `scaling/k8s/deployment.yaml` points to the image you just pushed.

Open `scaling/k8s/deployment.yaml` and change:
```yaml
        image: simple-app:latest
```
to:
```yaml
        image: your-docker-username/k8s-scaling:latest
```

### 3. Apply Kubernetes Manifests

Apply all the Kubernetes configuration files located in the `scaling/k8s` directory. This will deploy your application and Prometheus.

```bash
kubectl apply -f scaling/k8s/
```

### 4. Verify Deployment and Access Prometheus

1.  **Check Pod Status:**
    ```bash
    kubectl get pods
    ```
    Ensure that your application pods (e.g., `simple-app-deployment-...`) and the Prometheus pod (`prometheus-deployment-...`) are running.

2.  **Access Application:**
    Get the external IP of your application's load balancer service:
    ```bash
    kubectl get services
    ```
    Look for `simple-app-service-lb` and find its `EXTERNAL-IP`. You can then access your application in a web browser using `http://EXTERNAL-IP/`.

3.  **Access Prometheus UI:**
    Get the external IP of the Prometheus load balancer service:
    ```bash
    kubectl get services
    ```
    Look for `prometheus-service` and find its `EXTERNAL-IP`. You can then access the Prometheus UI in a web browser using `http://EXTERNAL-IP:9090`.

    In the Prometheus UI, you can query for the `requests_per_minute` metric to observe the application's request rate.

Feel free to open issues or contribute to improve this setup.
