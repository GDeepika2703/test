# Updated dummy.py code

'''import random
import time
import schedule
import math
from datetime import datetime, timedelta
import pytz
import mysql.connector
from src.dbconnection import get_mariadb_connection

# Indian timezone
ist = pytz.timezone("Asia/Kolkata")

# Helper → Generate random GPS around base location
def random_gps(base_lat=12.9716, base_lng=77.5946):
    return (
        round(base_lat + (random.random() - 0.5) * 0.12, 6),
        round(base_lng + (random.random() - 0.5) * 0.12, 6)
    )

def generate_all_sensor_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return

    try:
        cursor = conn.cursor()
        base_timestamp = datetime.now(ist)

        # Common insert query with all 66 columns
        query = """
            INSERT INTO dummy (
                device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                water_level_m, seismic_activity_hz, noise_pollution_db, equipment_name, fuel_consumption_l_per_100km,
                temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                tyre_pressure, battery_status, load_weight, latitude, longitude,
                worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                total_hours, reining, motor, date_of_fitment, remaining_hours,
                active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                drills_utilization, dust, z_axis
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        # Generate data for exactly 1 Excavator
        latitude, longitude = random_gps()
        offset = timedelta(seconds=random.uniform(0, 59))  # Random offset within the minute
        timestamp = (base_timestamp + offset).strftime("%Y-%m-%d %H:%M:%S")
        air_quality = random.randint(0, 500)
        co_ppm = round(random.uniform(0.0, 9.0), 2)
        development_meters = round(random.uniform(0, 500), 2)
        active_blast_areas = round(random.uniform(0, 5), 2)
        man_down_alert = bool(random.choice([0, 1]))  # Convert to boolean
        cursor.execute(query, (
            "d3", timestamp, air_quality, co_ppm, random.randint(200, 500), round(random.uniform(17.0, 22.0), 2), random.randint(40, 90),
            round(random.uniform(0.0, 5.0), 2), round(random.uniform(0.1, 10.0), 2), random.randint(30, 120), "Excavator", round((100/7) * (1 + 1.5 * math.sin(math.radians(random.uniform(-20, 20)))), 2),
            round(random.uniform(70, 90), 1), round(random.randint(1300, 1600)), random.randint(75, 95), random.randint(300, 700), random.randint(100, 150),
            random.randint(30, 45), random.randint(80, 100), random.randint(1000, 2000), latitude, longitude,
            f"W{random.randint(1, 10)}", random.randint(70, 100), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), man_down_alert,
            round(random.uniform(50.0, 100.0), 2), round(random.uniform(200.0, 300.0), 2), round(random.uniform(60.0, 120.0), 2), round(random.uniform(0.0, 100.0), 2),
            round(random.uniform(1000.0, 2000.0), 2), round(random.uniform(300.0, 500.0), 2), random.choice(["Normal", "Fault"]), random.randint(0, 5),
            round(random.uniform(10.0, 100.0), 2), round(random.uniform(2500.0, 3500.0), 2), round(random.uniform(30, 100), 2), round(random.uniform(100.0, 160.0), 2),
            random.choice(["Normal", "High", "Warning"]), random.choice(["Normal", "Fault"]), random.choice(["Normal", "Fault"]), random.choice(["No faults", "Overheat warning", "Hydraulic pressure drop", "Motor overload detected"]),
            round(random.uniform(200.0, 500.0), 2), round(random.uniform(70.0, 120.0), 2), round(random.uniform(1.0, 6.0), 3), round(random.uniform(60.0, 100.0), 2), round(random.uniform(20.0, 80.0), 2),
            random.randint(500, 3000), round(random.uniform(0.0, 100.0), 2), random.choice(["Motor_A", "Motor_B", "Motor_C"]), (datetime.now() - timedelta(days=random.randint(100, 1000))).date(), random.randint(50, 1000),
            active_blast_areas, development_meters, round(random.uniform(0, 1000), 2), round(random.uniform(0, 10000), 2), round(random.uniform(50, 500), 2),
            round(random.uniform(70, 100), 2), round(random.uniform(0, 10), 2), round(random.uniform(50, 100), 2), round(random.uniform(50, 100), 2),
            round(random.uniform(50, 100), 2), round(random.uniform(0, 500), 2), round(random.uniform(-30, 30))
        ))

        # Generate data for exactly 5 Haulers
        for i in range(5):  # Explicitly loop 5 times for 5 haulers
            latitude, longitude = random_gps()
            offset = timedelta(seconds=random.uniform(0, 59))  # Random offset within the minute
            timestamp = (base_timestamp + offset).strftime("%Y-%m-%d %H:%M:%S")
            air_quality = random.randint(0, 500)
            co_ppm = round(random.uniform(0.0, 9.0), 2)
            development_meters = round(random.uniform(0, 500), 2)
            active_blast_areas = round(random.uniform(0, 5), 2)
            man_down_alert = bool(random.choice([0, 1]))  # Convert to boolean
            z_axis = round(random.uniform(-30, 30), 2)  # Generate z_axis value
            cursor.execute(query, (
                "d3", timestamp, air_quality, co_ppm, random.randint(200, 500), round(random.uniform(17.0, 22.0), 2), random.randint(40, 90),
                round(random.uniform(0.0, 5.0), 2), round(random.uniform(0.1, 10.0), 2), random.randint(30, 120), f"Hauler-{i+1}", round((100/7) * (1 + 1.5 * math.sin(math.radians(z_axis))), 2),
                round(random.uniform(70, 90), 1), round(random.randint(1300, 1600)), random.randint(75, 95), random.randint(300, 700), random.randint(100, 150),
                random.randint(30, 45), random.randint(80, 100), random.randint(1000, 2000), latitude, longitude,
                f"W{random.randint(1, 10)}", random.randint(70, 100), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), man_down_alert,
                round(random.uniform(50.0, 100.0), 2), round(random.uniform(200.0, 300.0), 2), round(random.uniform(60.0, 120.0), 2), round(random.uniform(0.0, 100.0), 2),
                round(random.uniform(1000.0, 2000.0), 2), round(random.uniform(300.0, 500.0), 2), random.choice(["Normal", "Fault"]), random.randint(0, 5),
                round(random.uniform(10.0, 100.0), 2), round(random.uniform(2500.0, 3500.0), 2), round(random.uniform(30, 100), 2), round(random.uniform(100.0, 160.0), 2),
                random.choice(["Normal", "High", "Warning"]), random.choice(["Normal", "Fault"]), random.choice(["Normal", "Fault"]), random.choice(["No faults", "Overheat warning", "Hydraulic pressure drop", "Motor overload detected"]),
                round(random.uniform(200.0, 500.0), 2), round(random.uniform(70.0, 120.0), 2), round(random.uniform(1.0, 6.0), 3), round(random.uniform(60.0, 100.0), 2), round(random.uniform(20.0, 80.0), 2),
                random.randint(500, 3000), round(random.uniform(0.0, 100.0), 2), random.choice(["Motor_A", "Motor_B", "Motor_C"]), (datetime.now() - timedelta(days=random.randint(100, 1000))).date(), random.randint(50, 1000),
                active_blast_areas, development_meters, round(random.uniform(0, 1000), 2), round(random.uniform(0, 10000), 2), round(random.uniform(50, 500), 2),
                round(random.uniform(70, 100), 2), round(random.uniform(0, 10), 2), round(random.uniform(50, 100), 2), round(random.uniform(50, 100), 2),
                round(random.uniform(50, 100), 2), round(random.uniform(0, 500), 2), z_axis
            ))

        conn.commit()
        print(f"✅ Inserted 1 Excavator and 5 Haulers at {base_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()

# Retrieve last 5 z_axis values for each Hauler
def get_z_axis_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        # Query to get all z_axis values for each Hauler, ordered by timestamp
        query = """
            SELECT timestamp, z_axis, equipment_name
            FROM dummy
            WHERE equipment_name LIKE 'Hauler%'
            ORDER BY equipment_name, timestamp DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        # Group data by equipment_name
        hauler_data = {}
        for row in data:
            equipment = row['equipment_name']
            if equipment not in hauler_data:
                hauler_data[equipment] = []
            hauler_data[equipment].append({
                'timestamp': row['timestamp'],
                'z_axis': float(row['z_axis'])
            })
        
        # Ensure we have at most 5 entries per Hauler, sorted by timestamp DESC
        for equipment in hauler_data:
            hauler_data[equipment] = sorted(hauler_data[equipment], key=lambda x: x['timestamp'], reverse=True)[:5]
        
        return hauler_data

    except Exception as e:
        print(f"❌ Error retrieving z_axis data: {e}")
        return None
    finally:
        conn.close()

# Generate 5 charts, one for each Hauler
def generate_z_axis_charts():
    hauler_data = get_z_axis_data()
    if not hauler_data:
        print("No z_axis data retrieved from the database.")
        return

    baseline_kmpl = 7
    FC0 = 100 / baseline_kmpl
    k = 1.5

    for equipment_name in sorted(hauler_data.keys()):  # Sort to ensure consistent order (Hauler-1 to Hauler-5)
        data = hauler_data[equipment_name]
        if not data:
            print(f"No data for {equipment_name}.")
            continue

        # Extract z_axis values and timestamps
        z_axis_values = [row['z_axis'] for row in data]
        timestamps = [row['timestamp'].strftime('%H:%M:%S') for row in data]

        # Calculate gradients (%) and fuel consumption (L/100km)
        gradients = [math.sin(math.radians(z)) * 100 for z in z_axis_values]
        fuel_consumption = [FC0 * (1 + k * math.sin(math.radians(z))) for z in z_axis_values]

        # Calculate averages
        avg_fuel = sum(fuel_consumption) / len(fuel_consumption) if fuel_consumption else 0
        avg_gradient = sum(gradients) / len(gradients) if gradients else 0

        # Labels (simple indices)
        labels = [str(i + 1) for i in range(len(z_axis_values))]

        # Generate Chart.js configuration
        chart = {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Fuel Consumption (L/100km)",
                        "data": [round(fc, 2) for fc in fuel_consumption],
                        "borderColor": "#36a2eb",
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "fill": False,
                        "borderWidth": 2,
                        "pointRadius": 2
                    },
                    {
                        "label": "Gradient (%)",
                        "data": [round(g, 2) for g in gradients],
                        "borderColor": "#32cd32",
                        "backgroundColor": "rgba(50, 205, 50, 0.2)",
                        "fill": False,
                        "borderWidth": 2,
                        "pointRadius": 4,
                        "yAxisID": "y1"
                    },
                    {
                        "label": f"Average Fuel ({round(avg_fuel, 2)} L/100km)",
                        "data": [round(avg_fuel, 2)] * len(labels),
                        "borderColor": "orange",
                        "backgroundColor": "rgba(255, 165, 0, 0.2)",
                        "fill": False,
                        "borderWidth": 2,
                        "pointRadius": 0,
                        "borderDash": [5, 5]
                    },
                    {
                        "label": f"Average Gradient ({round(avg_gradient, 2)}%)",
                        "data": [round(avg_gradient, 2)] * len(labels),
                        "borderColor": "green",
                        "backgroundColor": "rgba(0, 128, 0, 0.2)",
                        "fill": False,
                        "borderWidth": 2,
                        "pointRadius": 0,
                        "borderDash": [5, 5],
                        "yAxisID": "y1"
                    }
                ]
            },
            "options": {
                "scales": {
                    "y": {
                        "beginAtZero": False,
                        "title": {
                            "display": True,
                            "text": "Fuel (L/100km)"
                        }
                    },
                    "y1": {
                        "position": "right",
                        "beginAtZero": False,
                        "title": {
                            "display": True,
                            "text": "Gradient (%)"
                        },
                        "grid": {
                            "drawOnChartArea": False
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Sample Index"
                        }
                    }
                },
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{equipment_name} Fuel & Gradient Overview"
                    },
                    "legend": {
                        "display": True
                    },
                    "annotation": {
                        "annotations": [{
                            "type": "label",
                            "xValue": labels[-1],
                            "yValue": round(fuel_consumption[-1], 2) if fuel_consumption else 0,
                            "content": f"{round(fuel_consumption[-1], 2) if fuel_consumption else 0} L/100km",
                            "color": "#36a2eb",
                            "position": "end"
                        }]
                    }
                }
            }
        }

        # Output the chart
        #print(f"Chart for {equipment_name}:")
        #print("```chartjs")
        #print(chart)
        #print("```")

# Schedule tasks
schedule.every(1).minutes.do(generate_all_sensor_data)
schedule.every(1).minutes.do(generate_z_axis_charts)  # Update charts every minute

# Run once immediately
generate_all_sensor_data()
generate_z_axis_charts()

while True:
    schedule.run_pending()
    time.sleep(1)'''
    
