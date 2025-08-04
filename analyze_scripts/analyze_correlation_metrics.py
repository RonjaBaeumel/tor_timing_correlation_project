import os
import subprocess
import pandas as pd
import numpy as np
from scipy.signal import correlate
from scipy.stats import zscore


# This script requires tshark (Wireshark CLI tool) to be installed and accessible in your system PATH


# SETTINGS
BIN_SIZE = 0.1  # seconds
TRAFFIC_TYPES = ['tor_regular', 'tor_burst', 'tor_parallel', 'tor_random']
NUM_RUNS = 10


#get the timestamps out of the pcap files
def extract_timestamps(pcap_path):
    result = subprocess.run(
        ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.time_epoch'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    timestamps = [float(ts.strip()) for ts in result.stdout.strip().split('\n') if ts.strip()]
    return np.array(timestamps)

#TODO
def bin_timestamps(timestamps, bin_size):
    if len(timestamps) == 0:
        return np.array([])
    min_time = timestamps.min()
    max_time = timestamps.max()
    bins = np.arange(min_time, max_time + bin_size, bin_size)
    binned_counts, _ = np.histogram(timestamps, bins=bins)
    return binned_counts


#Takes two pcap files (one client-server pair) and computes the z-score for correlation 
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


#handles each client - server pair in one folder (traffic type)
def process_traffic_type(folder):
    print(f"\nAnalyzing {folder}")
    results = []

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_folder = os.path.join(project_root, folder)

    #get files
    for i in range(1, NUM_RUNS + 1):
        # Build the pcap path in the parent directory
        client_pcap = os.path.join(target_folder, f"{folder}{i}_client.pcap")
        server_pcap = os.path.join(target_folder, f"{folder}{i}_server.pcap")

        if not os.path.exists(client_pcap) or not os.path.exists(server_pcap):
            print(f"Missing files for run {i}")
            continue

        #analyze for existing correlation 
        max_corr, lag = analyze_pair(client_pcap, server_pcap)
        results.append({
            "run": i,
            "max_correlation": max_corr,
            "lag": lag
        })

    #check if the results folder exists
    results_path= os.path.join(project_root, "results")
    os.makedirs(results_path, exist_ok=True)

    # Create the DataFrame for the results and save in a csv file
    df = pd.DataFrame(results)
    df.to_csv(f"{results_path}/{folder}_correlation_results.csv", index=False)
    print(f"Saved results to {results_path}/{folder}_correlation_results.csv")



def main():
    #iterate over the four different traffic types 
    for traffic_type in TRAFFIC_TYPES:
        process_traffic_type(traffic_type)


if __name__ == "__main__":
    main()
