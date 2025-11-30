# Simple Python Web Application

This project is a simple Flask web application that exposes a single endpoint returning the current date and time. The project is organized into several folders:

- `app/`: Contains the Python application code and Dockerfile.
- `k8s/`: Contains the Kubernetes deployment files.
- `docs/`: Contains detailed documentation.

## Documentation

For detailed instructions on how to use this project, please refer to the following documents:

- **[Running the Application Locally](./docs/local_development.md)**: Instructions on how to set up and run the application on your local machine.
- **[Containerizing with Docker](./docs/docker.md)**: Instructions on how to build and run the application as a Docker container.
- **[Deploying to Kubernetes](./docs/kubernetes.md)**: Instructions on how to deploy the application to a Kubernetes cluster.

### Internals

For a deeper dive into how some of the components work, see the following documents:

- **[How Ingress Works with OrbStack](./docs/internals/ingress_orb.md)**: An explanation of how `Ingress` resources are routed in a local OrbStack environment.

## Why does `curl` with a `Host` header work?

When interacting with the Ingress, you may notice that `curl -H "Host: simple-app.local" http://<INGRESS_IP>` succeeds, while `curl http://<INGRESS_IP>` returns a `404 Not Found` error.

This is because the Ingress controller uses the `Host` header to determine which service to route the request to. The routing rule is defined in `k8s/ingress.yaml`:

```yaml
...
spec:
  rules:
  - host: simple-app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: simple-app-service
            port:
              number: 80
```

This configuration tells the Ingress controller to only forward requests with the `Host` header set to `simple-app.local` to the `simple-app-service`. When the `Host` header is omitted, no rule matches, and the Ingress controller returns its own default 404 page.

### Ingress Applications Explained

This `ingress` directory now contains two identical Flask applications, `simple-app` and `simple-app2`, each running in its own Kubernetes Deployment and exposed via a `ClusterIP` Service. The `Ingress` resource is configured to route external traffic to these services based on hostnames.

#### Why a ClusterIP Service is needed with Ingress

Even when using an Ingress controller, a `ClusterIP` Service is essential in Kubernetes for several reasons:

1.  **Pods are Ephemeral:**
    *   Pods are the smallest, most basic deployable objects in Kubernetes. They typically contain one or more containers (like your `simple-app` or `simple-app2` running a Flask application).
    *   Pods are designed to be ephemeral: When a Pod is created, it's assigned a unique IP address from the cluster's internal network. If a Pod crashes, is restarted, or scaled horizontally, a new Pod (with a new IP address) is created.
    *   Because their IP addresses are not stable and can change frequently, you generally don't expose Pods directly to external traffic or even directly to other services within the cluster. Relying on Pod IPs would make inter-service communication brittle.

2.  **Stable Internal Endpoint (ClusterIP Service):**
    *   A `ClusterIP` Service provides a stable network endpoint (a static IP address and DNS name) for a set of Pods. It acts as an internal load balancer.
    *   **Stable Internal IP:** Unlike Pods, a `ClusterIP` Service has a fixed IP address within the cluster. This IP address remains constant even if the underlying Pods are replaced.
    *   **Service Discovery:** It allows other services or resources within the cluster to reliably find and communicate with your application, without needing to know the individual, changing IP addresses of the Pods. You refer to the application by the Service's name (e.g., `simple-app-service`).
    *   **Load Balancing:** The Service automatically distributes incoming traffic across all healthy Pods that match its selector (e.g., `app: simple-app`). If a Pod fails, the Service stops sending traffic to it.

3.  **Ingress Routes to Services, Not Pods:**
    *   An Ingress resource manages external access to services in a cluster, typically HTTP/S. However, an Ingress **does not** route traffic directly to Pods. Instead, it routes traffic to a **Service**.
    *   When an external request comes into the Ingress, the Ingress controller looks at its rules (e.g., `host: simple-app.local`, `path: /`).
    *   Based on these rules, it forwards the request to the specified Kubernetes Service (e.g., `simple-app-service`).
    *   The Service then takes that request and distributes it to one of the healthy Pods associated with it.

4.  **Decoupling for Resilience and Scalability:**
    *   The Service layer provides crucial decoupling:
        *   **Ingress from Pods:** The Ingress doesn't need to know anything about the individual Pods or their changing IP addresses. It only needs to know the stable name and port of the Service.
        *   **Client from Pods:** Any client within the cluster (or the Ingress itself) interacts with the stable Service endpoint, not directly with the ephemeral Pods.
        *   **Resilience and Scalability:** This separation allows you to scale your Pods up or down, replace failing Pods, or update your application (e.g., a rolling update) without affecting how the Ingress or other clients access your application. The Service ensures continuous availability and load balancing across the healthy Pods.

In summary, the `ClusterIP` Service acts as a vital intermediary, providing a stable, load-balanced front for your application's Pods, which the Ingress then uses to expose your application to the outside world. Without the Service, the Ingress would have no stable target to send traffic to.

### Usage Example

```bash
$ curl -H "Host: simple-app.local" http://192.168.139.2
{
  "current_datetime": "2025-11-30 12:00:03"
}
$ curl -H "Host: simple-app2.local" http://192.168.139.2
{
  "current_datetime_app2": "2025-11-30 12:00:06"
}
```