#converting csv file into influxDB

from src.dbconnection import get_influxdb_client
import os
import pandas as pd


client = get_influxdb_client()


csvfile = r"C:\Naveen\PythonAndNodejs\pythonproject\src\environmental_monitoring_data.csv"


if os.path.exists(csvfile):
    df = pd.read_csv(csvfile)
    print("✅ CSV file loaded successfully!")
    print(df.head())  # Print first 5 rows
else:
    print(f"❌ CSV file not found at: {csvfile}")



df["timestamp"] = pd.to_datetime(df["timestamp"])


data_points = []
for _, row in df.iterrows():
    data_point = {
        "measurement": "environmental",
        "time": row["timestamp"].isoformat(),
        "fields": {
            "PM2.5": row["PM2.5 (µg/m³)"],
            "PM10": row["PM10 (µg/m³)"],
            "CH4": row["CH4 (ppm)"],
            "H2S": row["H2S (ppm)"],
            "CO": row["CO (ppm)"],
            "CO2": row["CO2 (ppm)"],
            "O2": row["O2 (%)"],
            "Humidity": row["Humidity (%)"],
            "Water_Level": row["Water Level (m)"],
            "Seismic_Activity": row["Seismic Activity (Richter)"],
            "Noise_Pollution": row["Noise Pollution (dB)"],
        },
        "tags": {
            "Hazard": row["Hazard Status"]
        }
    }

    data_points.append(data_point)



if client:
    try:
        client.write_points(data_points)
        print(" Data successfully inserted into InfluxDB!")
    except Exception as e:
        print(f"⚠️ Error inserting data: {e}")
else:
    print(" Could not connect to InfluxDB.")

