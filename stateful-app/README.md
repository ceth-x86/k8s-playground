# Stateful Python Web Application with MariaDB

This project is a Flask web application that now includes MariaDB integration for request logging. It exposes an endpoint returning the current date and time, and another to view recent requests.

- `app/`: Contains the Python application code, Dockerfile, and `requirements.txt`.
- `k8s/`: Contains the Kubernetes deployment files, including configurations for MariaDB.
- `docs/`: Contains detailed documentation.

## Features

- **Current Date and Time**: The root endpoint (`/`) returns the current date and time.
- **Request Logging**: All incoming requests (excluding `/healthz`, `/readyz`, and `/requests`) are logged to a MariaDB database.
- **Last 10 Requests**: The `/requests` endpoint returns the last 10 logged requests from the MariaDB database.
- **Health Checks**: `/healthz` and `/readyz` endpoints for liveness and readiness probes, with `/readyz` also checking database connectivity.

## Accessing the Application on Kubernetes

When running on a local Kubernetes cluster like Minikube or OrbStack, the `LoadBalancer` service may not get an external IP address. You can use `kubectl port-forward` to access the application:

```bash
kubectl port-forward service/stateful-app-service-lb 8080:80
```

You can then access the application at `http://localhost:8080`.

### Why is Port Forwarding Necessary for Local Development?

In a cloud environment (like AWS, GCP, or Azure), creating a `Service` of type `LoadBalancer` automatically provisions a cloud load balancer with a public IP address.

However, in a local Kubernetes environment (like OrbStack, Minikube, or Docker Desktop), there's no cloud infrastructure to provide an external load balancer. This is why the `EXTERNAL-IP` for the service remains in a `<pending>` state.

`kubectl port-forward` is a convenient tool for development that creates a direct tunnel from your local machine to the service inside your cluster, allowing you to access it without needing an external IP.

For more permanent solutions in a local environment, you could consider using a `NodePort` service type or setting up an Ingress controller.

## Documentation

For detailed instructions on how to use this project, please refer to the following documents:

- **[Running the Application Locally](./docs/local_development.md)**: Instructions on how to set up and run the application on your local machine.
- **[Containerizing with Docker](./docs/docker.md)**: Instructions on how to build and run the application as a Docker container.
- **[Deploying to Kubernetes](./docs/kubernetes.md)**: Instructions on how to deploy the application to a Kubernetes cluster.

### Applying Kubernetes Resources (Split Files)

Since the Kubernetes deployment files have been split, you need to apply them in a specific order:

1.  **Secret**: This resource holds sensitive information like database credentials.
    ```bash
    kubectl apply -f stateful-app/k8s/secret.yaml
    ```
2.  **Persistent Volume Claim (PVC)**: This requests persistent storage for the MariaDB database.
    ```bash
    kubectl apply -f stateful-app/k8s/pvc.yaml
    ```
3.  **MariaDB Deployment and Service**: This sets up the MariaDB database within the cluster.
    ```bash
    kubectl apply -f stateful-app/k8s/mariadb-deployment.yaml
    ```
4.  **Stateful Application Deployment and Service**: This sets up the Flask application, configured to connect to the MariaDB instance.
    ```bash
    kubectl apply -f stateful-app/k8s/stateful-app-deployment.yaml
    ```

### Internals

For a deeper dive into how some of the components work, see the following documents:

- **[How LoadBalancer Works with OrbStack](./docs/internals/loadbalancer_orb.md)**: An explanation of how `LoadBalancer` services are routed in a local OrbStack environment.