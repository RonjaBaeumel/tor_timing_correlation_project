import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

TRAFFIC_TYPES = ['tor_regular', 'tor_burst', 'tor_parallel', 'tor_random']

#Loads the data from the previoulsy generated .csv files 
def load_data():
    all_data = []

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for traffic_type in TRAFFIC_TYPES:
        csv_path = os.path.join(project_root, "results", f"{traffic_type}_correlation_results.csv")
        if not os.path.exists(csv_path):
            print(f"Missing file: {csv_path}")
            continue
        df = pd.read_csv(csv_path)
        df["traffic_type"] = traffic_type.replace("tor_", "")
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)


#Create and save correlation plot in the results folder
def plot_max_correlation(data):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x="traffic_type", y="max_correlation", palette="Set3")
    sns.stripplot(data=data, x="traffic_type", y="max_correlation", color="black", alpha=0.5, jitter=True)
    plt.title("Maximum Cross-Correlation by Traffic Type")
    plt.ylabel("Max Correlation Score")
    plt.xlabel("Traffic Type")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(project_root, "results","correlation_plot.png"), dpi=300)
    plt.show()

if __name__ == "__main__":
    df = load_data()
    plot_max_correlation(df)