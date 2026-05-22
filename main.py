# backend.py

import csv
import numpy as np

input_path = "features.csv"
output_path = "dataset.csv"

timestamps = []
fwd_times = []
bwd_times = []

bwd_sizes = []
all_sizes = []
idle_times = []


def readfeatures():
    with open(input_path, mode="r") as f:
        reader = csv.reader(f)

        for row in reader:
            if not row:
                continue

            # skip header
            if row[0].lower() == "timestamp":
                continue

            try:
                timestamp = float(row[0])
                srcip = row[1]
                dstip = row[2]
                bwd_size = float(row[3])
                idle = float(row[4])
                pkt_size = float(row[5])
                direction = row[6].strip().upper()
            except:
                continue

            timestamps.append(timestamp)
            all_sizes.append(pkt_size)
            idle_times.append(idle)

            if direction == "FORWARD":
                fwd_times.append(timestamp)

            elif direction == "BACKWARD":
                bwd_sizes.append(bwd_size)
                bwd_times.append(timestamp)


def compute_and_save():
    if len(all_sizes) == 0:
        print("No data found in features.csv")
        return

    # -----------------------------------
    # Bwd Packet Length Max / Mean / Std
    # -----------------------------------
    if len(bwd_sizes) > 0:
        bwd_packet_length_max = np.max(bwd_sizes)
        bwd_packet_length_mean = np.mean(bwd_sizes)
        bwd_packet_length_std = np.std(bwd_sizes)
        avg_bwd_segment_size = sum(bwd_sizes) / len(bwd_sizes)
    else:
        bwd_packet_length_max = 0
        bwd_packet_length_mean = 0
        bwd_packet_length_std = 0
        avg_bwd_segment_size = 0

    # -----------------------------------
    # Flow IAT Max
    # -----------------------------------
    if len(timestamps) > 1:
        flow_iat = np.diff(sorted(timestamps))
        flow_iat_max = np.max(flow_iat)
    else:
        flow_iat_max = 0

    # -----------------------------------
    # Fwd IAT Std / Max
    # -----------------------------------
    if len(fwd_times) > 1:
        fwd_iat = np.diff(sorted(fwd_times))
        fwd_iat_std = np.std(fwd_iat)
        fwd_iat_max = np.max(fwd_iat)
    else:
        fwd_iat_std = 0
        fwd_iat_max = 0

    # -----------------------------------
    # Packet Length Features
    # -----------------------------------
    pkt_arr = np.array(all_sizes)

    max_packet_length = np.max(pkt_arr)
    packet_length_mean = np.mean(pkt_arr)
    packet_length_std = np.std(pkt_arr)
    packet_length_variance = np.var(pkt_arr)
    avg_packet_size = np.mean(pkt_arr)

    # -----------------------------------
    # Idle Features
    # -----------------------------------
    if len(idle_times) > 0:
        idle_mean = np.mean(idle_times)
        idle_max = np.max(idle_times)
        idle_min = np.min(idle_times)
    else:
        idle_mean = 0
        idle_max = 0
        idle_min = 0

    # -----------------------------------
    # Default Label
    # -----------------------------------
    attack_status = "not attack"

    # -----------------------------------
    # EXACT REQUIRED ORDER
    # -----------------------------------
    features = [
        bwd_packet_length_max,
        bwd_packet_length_mean,
        bwd_packet_length_std,
        flow_iat_max,
        fwd_iat_std,
        fwd_iat_max,
        max_packet_length,
        packet_length_mean,
        packet_length_std,
        packet_length_variance,
        avg_packet_size,
        avg_bwd_segment_size,
        idle_mean,
        idle_max,
        idle_min,
        attack_status
    ]

    with open(output_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(features)

    print("Saved ONE ROW to dataset.csv")


if __name__ == "__main__":
    readfeatures()
    compute_and_save()