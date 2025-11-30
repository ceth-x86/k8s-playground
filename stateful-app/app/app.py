import os
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

import mariadb
import mariadb.cursors
from flask import Flask, request, Response

app = Flask(__name__)

# --- Configuration ---
# Database connection details from environment variables
DB_HOST: Optional[str] = os.environ.get('DB_HOST')
DB_USER: Optional[str] = os.environ.get('DB_USER')
DB_PASSWORD: Optional[str] = os.environ.get('DB_PASSWORD')
DB_NAME: Optional[str] = os.environ.get('DB_NAME')

# --- Database Operations ---

def get_db_connection() -> Optional[mariadb.Connection]:
    """Establishes and returns a connection to the MariaDB database."""
    try:
        if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
            print("Database environment variables are not fully set.")
            return None
        
        conn = mariadb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

def create_requests_table_if_not_exists() -> None:
    """Creates the 'requests' table in the database if it does not already exist."""
    conn: Optional[mariadb.Connection] = get_db_connection()
    if conn:
        cursor: mariadb.cursors.Cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    request_time DATETIME,
                    ip_address VARCHAR(255)
                )
            """)
            conn.commit()
        except mariadb.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

# Initialize database table on startup
create_requests_table_if_not_exists()

# --- Request Logging ---

@app.before_request
def log_incoming_request() -> None:
    """
    Logs details of incoming requests to the database, excluding health checks
    and the /requests endpoint itself.
    """
    # Do not log requests to health check or the requests display endpoint
    if request.path in ['/healthz', '/readyz', '/requests']:
        return

    conn: Optional[mariadb.Connection] = get_db_connection()
    if conn:
        cursor: mariadb.cursors.Cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO requests (request_time, ip_address) VALUES (%s, %s)",
                (datetime.now(), request.remote_addr)
            )
            conn.commit()
        except mariadb.Error as e:
            print(f"Error logging request: {e}")
        finally:
            conn.close()

# --- Routes ---

@app.route("/")
def get_current_datetime_route() -> Dict[str, str]:
    """
    Returns the current date and time.
    """
    current_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_datetime": current_time}

@app.route("/requests")
def get_last_10_requests_route() -> Tuple[Dict[str, Any], int]:
    """
    Retrieves and returns the last 10 logged requests from the database.
    """
    conn: Optional[mariadb.Connection] = get_db_connection()
    if conn:
        cursor: mariadb.cursors.Cursor = conn.cursor()
        try:
            cursor.execute("SELECT request_time, ip_address FROM requests ORDER BY request_time DESC LIMIT 10")
            # Fetch all rows and format them into a list of dictionaries
            requests_data = [{"request_time": str(row[0]), "ip_address": row[1]} for row in cursor.fetchall()]
            return {"requests": requests_data}, 200
        except mariadb.Error as e:
            print(f"Error retrieving requests: {e}")
            return {"error": "Error retrieving requests from database"}, 500
        finally:
            conn.close()
    return {"error": "Could not connect to database"}, 500

@app.route("/healthz")
def healthz_route() -> Tuple[str, int]:
    """
    Liveness probe endpoint. Always returns "OK".
    """
    return "OK", 200

@app.route("/readyz")
def readyz_route() -> Tuple[str, int]:
    """
    Readiness probe endpoint. Checks database connectivity.
    """
    conn: Optional[mariadb.Connection] = get_db_connection()
    if conn:
        conn.close()
        return "OK", 200
    else:
        return "Database not ready", 503

# --- Application Entry Point ---

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
