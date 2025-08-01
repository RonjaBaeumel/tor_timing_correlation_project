import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

TRAFFIC_TYPES = [
    'tor_regular_traffic',
    'tor_burst_traffic',
    'tor_parallel_traffic',
    'tor_random_traffic'
]

def load_data():
    all_data = []
    for traffic_type in TRAFFIC_TYPES:
        csv_path = f"{traffic_type}_correlation_results.csv"
        if not os.path.exists(csv_path):
            print(f"Missing file: {csv_path}")
            continue
        df = pd.read_csv(csv_path)
        df["traffic_type"] = traffic_type.replace("tor_", "").replace("_traffic", "")
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

def plot_max_correlation(data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x="traffic_type", y="max_correlation", palette="Set3")
    sns.stripp
