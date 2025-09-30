import random
import pytz
import time
import schedule
from datetime import datetime, timezone
from src.dbconnection import get_mariadb_connection  # Your DB connection helper

# Generate sensor data for one insert
def generate_sensor_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return

    try:
        cursor = conn.cursor()
        ist = pytz.timezone("Asia/Kolkata")
        # Get current UTC time and format as ISO 8601 with Z
        timestamp = datetime.now(ist).strftime("%Y-%m-%dT%H:%M:%SZ")
        device_id = random.choice(["D8", "D9"])
        equipment_name = None
        latitude = 20.413320
        longitude = 81.071180
        gps_status = None
        z_axis = random.choice([0, 1, 2])
        pitch = random.choice([10, 15, 20, 30])
        roll = random.choice([0, 10])
        movement = None
        fuel_consumption = None
        avg_gradient = None

        query = """
            INSERT INTO realtime_sensor_data (
                device_id, timestamp, equipment_name, latitude, longitude,
                gps_status, z_axis, pitch, roll, movement,
                fuel_consumption_l_per_100km, avg_gradient
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            device_id, timestamp, equipment_name, latitude, longitude,
            gps_status, z_axis, pitch, roll, movement,
            fuel_consumption, avg_gradient
        ))

        conn.commit()
        print(f"✅ Inserted data for {device_id} at {timestamp}")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()


# Schedule the insert every 3 minutes
schedule.every(3).minutes.do(generate_sensor_data)

# Run once immediately
generate_sensor_data()

while True:
    schedule.run_pending()
    time.sleep(1)
