# Containerizing with Docker

To containerize this application, you can use the provided `Dockerfile`.

1.  **Navigate to the app directory**:
    ```bash
    cd app
    ```
2.  **Build the Docker image**:
    ```bash
    docker build -t simple-app:latest .
    ```

3.  **Run the Docker container**:
    ```bash
    docker run -p 5001:5001 simple-app:latest
    ```
    You can then access the application at [http://localhost:5001](http://localhost:5001).
