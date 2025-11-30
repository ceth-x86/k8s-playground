# Running the Application Locally

Follow these steps to set up and run the application on your local machine. This setup requires a running MariaDB instance.

### 1. Set up MariaDB

You need a MariaDB server running locally. You can use Docker to easily start one:

```bash
docker run -d --name some-mariadb -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=mydatabase \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=password \
  mariadb:10.5
```

This will start a MariaDB container with the necessary database and user created.

### 2. Set up the Application

1.  **Navigate to the app directory**:
    ```bash
    cd app
    ```
2.  **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set environment variables**:
    The application needs to know how to connect to the database.
    ```bash
    export DB_HOST=127.0.0.1
    export DB_USER=user
    export DB_PASSWORD=password
    export DB_NAME=mydatabase
    ```

6.  **Run the application**:
    ```bash
    python3 app.py
    ```

7.  **Access the endpoints**:
    *   **Current Time**: [http://127.0.0.1:5001/](http://127.0.0.1:5001/)
    *   **Last 10 Requests**: [http://127.0.0.1:5001/requests](http://127.0.0.1:5001/requests)