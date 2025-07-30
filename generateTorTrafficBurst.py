import requests
import time

# Tor SOCKS proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9055',
    'https': 'socks5h://127.0.0.1:9055'
}

url = 'http://ugqhoqtmenmykm2swd5hra3gg4fkpalmal4cn7burzyxvjbrnlksp2id.onion'  # Local target via Chutney

# Burst traffic pattern: 5 requests in quick succession, pause 3 seconds, repeat
num_bursts = 4
requests_per_burst = 5
#in seconds
pause_between_bursts = 3
pause_between_requests = 0.2

for burst in range(num_bursts):
    print(f"--- Starting burst {burst+1} ---")
    for i in range(requests_per_burst):
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            print(f"  [Burst {burst+1}.{i+1}] Status: {response.status_code}, Size: {len(response.content)}")
        except Exception as e:
            print(f"  [Burst {burst+1}.{i+1}] Request failed: {e}")
        time.sleep(pause_between_requests)
    time.sleep(pause_between_bursts)

print("Done with burst traffic test.")
