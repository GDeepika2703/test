import mysql.connector as mariadb
import pandas as pd
def get_mariadb_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="vistaarnksh",
            host="104.154.141.198",
            port=3306,
            database="project",
        )
        return conn
    except mariadb.Error as e:
        print(f" Error connecting to MariaDB: {e}")
        return None
def fetch_latest_data():
    conn = get_mariadb_connection()
    if not conn:
        return None
    try:
        query = "SELECT * FROM continuous_miner ORDER BY timestamp DESC LIMIT 10"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f" Error fetching latest data: {e}")
        return None
    finally:
        conn.close()