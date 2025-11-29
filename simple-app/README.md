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

- **[How LoadBalancer Works with OrbStack](./docs/internals/loadbalancer_orb.md)**: An explanation of how `LoadBalancer` services are routed in a local OrbStack environment.
