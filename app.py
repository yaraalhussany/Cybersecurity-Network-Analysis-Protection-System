import csv
import os
import subprocess
import sys
import joblib 
import numpy as np 
import pandas as pd # We need Pandas to format the data for the models!

from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET  = os.path.join(BASE_DIR, "dataset.csv")

# --- 1. LOAD MODELS ONCE AT STARTUP ---
print("Loading ML Models...")
rf_model = joblib.load(os.path.join(BASE_DIR, 'random_forest_network_model.pkl'))
xgb_model = joblib.load(os.path.join(BASE_DIR, 'xgboost_tuned_network_model.pkl'))
print("Models Loaded Successfully! 🚀")

# These MUST exactly match the 15 column names the models were trained on
LABELS = [
    "Bwd Packet Length Max", "Bwd Packet Length Mean", "Bwd Packet Length Std",
    "Flow IAT Max", "Fwd IAT Std", "Fwd IAT Max", "Max Packet Length",
    "Packet Length Mean", "Packet Length Std", "Packet Length Variance",
    "Average Packet Size", "Avg Bwd Segment Size", "Idle Mean", "Idle Max", "Idle Min"
]

def read_latest_row():
    """Return the last row of dataset.csv as a dict, and run ML prediction."""
    if not os.path.exists(DATASET):
        return None
    with open(DATASET, newline="") as f:
        rows = list(csv.reader(f))
    
    rows = [r for r in rows if any(cell.strip() for cell in r)]
    if not rows:
        return None
    last = rows[-1]
    
    # 1. Map CSV data to Labels
    row_data = {LABELS[i]: last[i] for i in range(min(len(LABELS), len(last)))}
    
    # 2. Extract exactly the 15 features as floats for the ML model
    try:
        features = [float(row_data[label]) for label in LABELS]
        
        # 3. Create a 1-row DataFrame so the models see the exact column names they expect
        features_df = pd.DataFrame([features], columns=LABELS)
        
        # 4. Get Predictions
        rf_pred = rf_model.predict(features_df)[0]
        xgb_pred = xgb_model.predict(features_df)[0]
        
        # 5. Ensemble Logic (FIXED: > 0 catches ALL attacks)
        if xgb_pred > 0:
            row_data["Attack Status"] = f"🔴 HACKER DETECTED! (Class {xgb_pred})"
        elif rf_pred > 0 and xgb_pred == 0:
            row_data["Attack Status"] = f"🟠 SUSPICIOUS (RF Warning Class {rf_pred})"
        else:
            row_data["Attack Status"] = "🟢 NORMAL TRAFFIC"
            
    except ValueError:
        # Failsafe in case main.py writes a bad row (like text instead of numbers)
        row_data["Attack Status"] = "🟡 Data Error - Could not parse features"
    except Exception as e:
        row_data["Attack Status"] = f"🟡 Model Error: {str(e)}"

    return row_data


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/data")
def data():
    """Return current dataset values as JSON."""
    row = read_latest_row()
    if row is None:
        return jsonify({"error": "No data yet. Click Refresh."}), 404
    return jsonify(row)


@app.route("/refresh")
def refresh():
    """Run main.py then return the freshly computed row as JSON."""
    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return jsonify({"error": result.stderr or "main.py failed"}), 500

        row = read_latest_row()
        if row is None:
            return jsonify({"error": "main.py ran but no data was written"}), 500
        return jsonify(row)

    except subprocess.TimeoutExpired:
        return jsonify({"error": "main.py timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)