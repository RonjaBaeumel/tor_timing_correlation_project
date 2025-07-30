import requests
import time
import random

# Tor SOCKS proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9055',
    'https': 'socks5h://127.0.0.1:9055'
}

url = 'http://ugqhoqtmenmykm2swd5hra3gg4fkpalmal4cn7burzyxvjbrnlksp2id.onion'  # Local target via Chutney

# Randomized traffic pattern
total_requests = 20
#in seconds
min_pause = 0.1 
max_pause = 3   

for i in range(total_requests):
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        print(f"[{i+1}] Status: {response.status_code}, Size: {len(response.content)}")
    except Exception as e:
        print(f"[{i+1}] Request failed: {e}")
    #Random pause between 0.1 and 3 seconds
    pause = random.uniform(min_pause, max_pause)
    time.sleep(pause)

print("Done with randomized traffic test.")
