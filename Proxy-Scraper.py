import os
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
import json

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Displays the tool banner."""
    banner = f"""
{Fore.RED}{Style.BRIGHT} ____                        ____                                 
{Fore.RED}{Style.BRIGHT}|  _ \ _ __ _____  ___   _  / ___|  ___ _ __ __ _ _ __   ___ _ __ 
{Fore.YELLOW}{Style.BRIGHT}| |_) | '__/ _ \ \/ / | | | \___ \ / __| '__/ _` | '_ \ / _ \ '__|
{Fore.YELLOW}{Style.BRIGHT}|  __/| | | (_) >  <| |_| |  ___) | (__| | | (_| | |_) |  __/ |   
{Fore.GREEN}{Style.BRIGHT}|_|   |_|  \___/_/\_\\__, | |____/ \___|_|  \__,_| .__/ \___|_|   
{Fore.GREEN}{Style.BRIGHT}                     |___/                       |_|              

{Fore.CYAN}{Style.BRIGHT}       Proxy Scraper Tool - Created by Emperor (Somnath Mali)
{Fore.MAGENTA}====================================================================
{Fore.WHITE} A simple tool to scrape proxies and manage logs efficiently.
====================================================================
"""
    print(banner)

def main_menu():
    while True:
        print(f"""
{Fore.CYAN}{Style.BRIGHT}[1] Start Scraper
[2] View Logs
[3] View Proxy Info
[4] Exit
""")
        choice = input(f"{Fore.GREEN}{Style.BRIGHT}Select an option: {Style.RESET_ALL}")
        if choice in ['1', '2', '3', '4']:
            return choice
        print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 4.")

def scrape_proxies():
    urls = [
        "https://www.sslproxies.org/",
        "https://free-proxy-list.net/",
        "https://www.us-proxy.org/"
    ]
    proxies = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"class": "table-striped"})

        if table is None:
            print(f"No table found on the page: {url}")
            continue

        for row in table.tbody.find_all("tr"):
            ip = row.find_all("td")[0].text.strip()
            port = row.find_all("td")[1].text.strip()
            proxies.append(f"{ip}:{port}")

    return proxies

def verify_proxy(proxy):
    url = "http://www.google.com"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}",
    }
    print(f"Testing proxy: {proxy}")
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}Proxy {proxy} is working.")
            return True
    except requests.RequestException as e:
        print(f"{Fore.RED}Proxy {proxy} failed: {e}")
    return False

def start_scraper():
    """Scrapes proxies and verifies them."""
    print(f"\n{Fore.YELLOW}Scraping proxies... Please wait.")
    proxies = scrape_proxies()
    print(f"{Fore.GREEN}Scraped {len(proxies)} proxies.")

    if not proxies:
        print(f"{Fore.RED}No proxies found. Exiting scraper.")
        return

    print(f"\n{Fore.YELLOW}Verifying proxies...")
    working_proxies = [proxy for proxy in proxies if verify_proxy(proxy)]
    print(f"{Fore.GREEN}Found {len(working_proxies)} working proxies.")

    with open("working_proxies.txt", "w") as f:
        for proxy in working_proxies:
            f.write(f"{proxy}\n")
    print(f"{Fore.CYAN}Working proxies saved to working_proxies.txt")

def load_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def test_proxy(proxy):
    proxy_types = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}",
        "socks4": f"socks4://{proxy}",
        "socks5": f"socks5://{proxy}",
    }

    test_url = "http://ipinfo.io"  # Using ipinfo.io to check the proxy
    anonymity_status = "Unknown"
    secure_proxy = False
    proxy_response = {}

    for proxy_type, proxy_url in proxy_types.items():
        try:
            response = requests.get(test_url, proxies={proxy_type: proxy_url}, timeout=5)
            if response.status_code == 200:
                json_data = response.json()
                if "ip" in json_data:  # Check if 'ip' is in the response JSON
                    secure_proxy = True
                    detected_ip = json_data["ip"]
                    anonymity_status = f"Anonymity Verified: IP = {detected_ip}"
                    # Extracting the proxy and port from the proxy string
                    proxy_ip, proxy_port = proxy.split(":") if ":" in proxy else (proxy, "80")
                    proxy_response = {
                        "proxy": proxy,
                        "proxy_type": proxy_type,
                        "secure": secure_proxy,
                        "anonymity_status": anonymity_status,
                        "ip": detected_ip,
                        "port": proxy_port,
                        "response": json_data  # Store the full response
                    }
                    print(f"Verified: {proxy_type} {proxy} - {anonymity_status}");
                    return proxy_response
        except:
            continue  # Try the next proxy type

    return {
        "proxy": proxy,
        "proxy_type": "Unknown",
        "secure": secure_proxy,
        "anonymity_status": "Failed or Non-Anonymous",
        "ip": "Unknown",
        "port": "Unknown",
        "response": "No response or error"
    }

def view_logs():
    """Simulates viewing logs."""
    print(f"\n{Fore.YELLOW}Fetching logs...")
    time.sleep(2)
    print(f"{Fore.GREEN}No logs found! (This is a placeholder for future functionality)")

def view_proxy_info():
    """Displays detailed proxy information."""
    print(f"\n{Fore.YELLOW}Fetching proxy information...")

    # Prompt the user to enter the file name and format
    file_name = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the proxy file name (without extension): {Style.RESET_ALL}")
    file_format = input(f"{Fore.GREEN}{Style.BRIGHT}Enter the proxy file format (txt/json): {Style.RESET_ALL}")

    # Construct the file path based on user input
    file_path = f"{file_name}.{file_format}"

    if not os.path.exists(file_path):
        print(f"{Fore.RED}File not found! Please check the file path and try again.")
        return

    proxies = load_proxies(file_path)
    print(f"{Fore.GREEN}Loaded {len(proxies)} proxies from {file_path}.")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(test_proxy, proxies))

    # Save proxy responses and formatted results
    print("\nTest Results:")
    formatted_proxies = []  # For proxy chain
    with open("proxy_responses.json", "w", encoding="utf-8") as response_file, \
         open("proxy_test_results.txt", "w", encoding="utf-8") as result_file, \
         open("working_proxies.txt", "w", encoding="utf-8") as working_file:
        for result in results:
            # Save proxy response (full response in JSON format)
            response_file.write(json.dumps(result["response"], ensure_ascii=False, indent=4) + "\n")

            # Format the output as requested
            if result["secure"]:
                chain_entry = f"{result['proxy_type']} {result['ip']} {result['port']}"
                formatted_proxies.append(chain_entry)
                result_file.write(chain_entry + "\n")

                # Save working proxies
                working_file.write(result["proxy"] + "\n")

    print("\nProxy responses saved to proxy_responses.json")
    print(f"Formatted proxy test results saved to proxy_test_results.txt")
    print(f"Working proxies saved to working_proxies.txt\nTotal Working Proxies: {len(formatted_proxies)}")

def main():
    clear_screen()
    display_banner()
    while True:
        choice = main_menu()
        if choice == '1':
            start_scraper()
        elif choice == '2':
            view_logs()
        elif choice == '3':
            view_proxy_info()
        elif choice == '4':
            print(f"{Fore.RED}Exiting... Goodbye, and thank you for using the tool!")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
        time.sleep(2)

if __name__ == "__main__":
    main()
