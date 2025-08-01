import os
import subprocess
import pandas as pd
import numpy as np
from scipy.signal import correlate
from scipy.stats import zscore

# SETTINGS
BIN_SIZE = 0.1  # seconds
TRAFFIC_TYPES = ['tor_regular_traffic', 'tor_burst_traffic', 'tor_parallel_traffic', 'tor_random_traffic']
NUM_RUNS = 10

def extract_timestamps(pcap_path):
    result = subprocess.run(
        ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.time_epoch'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    timestamps = [float(ts.strip()) for ts in result.stdout.strip().split('\n') if ts.strip()]
    return np.array(timestamps)

def bin_timestamps(timestamps, bin_size):
    if len(timestamps) == 0:
        return np.array([])
    min_time = timestamps.min()
    max_time = timestamps.max()
    bins = np.arange(min_time, max_time + bin_size, bin_size)
    binned_counts, _ = np.histogram(timestamps, bins=bins)
    return binned_counts

def analyze_pair(client_pcap, server_pcap):
    client_ts = extract_timestamps(client_pcap)
    server_ts = extract_timestamps(server_pcap)

    client_bins = bin_timestamps(client_ts, BIN_SIZE)
    server_bins = bin_timestamps(server_ts, BIN_SIZE)

    # Align both to the same length
    length = max(len(client_bins), len(server_bins))
    client_bins = np.pad(client_bins, (0, length - len(client_bins)), mode='constant')
    server_bins = np.pad(server_bins, (0, length - len(server_bins)), mode='constant')

    # Normalize using z-score
    client_z = zscore(client_bins)
    server_z = zscore(server_bins)

    corr = correlate(client_z, server_z, mode='full')
    max_corr = np.max(corr)
    lag = np.argmax(corr) - (len(client_z) - 1)

    return max_corr, lag

def process_traffic_type(folder):
    print(f"\nAnalyzing {folder}")
    results = []

    for i in range(1, NUM_RUNS + 1):
        client_pcap = os.path.join(folder, f"{folder[:-8]}{i}_client.pcap")
        server_pcap = os.path.join(folder, f"{folder[:-8]}{i}_server.pcap")

        if not os.path.exists(client_pcap) or not os.path.exists(server_pcap):
            print(f"Missing files for run {i}")
            continue

        max_corr, lag = analyze_pair(client_pcap, server_pcap)
        results.append({
            "run": i,
            "max_correlation": max_corr,
            "lag": lag
        })

    df = pd.DataFrame(results)
    df.to_csv(f"{folder}_correlation_results.csv", index=False)
    print(f"Saved results to {folder}_correlation_results.csv")

def main():
    for traffic_type in TRAFFIC_TYPES:
        process_traffic_type(traffic_type)

if __name__ == "__main__":
    main()
