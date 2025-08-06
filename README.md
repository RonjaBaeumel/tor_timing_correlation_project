# Timing Correlation Attacks on Tor Traffic
This project explores timing-based correlation attacks on a local Tor network using simulated traffic. The goal is to evaluate how timing patterns can be used to deanonymize users under different traffic behaviors.


## About the Project
This repository was created as a final project for an university course to explore low-level traffic correlation vulnerabilities in Tor. It demonstrates how even without content, timing alone can reveal linkability between clients and servers. This includes: 
- Setting up a local Tor network with [Chutney](https://gitweb.torproject.org/chutney.git/) including two clients, several relays and a hidden tor service running on a server
- Simulating client-server communication using various traffic types (regular, burst, parallel, random)
- Capturing these conversations as `.pcap` files at client and server
- Analyzing and comparing traffic via normalized cross-correlation
- Visualizing attack effectiveness across traffic types
- Interpreting results and drawing a conclusion


## Usage
### 1. Get the Data
To generate the `.pcap` files used in this analysis:
1. **Set up a local Tor network** using [Chutney](https://gitweb.torproject.org/chutney.git/)
2. **Run the included traffic generation scripts** for different traffic patterns
3. **Capture traffic** on the client and server interfaces
4. Store the resulting `.pcap` files under folders like `tor_regular/`, `tor_burst/`, etc.
or:
1. **Download provided examples**

> For full setup details and instructions, see [`TRAFFIC_GEN.md`](TRAFFIC_GEN.md)

### 2. Analyze traffic correlation
```bash
python3 scripts/analyze_correlation_metrics.py
```
This script:
- Loads .pcap files from specified folders ( in client/server pairs)
- Extracts timestamps using tshark
- Computes normalized cross-correlation and max lag
- Saves results to results/<traffic_type>_correlation_results.csv

### 3. Plot results
```bash
python scripts/plot_correlation_results.py
```
This script:
- Loads all previously generated .csv results
- Plots correlation scores by traffic type

## Example output:
[Analysis](ANALYSIS.md)


## Project Structure
```bash
tor-timing-correlation/
├── data/                       # Sample .pcap files #TODO
├── results/                    # Output plots and correlation scores
├── analyze_scripts/            # Python scripts for traffic analysis & plotting
├── traffic_scripts/            # Python scripts to create the traffic and instructions
├── requirements.txt            # Python dependencies
├── README.md                   # You're here
└── ANALYSIS.md                 # Results and interpretation
```

## Requirements
### Python Packages
Install with:
```bash
pip install -r requirements.txt
```
### System Dependencies
You must have tshark installed (the command-line version of Wireshark), as it's used to extract packet timestamps from .pcap files.<br>
- On Linux:
```bash
sudo apt install tshark
```
- On macOS (via Homebrew):
```bash
brew install wireshark
```
You may also need to run:
```bash
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark $USER
```
Then restart your session to capture without sudo.
TODO: captures with tcpdump -> then add tcpdump (or captures with tshark possible?)


## Disclaimer
This project is for educational and ethical research only. All experiments were conducted in a fully contained virtual environment and did not interact with the live Tor network.


## License
MIT License — see LICENSE for details.
