import json
from flask import Flask, jsonify
from src.dbconnection import fetch_latest_data
from src.prediction import predict_next_value
from src.randomdata import generate_mining_data
import sys
from datetime import datetime, timezone
# Disable output buffering to ensure prints appear immediately
sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Python script started...", flush=True)

app.run()


app = Flask(__name__)

@app.route("/")
def home():
    return "  hello !" #Python App Running on Port 3009!

@app.route("/sensor-data", methods=["GET"])
def predict():      
    """Manually trigger prediction via API"""
    try:
        print("\n Manual Prediction Triggered...")
        predictions = predict_next_value()

        if not predictions:
            return jsonify({"error": "No predictions available"}), 400
        
        print("\n Predictions:")
        for key, value in predictions.items():
            print(f"   {key}: {value:.2f}")

        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(" Starting Data Ingestion and Prediction Service...")

    # Fetch & store data ONCE at startup
    print("\n Generating and storing new sensor data...")
    data = generate_mining_data()
    print(f" Generated Data: {json.dumps(data, indent=2)}")
    
    print("\n Fetching latest data from InfluxDB...")
    latest_data = fetch_latest_data()

    if not latest_data:
        print(" No new data found in InfluxDB! Skipping initial prediction.")
    else:
        print(f" Latest Data: {latest_data}")

        # Run predictions ONCE at startup
        print("\n Running Predictions...")
        predictions = predict_next_value()

        if predictions:
            print("\n Predictions:")
            for key, value in predictions.items():
                print(f"   {key}: {value:.2f}")
        else:
            print(" Prediction failed. No valid data.")

    # Start Flask server
    app.run(host="0.0.0.0", port=3009, debug=True)