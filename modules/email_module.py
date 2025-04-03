import requests
from modules.base_module import BaseModule

class EmailModule(BaseModule):
    def __init__(self):
        super().__init__("email_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] EmailModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        email = target.split("email:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {"User-Agent": global_config.get("user_agent"), "Accept": "application/json"}
        timeout = global_config.get("http_timeout", 10)
        api_url = self.config.get("api_url", f"https://emailrep.io/{email}")
        try:
            response = requests.get(api_url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                rep_data = response.json()
                details = {
                    "reputation": rep_data.get("reputation"),
                    "suspicious": rep_data.get("suspicious"),
                    "details": rep_data.get("details"),
                    "references": rep_data.get("references")
                }
                results["entities"].append({"type": "email", "value": email, "details": details})
                print(f"[+] Email data retrieved for {email}")
            else:
                print(f"[-] API returned status {response.status_code} for {email}")
                results["entities"].append({"type": "email", "value": email, "details": {"error": "No data retrieved"}})
        except Exception as e:
            print(f"[-] Error querying API for {email}: {e}")
            results["entities"].append({"type": "email", "value": email, "details": {"error": str(e)}})

        if "@" in email:
            local_part, domain = email.split("@", 1)
            results["new_targets"].extend([f"username:{local_part}", f"domain:{domain}"])
            results["relations"].append({"source": email, "target": domain, "relation": "email_domain"})
            results["relations"].append({"source": email, "target": local_part, "relation": "email_localpart"})
        return results
