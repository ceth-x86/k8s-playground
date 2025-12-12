# Simple KinD Cluster with Ingress

This project demonstrates how to set up a simple Kubernetes cluster using KinD (Kubernetes in Docker), deploy a multi-tier application with a custom-built frontend and backend, and configure an Ingress controller to manage external access.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

## Overview

The setup consists of:

1.  `kind-config.yaml`: Configures a single-node KinD cluster with specific port mappings (`80`, `443`, `30080`) from the host to the cluster's node. This allows us to access services running inside the cluster.
2.  `ingress.yaml`: Contains the necessary Kubernetes resources to deploy the NGINX Ingress Controller. This controller will manage routing external traffic to the correct services within the cluster.
3.  `app.yaml`: Defines our sample three-tier application within the `demo-app` namespace:
    *   **Database**: A Redis database (not actively used by the sample apps, but included as an example).
    *   **Backend**: A custom Python Flask application located in the `backend/` directory.
    *   **Frontend**: A custom Node.js/Express application located in the `frontend/` directory. It serves a static HTML page and proxies API requests to the backend.
    *   **Ingress**: An Ingress resource that routes traffic to the frontend (`/`) and the API (`/api`) using the hostname `my-app.local`.

## Setup Instructions

### 1. Create the KinD Cluster

First, create the local Kubernetes cluster using the provided configuration:

```bash
kind create cluster --config kind-config.yaml
```

### 2. Build and Load Application Images

Since our `app.yaml` file refers to images `frontend-web:latest` and `backend-api:latest` that don't exist in a public registry, you need to build them locally and load them into your KinD cluster. Note that `app.yaml` now includes `imagePullPolicy: IfNotPresent` for these deployments to ensure Kubernetes uses your local images.

```bash
# Build the backend API image
docker build -t backend-api:latest ./backend

# Build the frontend web app image
docker build -t frontend-web:latest ./frontend

# Load the images into the KinD cluster
# IMPORTANT: Replace <your-cluster-name> with the actual name of your KinD cluster (e.g., 'kind', 'sandbox', 'work-projects').
kind load docker-image backend-api:latest --name <your-cluster-name>
kind load docker-image frontend-web:latest --name <your-cluster-name>
```

### 3. Deploy the NGINX Ingress Controller

With the cluster running, deploy the NGINX Ingress controller. This step is crucial for the Ingress resource in `app.yaml` to work.

```bash
kubectl apply -f ingress.yaml
```

Wait a few moments for the ingress controller pods to start in the `ingress-nginx` namespace. You can check their status with:
```bash
kubectl get pods -n ingress-nginx
```

### 4. Deploy the Application

Once the ingress controller is running, deploy the sample application:

```bash
kubectl apply -f app.yaml
```

This will create the `demo-app` namespace and all the associated resources (Deployments, Services, and Ingress). New pods will be created based on the updated `app.yaml` with `imagePullPolicy: IfNotPresent`.

## Accessing the Application

### A) Via NodePort

The frontend service is exposed as a `NodePort` on port `30080`. You can access the web application at:

[http://localhost:30080](http://localhost:30080)

### B) Via Ingress (Recommended)

The Ingress resource is configured to route traffic based on the hostname `my-app.local`. To make this hostname resolve to your local machine, add the following entry to your `/etc/hosts` file:

```
127.0.0.1 my-app.local
```

Now you can access:

-   **Frontend**: [http://my-app.local](http://my-app.local)
-   **Backend API**: [http://my-app.local/api/hello](http://my-app.local/api/hello)

Inside the frontend, you can click the "Fetch from Backend" button to test the communication between the frontend and backend services.

## Cleanup

To delete the cluster and all its resources, run:

```bash
kind delete cluster
```
