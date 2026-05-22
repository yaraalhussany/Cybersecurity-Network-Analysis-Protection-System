from scapy.all import sniff, IP, TCP
import csv
import numpy as np
import os

# VM IPs
VM1_IP = "192.168.56.104"   # detector VM
VM3_IP = "192.168.56.106"   # traffic generator VM

# Shared folder path inside VM1
# This maps to:
# C:\CPH.cpp\CPH.cpp\.cph\networksproject\features.csv
CSV_PATH = "/media/sf_networksproject/features.csv"

# Storage
all_times = []
bwd_packets = []


def compute_idle_time(current_time):
    """
    Idle time = gap between current packet and previous packet
    Only counted if gap > 1 second
    """
    if len(all_times) == 0:
        return 0

    last_time = all_times[-1]
    gap = current_time - last_time

    if gap > 1:
        return gap
    else:
        return 0


def packet_callback(packet):
    if IP in packet:
        timestamp = packet.time
        src = packet[IP].src
        dst = packet[IP].dst
        pkt_len = len(packet)

        # Default values
        direction = "OTHER"
        bwd_tcp_segment_size = 0

        # Direction detection
        if src == VM1_IP and dst == VM3_IP:
            direction = "FORWARD"

        elif src == VM3_IP and dst == VM1_IP:
            direction = "BACKWARD"

            # Backward TCP segment size
            if TCP in packet:
                bwd_tcp_segment_size = len(packet[TCP].payload)
            else:
                bwd_tcp_segment_size = pkt_len

            bwd_packets.append(bwd_tcp_segment_size)

        # Idle time calculation
        idle_time = compute_idle_time(timestamp)
        all_times.append(timestamp)

        print(
            f"Captured: {src} -> {dst} | "
            f"{pkt_len} bytes | {direction}"
        )

        # CSV row
        row = [
            timestamp,
            src,
            dst,
            bwd_tcp_segment_size,
            idle_time,
            pkt_len,
            direction
        ]

        # Save directly to CSV
        with open(CSV_PATH, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)


def create_csv_header():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "Source IP",
                "Destination IP",
                "Backward TCP Segment Size",
                "Idle Time",
                "Packet Size",
                "Direction"
            ])


print("STARTING CAPTURE... Press CTRL+C to stop\n")

create_csv_header()

try:
    sniff(
        iface="enp0s8",   # Host-only adapter
        filter="ip",
        prn=packet_callback,
        store=0
    )

except KeyboardInterrupt:
    print("\nCapture stopped. Results saved to features.csv")
