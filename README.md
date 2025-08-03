# Timing Correlation Attacks on Tor Traffic
This project explores timing-based correlation attacks on a local Tor network using simulated traffic. The goal is to evaluate how timing patterns can be used to deanonymize users under different traffic behaviors.

## What It Does
- Spins up a local Tor network with [Chutney](https://gitweb.torproject.org/chutney.git/)
- Simulates client-server communication using various traffic types (regular, burst, parallel, random)
- Captures `.pcap` files at client and server
- Analyzes and compares traffic via normalized cross-correlation
- Visualizes attack effectiveness across traffic types

## Requirements
### Python Packages
Install with:
```bash
pip install -r requirements.txt
```
### System Dependencies
You must have tshark installed (the command-line version of Wireshark), as it's used to extract packet timestamps from .pcap files.
On Linux:
```bash
sudo apt install tshark
```
On macOS (via Homebrew):
```bash
brew install wireshark
```
You may also need to run:
```bash
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark $USER
```
Then restart your session to capture without sudo.

## Project Structure
```bash
tor-timing-correlation/
├── data/                  # Sample .pcap files (optional, small)
├── results/               # Output plots and correlation scores
├── scripts/               # Python scripts for analysis & plotting
├── utils/                 # Helper functions for .pcap processing
├── notebooks/             # (Optional) Jupyter demos
├── requirements.txt       # Python dependencies
└── README.md              # You're here
```

## Usage
### 1. Analyze traffic correlation
```bash
python3 scripts/analyze_correlation_metrics.py
```
This script:
- Loads .pcap files from specified folders (client/server pairs)
- Extracts timestamps using tshark
- Computes normalized cross-correlation and max lag
- Saves results to results/<traffic_type>_correlation_results.csv

### 2. Plot results
```bash
python scripts/plot_correlation_results.py
```
This script:
- Loads all .csv results
- Plots correlation scores by traffic type

Example output:

Sample Traffic Types
- tor_regular/
- tor_burst/
- tor_parallel/
- tor_random/

Each folder contains:
- 10 client-side .pcap captures
- 10 server-side .pcap captures

Files named like: tor_regular10_client.pcap, tor_regular10_server.pcap

## About the Project
This repository was created as part of a research-oriented university project to explore low-level traffic correlation vulnerabilities in Tor. It demonstrates how even without content, timing alone can reveal linkability between clients and servers.

## Disclaimer
This project is for educational and ethical research only. All experiments were conducted in a fully contained virtual environment and do not interact with the live Tor network.

## License
MIT License — see LICENSE for details.

