import requests
import re
import dns.resolver
import whois
from bs4 import BeautifulSoup
from modules.base_module import BaseModule

class DomainModule(BaseModule):
    def __init__(self):
        super().__init__("domain_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] DomainModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        domain = target.split("domain:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {"User-Agent": global_config.get("user_agent")}
        timeout = global_config.get("http_timeout", 10)
        try:
            whois_data = whois.whois(domain)
            details = {
                "registrar": whois_data.get("registrar"),
                "creation_date": str(whois_data.get("creation_date")),
                "expiration_date": str(whois_data.get("expiration_date")),
                "name_servers": whois_data.get("name_servers")
            }
            results["entities"].append({"type": "domain", "value": domain, "details": details})
            print(f"[+] WHOIS data retrieved for {domain}")
        except Exception as e:
            print(f"[-] Error during WHOIS lookup for {domain}: {e}")
            results["entities"].append({"type": "domain", "value": domain, "details": {"error": str(e)}})
        try:
            answers = dns.resolver.resolve(domain, 'A')
            ips = [rdata.to_text() for rdata in answers]
            results["entities"].append({"type": "ip", "value": ", ".join(ips), "details": {"source": "DNS A records"}})
            for ip in ips:
                results["relations"].append({"source": domain, "target": ip, "relation": "resolves_to"})
            print(f"[+] DNS A records for {domain}: {ips}")
        except Exception as e:
            print(f"[-] DNS lookup error for {domain}: {e}")
        if self.config.get("scrape_homepage", True):
            try:
                url = f"http://{domain}"
                resp = requests.get(url, headers=headers, timeout=timeout)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text()
                    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text)
                    emails = list(set(emails))
                    for email in emails:
                        results["new_targets"].append(f"email:{email}")
                        results["relations"].append({"source": domain, "target": email, "relation": "homepage_email"})
                    print(f"[+] Found emails on {domain}: {emails}")
                else:
                    print(f"[-] Homepage request for {domain} returned status {resp.status_code}")
            except Exception as e:
                print(f"[-] Error fetching homepage for {domain}: {e}")
        return results
