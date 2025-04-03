import requests
from modules.base_module import BaseModule

class RealNameModule(BaseModule):
    def __init__(self):
        super().__init__("realname_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] RealNameModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        # Expect target in the format "realname:John Doe"
        realname = target.split("realname:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": realname,
                "format": "json"
            }
            headers = {"User-Agent": global_config.get("user_agent")}
            resp = requests.get(url, params=params, headers=headers, timeout=global_config.get("http_timeout", 10))
            data = resp.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                # Use the first result.
                first = search_results[0]
                details = {
                    "title": first.get("title"),
                    "snippet": first.get("snippet")
                }
                results["entities"].append({"type": "realname", "value": realname, "details": details})
                print(f"[+] Wikipedia result found for {realname}")
            else:
                print(f"[-] No Wikipedia results for {realname}")
                results["entities"].append({"type": "realname", "value": realname, "details": {"error": "No results"}})
        except Exception as e:
            print(f"[-] Error querying Wikipedia for {realname}: {e}")
            results["entities"].append({"type": "realname", "value": realname, "details": {"error": str(e)}})
        return results
