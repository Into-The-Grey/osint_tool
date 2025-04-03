import requests
from modules.base_module import BaseModule

class UsernameModule(BaseModule):
    def __init__(self):
        super().__init__("username_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] UsernameModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        username = target.split("username:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {"User-Agent": global_config.get("user_agent")}
        timeout = global_config.get("http_timeout", 10)
        if self.config.get("check_github", True):
            github_url = f"https://github.com/{username}"
            try:
                r = requests.get(github_url, headers=headers, timeout=timeout)
                if r.status_code == 200:
                    results["entities"].append({"type": "username", "value": username, "details": {"platform": "GitHub", "profile": github_url}})
                    results["relations"].append({"source": username, "target": github_url, "relation": "GitHub_profile"})
                    print(f"[+] GitHub account found for {username}")
                else:
                    print(f"[-] GitHub account not found for {username}")
            except Exception as e:
                print(f"[-] Error checking GitHub for {username}: {e}")
        if self.config.get("check_reddit", True):
            reddit_url = f"https://www.reddit.com/user/{username}/about.json"
            try:
                r = requests.get(reddit_url, headers=headers, timeout=timeout)
                if r.status_code == 200:
                    results["entities"].append({"type": "username", "value": username, "details": {"platform": "Reddit", "profile": f"https://reddit.com/user/{username}"}})
                    results["relations"].append({"source": username, "target": f"https://reddit.com/user/{username}", "relation": "Reddit_profile"})
                    print(f"[+] Reddit account found for {username}")
                else:
                    print(f"[-] Reddit account not found for {username}")
            except Exception as e:
                print(f"[-] Error checking Reddit for {username}: {e}")
        if global_config.get("username_permutation_enabled"):
            variants = self.generate_permutations(username)
            for variant in variants:
                results["new_targets"].append(f"username:{variant}")
                results["relations"].append({"source": username, "target": variant, "relation": "username_variant"})
            if variants:
                print(f"[*] Generated {len(variants)} username variants for {username}")
        return results

    def generate_permutations(self, username):
        variants = []
        for suffix in ["123", "2023", "01"]:
            variants.append(username + suffix)
        if "." not in username:
            variants.append(username.replace("_", "."))
        if "_" not in username:
            variants.append(username.replace(".", "_"))
        return list(set(variants))
