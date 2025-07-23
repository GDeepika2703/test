#connecting to influxDB

from influxdb import InfluxDBClient
import pandas as pd
import os 

INFLUXDB_HOST = "34.28.117.27"  # Your VM's IP
INFLUXDB_PORT = 8086  # Default InfluxDB port
INFLUXDB_USER = "root"
INFLUXDB_PASSWORD = "vistaarnksh"
INFLUXDB_DB = "old_mining_data"  # Replace with your actual database name

def get_influxdb_client():
    try:
        client = InfluxDBClient(
            host=INFLUXDB_HOST, 
            port=INFLUXDB_PORT, 
            username=INFLUXDB_USER, 
            password=INFLUXDB_PASSWORD, 
            database=INFLUXDB_DB
        )
        
        # Check if connected
        if client.ping():
            #print(" Successfully connected to InfluxDB!")                           //
            return client
        else:
            print(" Connection to InfluxDB failed!")
            return None
    except Exception as e:
        print(f" Error: {e}")
        return None
    




def fetch_latest_data():
    """Fetch the latest sensor data from InfluxDB."""
    client = get_influxdb_client()
    if client:
        query = f'SELECT * FROM environmental ORDER BY time DESC LIMIT 10'
        result = client.query(query)
        points = list(result.get_points())
        if points:
            df = pd.DataFrame(points)
            return df
        else:
            print(" No data found in InfluxDB.")
            return None
    return None