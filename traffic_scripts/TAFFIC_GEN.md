# Traffic Generation Guide
This guide explains how to set up a local Tor network with Chutney and use the included traffic generation scripts to create the `.pcap` datasets.


## 1. Prerequisites
- Python 3
- tcpdump
- `tshark` (Wireshark CLI)
- [Chutney](https://gitweb.torproject.org/chutney.git/)

Clone Chutney:
```bash
git clone https://git.torproject.org/chutney.git
cd chutney
make
```
## 2.Start the Tor network
Setup the Chutney test network (or use a provided example) with:
- 2 client nodes
- 1 hidden service (server)
- 3 relays

Start the examples/basic network:
```bash
./chutney configure networks/basic
./chutney start networks/basic
```

Configure:
- Clients to only use SocksPort to access the network (on ports 9055 and 9056 for example).<br>
    For this open the torrc file in each client:
    ```bash
    nano chutney/net/nodes/000a/torrc
    ```
    and change the Port number manually. To test if it works: 
    ```bash
    TOR_SOCKS_PORT=9055 torsocks curl http://www.google.com
    ```
- Hidden service to host a simple web server with a .onion address.<br>
    For this use node 008c to configure your service on and open the torrc file again. Then add these two lines:
    ```bash
    HiddenServiceDir <complete_path_to_your>/chutney/net/nodes/008c/hs  #insert your path
    HiddenServicePort 80 127.0.0.1:8080 
    ```
    
## 3. Test the Tor Network
- Restart the Tor test network.
- Test connectivity manually:
```bash
curl --socks5-hostname 127.0.0.1:9055 http://<your-hidden-service.onion>
```
> If the server responds with the html page, the Tor network is working.


## 4. Prepare for Data Collection
- Open three terminal windows:
**Terminal 1** 
- Client Side Capture
```bash
sudo tcpdump -i lo port 9055 -w client_capture.pcap
```

**Terminal 2** 
- Server Side Capture
```bash
    sudo tcpdump -i lo port 8080 -w server_capture.pcap
```
- Use right port or interface where server listens

**Terminal 3** 
- Monitor Server for incomming GET requests.
- navigate to the .../chutney directory
- restart the network 
- navigate to the server node and start the  server
```bash
./chutney restart networcs/basic
cd net/nodes/008c
python3 -m http.server 8080
```  


## 5.Run the Experiment
- In a new terminal, run one of the traffic generation scripts:
```bash
python3 generateTorTrafficRandom.py
```
Or, depending on scenario:
```bash
    python3 generateTorTrafficBurst.py
    python3 generateTorTrafficRegular.py
```
- If simulating parallel clients, start both scripts:
- One using port 9055 (target, measured)
- One using port 9056 (noise)

## 6. After the Test
- Stop tcpdump in both Terminal 1 and 2 with Ctrl+C.
- Save the .pcap files (label them clearly: client/server + traffic type).
- Stop the Tor network (chutney stop or custom script).
- Restart Chutney to reset the network

## 7. Repeat for Each Scenario
- Repeat steps 3–5 for each of the 4 traffic modes:
    - Regular
    - Burst
    - Randomized
    - Parallel Clients (Regular + Random)

    >Repeat each scenario 10 or more times for statistic relevance
<br>
The following patterns are implemented here:
### Regular Interval Traffic:
- Pattern: 1 request every second
- Duration: 20 requests total
- Purpose: Establish a baseline with steady, predictable traffic

### Burst Traffic:
- Pattern: 5 quick requests (0.2s apart), followed by a 3-second pause- 
- Duration: 4 bursts (20 requests total)- 
- Purpose: Simulate bursts like rapid page refreshes or data pulls

### Randomized Interval Traffic:
- Pattern: Random delay between 0.1–3 seconds between each request- 
- Duration: 20 requests total 
- Purpose: Mimic realistic, unpredictable human browsing behavior

### Parallel Client Noise Traffic
- Setup: Two clients send traffic simultaneously
- Client 1: Sends regular interval traffic (used for measurement)
- Client 2: Sends random traffic (used to simulate background noise)
- Purpose: Add realism by emulating concurrent activity in the Tor network

Each folder contains:
- 10 client-side .pcap captures
- 10 server-side .pcap captures

File names example: tor_regular10_client.pcap, tor_regular10_server.pcap

# 8. Post-Experiment
- Analyze .pcap files to assess if traffic patterns can be linked across client and server → possible deanonymization.
- see [ANALYSIS.md](../ANALYSIS.md)




