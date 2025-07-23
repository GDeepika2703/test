import random
import time
import pandas as pd
import schedule
from src.dbconnection import get_influxdb_client
from datetime import datetime

# Connect to InfluxDB
client = get_influxdb_client()

def generate_mining_data(num_records=10):
    """Generate mining data and store in InfluxDB."""
    
    data_points = []

    for _ in range(num_records):
        timestamp = datetime.utcnow().isoformat()  # UTC format timestamp
        
        co2 = random.randint(2000, 5000)
        o2 = round(random.uniform(17, 22), 2)
        humidity = random.randint(40, 90)        

        # Create data point for InfluxDB
        data_point = {
            "measurement": "real_time_data",
            "time": timestamp,
            "fields": {
                "CO2": co2,
                "O2": o2,
                "Humidity": humidity
            }
        }

        data_points.append(data_point)

    # Store data in InfluxDB
    if client:
        try:
            client.write_points(data_points)
            print(f" Data stored in InfluxDB at {timestamp}") 
        except Exception as e:
            print(f" Error storing data: {e}")

# Run the function immediately at startup
generate_mining_data()

# Schedule the function to run every 1 minute
schedule.every(1).minutes.do(generate_mining_data)

while True:
    schedule.run_pending()
    time.sleep(60)  
