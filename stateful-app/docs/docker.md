# Containerizing with Docker

To containerize this application, you can use the provided `Dockerfile`.

1.  **Navigate to the app directory**:
    ```bash
    cd app
    ```
2.  **Build the Docker image**:
    ```bash
    docker build -t stateful-app:latest .
    ```

3.  **Run the Docker container**:
    To run the container, you need to provide the database connection details as environment variables.
    ```bash
    docker run -p 5001:5001 \
      -e DB_HOST=<your_db_host> \
      -e DB_USER=<your_db_user> \
      -e DB_PASSWORD=<your_db_password> \
      -e DB_NAME=<your_db_name> \
      stateful-app:latest
    ```
    You can then access the application at [http://localhost:5001](http://localhost:5001).

    **Note**: You will need a running MariaDB instance accessible from the container.