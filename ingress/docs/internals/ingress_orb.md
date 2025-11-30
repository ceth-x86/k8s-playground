# How Ingress Works with OrbStack

> How does the OS route an Ingress hostname to localhost?

That's a fantastic question that gets to the core of how local Kubernetes solutions like OrbStack work their magic. Here's a step-by-step breakdown of how the request is routed:

1.  **Ingress Controller**: When you create an `Ingress` resource, you are defining a set of rules for routing external HTTP/S traffic to services within your cluster. For these rules to work, you need an Ingress Controller. OrbStack comes with a built-in Ingress Controller (based on Nginx) that is responsible for reading these rules and managing traffic.

2.  **DNS and Hostname Resolution (The "Magic")**: This is the key part. When you define a hostname in your Ingress resource (e.g., `simple-app.local`), OrbStack automatically updates your Mac's `/etc/hosts` file (or an equivalent internal DNS service). It adds an entry that maps this hostname to an IP address managed by OrbStack. This IP address is the entry point to the Ingress Controller.

3.  **The Request Journey**:
    *   **Browser to Host OS**: You type `http://simple-app.local` into your browser. Your Mac's OS looks up this hostname and, thanks to the entry OrbStack created, resolves it to the Ingress Controller's IP address.
    *   **Host OS to OrbStack VM**: Your Mac routes the request to the OrbStack VM where the Ingress Controller is running.
    *   **Inside the Kubernetes Cluster (Ingress Controller)**: The request hits the Ingress Controller. The controller inspects the request's hostname (`simple-app.local`) and path. It then looks at the `Ingress` resource rules you defined to determine which `Service` to forward the traffic to.
    *   **Ingress to Service**: The Ingress Controller forwards the request to the correct `Service` (e.g., `simple-app-service`).
    *   **Service to Pod**: The `Service` then forwards the request to one of the healthy pods selected by your service (e.g., `simple-app-deployment-xxxx`). The request is sent to the `targetPort` specified in your service, which is `5001`.
    *   **Application Response**: Your Flask application running inside the pod receives the request on port `5001`, processes it, and sends the response back along the same path.

So, in short: **OrbStack makes your computer treat `simple-app.local` (or any hostname in your Ingress) as a "local" address that points directly to its internal Ingress Controller.** This allows you to use standard hostnames and HTTP/S routing for local development, which is a more flexible and realistic setup than using `LoadBalancer` IPs.