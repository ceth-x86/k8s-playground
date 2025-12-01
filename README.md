# mk8s Project

This project contains examples of Kubernetes deployments and scaling.

## Sub-projects

*   **[Simple Application](./simple-app/README.md)**: A basic Flask application deployed to Kubernetes.
*   **[Scaling Application](./scaling/README.md)**: A Flask application demonstrating horizontal scaling and Prometheus integration.
*   **[Ingress Application](./ingress/README.md)**: Demonstrates how to use Kubernetes Ingress to route traffic to multiple applications.
*   **[Stateful Application](./stateful-app/README.md)**: A Flask application with MariaDB integration, request logging, and a dedicated endpoint to view recent requests.
*   **[Background Processing Application](./background-processing/README.md)**: A Flask application extended with Redis for background job management, including a Kubernetes Job and CronJob.
