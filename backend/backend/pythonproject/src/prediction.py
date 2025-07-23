
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import sys
import os
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dbconnection import get_influxdb_client

client = get_influxdb_client()

def fetch_data_from_influx():
   # print(" Fetching data from InfluxDB...")
    query = 'SELECT * FROM "real_time_data" ORDER BY time DESC LIMIT 10'
    result = client.query(query)
    
    data = list(result.get_points())

    if not data:
        print(" No data found in InfluxDB! ")
        return None
    
    df = pd.DataFrame(data)
    print(" Data fetched from InfluxDB! ")                         #
    #print(df)          #printing update random values (limit-10)   //
    return df
 
#stroring prediction values into influxdb
def write_prediction_to_influx(data):
    client = get_influxdb_client()

    if not client:
        print("❌ Could not connect to InfluxDB to write data.")
        return

    json_body = [
        {
            "measurement": "predicted_data",  # You can name this as needed
            "time": data["timestamp"],
            "fields": {
                "co2": float(data["co2"]),
                "o2": float(data["o2"]),
                "humidity": float(data["humidity"])
            }
        }
    ]

    try:
        client.write_points(json_body)
        print("Prediction data written to InfluxDB!")
    except Exception as e:
        print(f"Failed to write to InfluxDB: {e}")
 



def predict_next_value():
    df = fetch_data_from_influx()
    if df is None:
        print(" No data available for prediction!")                   #
        return {}

    predictions = {}
    # Convert timestamps properly
    df['time_numeric'] = pd.to_datetime(df['time']).astype('int64') // 10**9  # Convert to seconds
    df['time_numeric'] = (df['time_numeric'] - df['time_numeric'].min()) / 60  # Normalize to minutes

    print(" Running predictions...")

    for feature in ["CO2", "O2", "Humidity"]:
        if feature not in df.columns:
            print(f" Column '{feature}' is missing in fetched data!")
            continue

        time_steps = df[['time_numeric']]
        values = df[[feature]]

        # Use MinMaxScaler instead of StandardScaler
        scaler_x = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_scaled = scaler_x.fit_transform(time_steps)
        y_scaled = scaler_y.fit_transform(values)

        model = LinearRegression()
        model.fit(X_scaled, y_scaled)

        # Predict next step using median time step size
        time_step_size = df['time_numeric'].diff().median()
        next_time_value = df['time_numeric'].iloc[-1] + time_step_size
        next_time = pd.DataFrame([[next_time_value]], columns=['time_numeric'])
        next_time_scaled = scaler_x.transform(next_time)

        prediction_scaled = model.predict(next_time_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled)

        # Clip values to realistic sensor ranges
        prediction = np.clip(prediction, 0, 5000)  # Adjust range as needed

        predictions[feature.lower()] = round(float(prediction[0][0]),2)

        #print(f" Predicted {feature} for next step: {prediction[0][0]:.2f}")                #

        final_json = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "co2": predictions.get("co2"),
        "o2": predictions.get("o2"),
        "humidity": predictions.get("humidity")
        }
        #print("📦 Final Prediction JSON:", final_json)
        
    print(json.dumps(final_json))
    write_prediction_to_influx(final_json)


    return final_json

     
    #return predictions

predict_next_value()