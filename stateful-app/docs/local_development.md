# Running the Application Locally

Follow these steps to set up and run the application on your local machine:

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

5.  **Run the application**:
    ```bash
    python3 app.py
    ```

6.  **Access the endpoint**:
    Open your web browser or use a tool like `curl` to access:
    [http://127.0.0.1:5001/](http://127.0.0.1:5001/)
