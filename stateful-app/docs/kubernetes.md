# Deploying to Kubernetes

Kubernetes deployment files are provided in the `k8s/` directory. The new setup includes a MariaDB database and the stateful application.

The deployment includes:
- A `Secret` to store MariaDB credentials.
- A `PersistentVolumeClaim` to provide persistent storage for the MariaDB data.
- A `Deployment` and `Service` for MariaDB.
- A `Deployment` and `Service` for the stateful application.
- `liveness` and `readiness` probes for both the application and the database.

1.  **Rebuild your Docker image**:
    ```bash
    cd app
    docker build -t stateful-app:latest .
    cd ..
    ```

2.  **Ensure your Docker image is available to your cluster.**
    If you are using a local cluster (like Minikube or OrbStack), you can often use the image you built locally. For Minikube, you can load your local image directly into the cluster's Docker daemon:
    ```bash
    minikube image load stateful-app:latest
    ```
    If you are using a cloud-based Kubernetes cluster, you will need to push your image to a container registry and update the `image` field in `k8s/stateful-deployment.yaml`.

3.  **Navigate to the Kubernetes directory**:
    ```bash
    cd k8s
    ```

4.  **Apply the Kubernetes configuration**:
    ```bash
    kubectl apply -f stateful-deployment.yaml
    ```
    This will create all the necessary resources for the stateful application and the MariaDB database.

5.  **Access the application**:
    The service type is `LoadBalancer`. Find the external IP with:
    ```bash
    kubectl get svc stateful-app-service-lb
    ```
    You can then access the application at `http://<EXTERNAL-IP>:80`.

6.  **Access the requests endpoint**:
    To see the last 10 requests, you can access `http://<EXTERNAL-IP>:80/requests`.