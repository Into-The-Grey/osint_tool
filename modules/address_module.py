import requests
from modules.base_module import BaseModule

class AddressModule(BaseModule):
    def __init__(self):
        super().__init__("address_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] AddressModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        # Expect target in the format "address:123 Main St, City, Country"
        address = target.split("address:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"format": "json", "q": address}
            headers = {"User-Agent": global_config.get("user_agent")}
            resp = requests.get(url, params=params, headers=headers, timeout=global_config.get("http_timeout", 10))
            data = resp.json()
            if data:
                # Take the first result.
                location = data[0]
                details = {
                    "lat": location.get("lat"),
                    "lon": location.get("lon"),
                    "display_name": location.get("display_name")
                }
                results["entities"].append({"type": "address", "value": address, "details": details})
                print(f"[+] Geocoding data retrieved for {address}")
            else:
                print(f"[-] No geocoding results for {address}")
                results["entities"].append({"type": "address", "value": address, "details": {"error": "No results"}})
        except Exception as e:
            print(f"[-] Error geocoding address {address}: {e}")
            results["entities"].append({"type": "address", "value": address, "details": {"error": str(e)}})
        return results
