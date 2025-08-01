# Timing Correlation Attacks on Tor Traffic

This project explores timing-based correlation attacks on a local Tor network using simulated traffic. The goal is to evaluate how timing patterns can be used to deanonymize users under different traffic behaviors.

## What It Does
- Spins up a local Tor network with [Chutney](https://gitweb.torproject.org/chutney.git/)
- Simulates client-server communication using various traffic types (regular, burst, parallel, random)
- Captures `.pcap` files at client and server
- Analyzes and compares traffic via normalized cross-correlation
- Visualizes attack effectiveness across traffic types

## Project Structure

- `scripts/` — Python scripts for analysis and plotting
- `utils/` — Timestamp extraction and preprocessing functions
- `results/` — Output CSVs and plots
- `data/sample_pcaps/` — Small test `.pcap` files (if permissible)
- `notebooks/` — (Optional) Jupyter notebook for exploration

## Requirements

```bash
pip install -r requirements.txt
sudo apt install tshark
