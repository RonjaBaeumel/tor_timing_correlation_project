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

## Project Structure
```bash
tor-timing-correlation/
├── data/                       # Sample .pcap files #TODO
├── results/                    # Output plots and correlation scores #TODO
├── results_scripts/            # Python scripts for traffic analysis & plotting
├── traffic_scripts/            # Python scripts to create the traffic
├── notebooks/                  # Jupyter demos #TODO
├── requirements.txt            # Python dependencies
└── README.md                   # You're here
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
- Loads all .csv previously generated results
- Plots correlation scores by traffic type

## Example output:
TODO put in picture

## Sample Traffic Types
The generated data has the following patterns: 
### tor_regular/
Regular Interval Traffic:
- Pattern: 1 request every second
- Duration: 20 requests total
- Purpose: Establish a baseline with steady, predictable traffic

### tor_burst/
Burst Traffic:
- Pattern: 5 quick requests (0.2s apart), followed by a 3-second pause- 
- Repetition: 4 bursts (20 requests total)- 
- Purpose: Simulate bursts like rapid page refreshes or data pulls

### tor_parallel/
Parallel Client Noise Traffic
- Setup: Two clients send traffic simultaneously
- Client 1: Sends regular interval traffic (used for measurement)
- Client 2: Sends random traffic to simulate background noise
- Purpose: Add realism by emulating concurrent activity in the Tor network

### tor_random/
Randomized Interval Traffic:
- Pattern: Random delay between 0.1–3 seconds between each request- 
- Total Requests: 20- 
- Purpose: Mimic realistic, unpredictable human browsing behavior

Each folder contains:
- 10 client-side .pcap captures
- 10 server-side .pcap captures

File names example: tor_regular10_client.pcap, tor_regular10_server.pcap

## About the Project
This repository was created as part of a research-orientented university project to explore low-level traffic correlation vulnerabilities in Tor. It demonstrates how even without content, timing alone can reveal linkability between clients and servers.

## Disclaimer
This project is for educational and ethical research only. All experiments were conducted in a fully contained virtual environment and do not interact with the live Tor network.

## License
MIT License — see LICENSE for details.


<!--Tor Traffic Experiment Workflow
✅ 1. Initial Setup (One-Time Preparation)

    ✅ Ensure the following tools are installed:

Tor

Chutney (for creating the local Tor network)

tcpdump (for capturing network traffic)

Python 3

        curl (for initial connectivity testing)

    ✅ Clone/setup the Chutney test network with:

        2 client nodes

        1 hidden service (server)

        3 relays

    ✅ Configure:

        Hidden service to host a simple web server with a .onion address.

        Clients to access it only via SOCKS5 proxies (on ports 9055 and 9056).

🚀 2. Test the Tor Network

    Run Chutney to start the Tor test network.

    Test connectivity manually:

    curl --socks5-hostname 127.0.0.1:9055 http://your-hidden-service.onion

    ✅ If the server responds, the Tor network is working.

📦 3. Prepare for Data Collection

    Open three terminal windows:
    Terminal 1 (Client Side Capture)

sudo tcpdump -i lo port 9055 -w client_capture.pcap

Terminal 2 (Server Side Capture)

    sudo tcpdump -i lo port [server_port] -w server_capture.pcap

    (Use appropriate port or interface where server listens)
    Terminal 3 (Server Monitoring)

        Run a lightweight HTTP server to print incoming GET requests.

🧪 4. Run the Experiment

    In a new terminal, run one of the traffic generation scripts:

python3 generateTorTrafficRandom.py

Or, depending on scenario:

    python3 generateTorTrafficBurst.py
    python3 generateTorTrafficRegular.py

    If simulating parallel clients, start both scripts:

        One using port 9055 (target, measured)

        One using port 9056 (noise)

🧹 5. After the Test

    Stop tcpdump in both Terminal 1 and 2.

    Save the .pcap files (label them clearly: client/server + traffic type).

    Stop the Tor network (chutney stop or custom script).

    Restart Chutney to reset the network:

    chutney stop
    chutney configure
    chutney start

🔁 6. Repeat for Each Scenario

Repeat steps 3–5 for each of the 4 traffic modes:

    Regular

    Burst

    Randomized

    Parallel Clients (Regular + Random)

Repeat each scenario 10 times → results in 40 total captures.
📊 7. Post-Experiment

    Analyze .pcap files using:

        Wireshark or

        Python tools (e.g., scapy, pyshark) to inspect timing, packet sizes, etc.

    Goal: assess if traffic patterns can be linked across client and server → possible deanonymization.-->
