# Deploying to Kubernetes

Kubernetes deployment files are provided in the `k8s/` directory.

The deployment includes `liveness` and `readiness` probes, which Kubernetes uses to ensure the application is healthy and ready to receive traffic. It also includes resource `requests` and `limits` to manage CPU and memory allocation for the pods.

1.  **Rebuild your Docker image** to include the new health check endpoints (if you haven't already):
    ```bash
    cd app
    docker build -t simple-app:latest .
    cd .. 
    ```

2.  **Ensure your Docker image is available to your cluster.**
    If you are using a local cluster (like Minikube or OrbStack), you can often use the image you built locally. If you are using a cloud-based Kubernetes cluster, you will need to push your image to a container registry (like Docker Hub, GCR, or ECR) and update the `image` field in `k8s/deployment.yaml` accordingly.

    For Minikube, you can load your local image directly into the cluster's Docker daemon:
    ```bash
    minikube image load simple-app:latest
    ```

3.  **Navigate to the Kubernetes directory**:
    ```bash
    cd k8s
    ```

4.  **Apply the Kubernetes configuration**:
    ```bash
    kubectl apply -f deployment.yaml
    ```
    This will update the Deployment to use the new image (if applicable) and include the probes, along with the defined resource requests and limits.

5.  **Access the application**:
    Depending on the service type you are using (`NodePort` or `LoadBalancer`), the access method will differ. Please refer to the `deployment.yaml` file in the `k8s/` directory to see which service is active.

    *   **For `NodePort`**: Find the port with `kubectl get svc` and access `http://localhost:<NodePort>`.
    *   **For `LoadBalancer`**: Find the IP with `kubectl get svc` and access `http://<EXTERNAL-IP>:80`.
