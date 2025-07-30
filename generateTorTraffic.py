import requests
import time

# Tor SOCKS proxy
#socks5h:// -> the h is important because it ensures that DNS resolution happens over Tor, which simulates real Tor usage.
proxies = {
    'http': 'socks5h://127.0.0.1:9055',
    'https': 'socks5h://127.0.0.1:9055'
}

url = 'http://ugqhoqtmenmykm2swd5hra3gg4fkpalmal4cn7burzyxvjbrnlksp2id.onion'  # Local target via Chutney

# Generate regular traffic
for i in range(20):
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        print(f"[{i+1}] Status: {response.status_code}, Size: {len(response.content)}")
    except Exception as e:
        print(f"[{i+1}] Request failed: {e}")
    time.sleep(1)






#    Using socks5h ensures DNS queries also go through Tor.
#    If you want to send traffic to your own Tor hidden service (server), you can also set that up in Chutney — let me know if you'd like to
#     simulate hidden service communication instead of external sites.