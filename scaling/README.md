# Scaling Application

This directory contains a simple Flask application demonstrating horizontal scaling and Prometheus integration.

## How Prometheus Monitoring Works (Pull Model)

Prometheus operates on a "pull" model for collecting metrics. This means:

1.  **Application Exposes Metrics:** Your Flask application, known as a "target" to Prometheus, exposes its metrics via a specific HTTP endpoint (in this case, `/metrics`). When requested, it provides the current state of its metrics in a plain text format.

2.  **Prometheus Scrapes Metrics:** The Prometheus server is configured to periodically scrape (or "pull") these metrics from its targets. It actively makes HTTP requests to your application's `/metrics` endpoint at a defined `scrape_interval` (e.g., every 15 seconds).

3.  **Kubernetes Service Discovery:** Prometheus leverages Kubernetes' service discovery mechanism to find your application pods. It looks for specific annotations on your pods (like `prometheus.io/scrape: "true"`, `prometheus.io/port`, and `prometheus.io/path`) to identify which pods to scrape and how to connect to their metrics endpoint.

4.  **Data Storage:** Once scraped, Prometheus stores this time-series data in its own database, along with various labels (e.g., `app`, `instance`, `job`, `kubernetes_pod_name`) that provide context about the source of the metric.

This pull model simplifies application configuration, centralizes control at the Prometheus server, and provides clear visibility when an application or metric endpoint becomes unavailable.

## Horizontal Pod Autoscaling (HPA) with Custom Metrics

This section explains how to configure a Horizontal Pod Autoscaler (HPA) to automatically scale your `simple-app-deployment` based on the custom `requests_per_minute` metric we are exposing.

### Prerequisites for HPA

The HPA needs a way to access custom metrics from Prometheus. This is achieved by deploying the Prometheus Adapter.

#### 1. Install Prometheus Adapter

The Prometheus Adapter queries Prometheus for your custom metrics and exposes them through the Kubernetes Custom Metrics API, which the HPA can then access.

First, create a `prometheus-adapter-values.yaml` file in the `scaling/k8s/` directory with the following content. This file configures the adapter to find your `requests_per_minute` metric:
```yaml
prometheus:
  url: http://prometheus-service.default.svc
  port: 9090

rules:
  custom:
  - seriesQuery: '{__name__="requests_per_minute"}'
    resources:
      overrides:
        kubernetes_namespace: {resource: "namespace"}
        kubernetes_pod_name: {resource: "pod"}
    name:
      matches: "requests_per_minute"
      as: "requests_per_minute"
    metricsQuery: 'avg(<<.Series>>{<<.LabelMatchers>>}) by (<<.GroupBy>>)'
```

Next, add the `prometheus-community` Helm repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Finally, install the Prometheus Adapter using Helm and your custom values file. If you have an existing release named `prometheus-adapter`, use `helm upgrade` instead of `helm install`:
```bash
# For a new installation:
helm install prometheus-adapter prometheus-community/prometheus-adapter -f scaling/k8s/prometheus-adapter-values.yaml

# To upgrade an existing installation:
helm upgrade prometheus-adapter prometheus-community/prometheus-adapter -f scaling/k8s/prometheus-adapter-values.yaml
```
After a few minutes, the adapter will be running and exposing your custom metric to the Kubernetes API.

#### 2. Create the HorizontalPodAutoscaler (HPA)

Now, we can create the HPA resource. Create a file named `scaling/k8s/hpa.yaml` with the following content:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: simple-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: simple-app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Pods
    pods:
      metric:
        name: requests_per_minute
      target:
        type: AverageValue
        # HPA will scale up if the average is above this value, and scale down if below.
        averageValue: "3" # Target average value of 3 requests per minute per pod
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Pods
        value: 2
        periodSeconds: 15 # Add 2 pods every 15 seconds if the threshold is breached
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 60 # Remove 1 pod every 60 seconds if below the threshold
```
This HPA will maintain a minimum of 2 pods and scale up to a maximum of 10 pods, trying to keep the average `requests_per_minute` per pod at `3`.

#### 3. Apply and Test the HPA

Apply the HPA manifest to your cluster:
```bash
kubectl apply -f scaling/k8s/hpa.yaml
```

To observe the HPA in action, run the following command in a separate terminal:
```bash
kubectl get hpa simple-app-hpa --watch
```

##### Understanding HPA Target Values

When observing the HPA status using `kubectl get hpa simple-app-hpa --watch`, pay attention to the `TARGETS` column. This column shows `Current Average / Target Average`.

*   **Target Average:** This is the `averageValue` you configured in your `hpa.yaml` (in our case, `3`). The HPA aims to maintain this average `requests_per_minute` per pod.
*   **Current Average:** This is the actual average `requests_per_minute` per pod that the HPA is reading from the Custom Metrics API.

You might notice values in the "Current Average" part of the `TARGETS` column expressed with an "m" suffix (e.g., `73333m/3`). The "m" stands for "milli-" (one-thousandth). This is a standard Kubernetes notation for representing fractional values as whole numbers to avoid floating-point numbers in some contexts.

For example:
*   `73333m` means `73333 / 1000 = 73.333`
*   `45300m` means `45300 / 1000 = 45.3`

So, if `TARGETS` shows `73333m/3`, it means the current average is `73.333` requests per minute per pod, and the target is `3`. Because `73.333` is significantly higher than `3`, the HPA would scale up the number of replicas.

To generate traffic and trigger the autoscaler, run this `curl` loop in another terminal:
```bash
while true; do curl http://<your-external-ip>/ > /dev/null; sleep 0.1; done
# Replace <your-external-ip> with the IP of your simple-app-service-lb
```
As you generate traffic, you will see the `TARGETS` column in the HPA output increase, and the `REPLICAS` count will go up. When you stop the traffic, the `TARGETS` will decrease, and after the stabilization window, the `REPLICAS` count will go down.

Feel free to open issues or contribute to improve this setup.
