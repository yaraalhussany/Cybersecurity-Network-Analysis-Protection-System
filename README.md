# 🛡️ Real-Time Network Intrusion Detection Dashboard

An end-to-end Machine Learning pipeline and interactive web dashboard that monitors network traffic in real-time, extracts statistical flow features, and detects malicious attacks using a dual-engine ensemble of AI models.

## 📸 Project Dashboards

<img width="975" height="441" alt="image" src="https://github.com/user-attachments/assets/477fb9ec-a6ab-48f3-a507-65a8ea557fac" />

<img width="975" height="440" alt="image" src="https://github.com/user-attachments/assets/9d84d88e-1d4e-4a7f-b2e4-414903a67a08" />


## 🚀 Project Overview

This project simulates an enterprise-level Intrusion Detection System (IDS). It captures live network packets, processes them into 15 distinct flow-based features, and feeds them into a Machine Learning pipeline to identify anomalies and cyber attacks instantly.

### Key Features
* **Live Feature Extraction:** Captures packets and calculates statistical metrics (Max/Mean/Std of packet lengths, Inter-Arrival Times, etc.) on the fly.
* **Dual-Model ML Ensemble:** Utilizes a custom "Two-Key" verification system:
  * **Random Forest (The Paranoid Engine):** Highly robust, designed for high recall to catch minority class attacks.
  * **XGBoost (The Precision Engine):** Gradient boosting model tuned to filter out false alarms and identify complex attack signatures.
* **Flask Backend Server:** Hosts the ML models permanently in RAM for millisecond-latency predictions.
* **Auto-Updating UI:** A vanilla HTML/JS frontend that polls the server and visually triggers an "Attack Mode" if a threat is detected.

## 🖥️ VirtualBox / VM Test Environment

To simulate real network conditions and safely generate traffic, this project can be deployed using **Oracle VirtualBox virtual machines**.

### Setup Used in This Project:
* Two Virtual Machines running on VirtualBox:
  * **VM 1 (Attacker / Traffic Generator):** Generates network traffic such as pings, scans, and packet bursts.
  * **VM 2 (Victim / Monitoring Node):** Runs the packet capture script (`main.py`) and collects network flow data.
* Both VMs are connected through a **Host-Only Adapter / Internal Network**, allowing controlled communication without exposing traffic to the external internet.
* <img width="975" height="533" alt="image" src="https://github.com/user-attachments/assets/9e0dad46-5b65-4e13-9802-d2f8cb3efdd0" />
* <img width="975" height="521" alt="image" src="https://github.com/user-attachments/assets/6a20e767-f449-4a0b-80ed-27f2271eb30f" />
* Packet capture is performed on the victim VM using Python-based monitoring scripts, using vars.py code, ping the from vm3 while running vars.py at vm1 at the same time for real-time feature extraction.
* The captured traffic is saved into `features.csv`, which is then processed into ML-ready features.

### Why VirtualBox is Used:
* Provides a **safe isolated environment** for simulating cyber attacks
* Allows repeatable testing of network intrusion scenarios
* Enables controlled generation of labeled attack traffic
* Prevents risk to real production or personal networks

This setup ensures the dataset reflects realistic network behavior while maintaining a secure testing environment.

## 🧠 Architecture Flow

<img width="1484" height="732" alt="image" src="https://github.com/user-attachments/assets/2633373b-5616-4433-9e18-30a1f35c742f" />


1. **Traffic Capture:** Network data is captured (e.g., via VirtualBox internal network) and written directly to `features.csv`.
2. **Data Pipeline (`main.py`):** Reads the raw metrics, computes the 15 required ML features, and appends the clean row to `dataset.csv`.
3. **Inference API (`app.py`):** A Flask server reads the latest data, formats it into a Scikit-Learn NumPy array, and runs it through the loaded `.pkl` models.
4. **Dashboard (`index.html`):** Pings the backend every 60 seconds, displaying live network stats and alerting the user to threats.

## 📂 Repository Structure
* `app.py`: The Flask server that loads the ML models and serves the UI.
* `main.py`: The data processing script that calculates flow features.
* `index.html`: The frontend dashboard UI.
* `inference.ipynb`: Jupyter notebook containing model evaluation and testing.
* `*.pkl` / `*.zip`: The trained Machine Learning model weights.
* `dataset.csv` / `features.csv`: The local database files for the data pipeline.

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10+ (Built and tested on Python 3.13)
* VirtualBox (If simulating live attacks via VMs)

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
