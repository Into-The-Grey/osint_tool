from ipwhois import IPWhois
import json
from modules.base_module import BaseModule

class IPModule(BaseModule):
    def __init__(self):
        super().__init__("ip_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] IPModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        # Expect target in the format "ip:1.2.3.4"
        ip_addr = target.split("ip:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        try:
            obj = IPWhois(ip_addr)
            details = obj.lookup_whois()
            # Extract a few useful fields.
            summary = {
                "asn": details.get("asn"),
                "asn_description": details.get("asn_description"),
                "country": details.get("asn_country_code"),
                "nets": details.get("nets")
            }
            results["entities"].append({"type": "ip", "value": ip_addr, "details": summary})
            print(f"[+] IP data retrieved for {ip_addr}")
        except Exception as e:
            print(f"[-] Error looking up IP {ip_addr}: {e}")
            results["entities"].append({"type": "ip", "value": ip_addr, "details": {"error": str(e)}})
        return results