import random
import time
import schedule
import math
from datetime import datetime, timedelta
import pytz
import mysql.connector
from src.dbconnection import get_mariadb_connection

# Indian timezone
ist = pytz.timezone("Asia/Kolkata")

def generate_all_sensor_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return

    try:
        cursor = conn.cursor()
        base_timestamp = datetime.now(ist)

        # Single-line INSERT query with 65 columns (excluding id, latitude, longitude, equipment_name, z_axis)
        query = "INSERT INTO dummy (device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity, water_level_m, seismic_activity_hz, noise_pollution_db, fuel_consumption_l_per_100km, temperature, pressure, motor_load, machine_runtime, fuel_consumption, tyre_pressure, battery_status, load_weight, worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert, battery_health, voltage, traction_motor_temp, pick_wear_monitoring, cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count, vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp, hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details, exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure, total_hours, reining, motor, date_of_fitment, remaining_hours, active_blast_areas, development_meters, production_meters, ore_mined, throughput, crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization, drills_utilization, dust, gradient, gradient_deg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Generate data for exactly 1 Excavator
        device_id = random.choice(['d1', 'd2', 'd4', 'd5'])  # Randomly select device_id
        offset = timedelta(seconds=random.uniform(0, 59))  # Random offset within the minute
        timestamp = (base_timestamp + offset).strftime("%Y-%m-%d %H:%M:%S")
        air_quality = random.randint(0, 500)
        co_ppm = round(random.uniform(0.0, 9.0), 2)
        development_meters = round(random.uniform(0, 500), 2)
        active_blast_areas = round(random.uniform(0, 5), 2)
        man_down_alert = bool(random.choice([0, 1]))  # Convert to boolean
        gradient_deg = round(random.uniform(-30, 30), 2)  # Use for gradient_deg
        gradient = round(math.sin(math.radians(gradient_deg)) * 100, 2)  # Calculate gradient (%)
        fuel_consumption_l_per_100km = round((100/7) * (1 + 1.5 * math.sin(math.radians(gradient_deg))), 2)  # Use gradient_deg
        cursor.execute(query, (device_id, timestamp, air_quality, co_ppm, random.randint(200, 500), round(random.uniform(17.0, 22.0), 2), random.randint(40, 90), round(random.uniform(0.0, 5.0), 2), round(random.uniform(0.1, 10.0), 2), random.randint(30, 120), fuel_consumption_l_per_100km, round(random.uniform(70, 90), 1), round(random.randint(1300, 1600)), random.randint(75, 95), random.randint(300, 700), random.randint(100, 150), random.randint(30, 45), random.randint(80, 100), random.randint(1000, 2000), f"W{random.randint(1, 10)}", random.randint(70, 100), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), round(random.uniform(0.0, 0.05), 2), man_down_alert, round(random.uniform(50.0, 100.0), 2), round(random.uniform(200.0, 300.0), 2), round(random.uniform(60.0, 120.0), 2), round(random.uniform(0.0, 100.0), 2), round(random.uniform(1000.0, 2000.0), 2), round(random.uniform(300.0, 500.0), 2), random.choice(["Normal", "Fault"]), random.randint(0, 5), round(random.uniform(10.0, 100.0), 2), round(random.uniform(2500.0, 3500.0), 2), round(random.uniform(30, 100), 2), round(random.uniform(100.0, 160.0), 2), random.choice(["Normal", "High", "Warning"]), random.choice(["Normal", "Fault"]), random.choice(["Normal", "Fault"]), random.choice(["No faults", "Overheat warning", "Hydraulic pressure drop", "Motor overload detected"]), round(random.uniform(200.0, 500.0), 2), round(random.uniform(70.0, 120.0), 2), round(random.uniform(1.0, 6.0), 3), round(random.uniform(60.0, 100.0), 2), round(random.uniform(20.0, 80.0), 2), random.randint(500, 3000), round(random.uniform(0.0, 100.0), 2), random.choice(["Motor_A", "Motor_B", "Motor_C"]), (datetime.now() - timedelta(days=random.randint(100, 1000))).date(), random.randint(50, 1000), active_blast_areas, development_meters, round(random.uniform(0, 1000), 2), round(random.uniform(0, 10000), 2), round(random.uniform(50, 500), 2), round(random.uniform(70, 100), 2), round(random.uniform(0, 10), 2), round(random.uniform(50, 100), 2), round(random.uniform(50, 100), 2), round(random.uniform(50, 100), 2), round(random.uniform(0, 500), 2), gradient, gradient_deg))

        conn.commit()
        print(f"✅ Inserted 1 Excavator with device_id {device_id} at {base_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()

# Schedule tasks
schedule.every(1).minutes.do(generate_all_sensor_data)

# Run once immediately
generate_all_sensor_data()

while True:
    schedule.run_pending()
    time.sleep(1)