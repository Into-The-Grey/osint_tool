import requests
import os
import logging
import json
from modules.base_module import BaseModule

# Setup logger for UsernameModule
logger = logging.getLogger("UsernameModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "username_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class UsernameModule(BaseModule):
    def __init__(self):
        super().__init__("username_module")
        # Load sites list from the JSON configuration.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "configs",
            "username_module.json",
        )
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
                self.sites = config_data.get("sites", [])
        except Exception as e:
            logger.exception(f"Error loading sites from config: {e}")
            self.sites = []

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("UsernameModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        username = target.split("username:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {"User-Agent": global_config.get("user_agent", "OSINT Tool")}
        timeout = global_config.get("http_timeout", 10)

        # Iterate over the sites loaded from configuration.
        for site in self.sites:
            site_name = site.get("name")
            url_template = site.get("url")
            false_positive_signatures = site.get("false_positive_signatures", [])
            profile_url = url_template.format(username=username)
            try:
                logger.info(
                    f"Checking {site_name} profile for '{username}' at {profile_url}"
                )
                response = requests.get(profile_url, headers=headers, timeout=timeout)
                valid = self.validate_profile(
                    response, false_positive_signatures, site_name
                )
                if valid:
                    results["entities"].append(
                        {
                            "type": "username",
                            "value": username,
                            "details": {"platform": site_name, "profile": profile_url},
                        }
                    )
                    results["relations"].append(
                        {
                            "source": username,
                            "target": profile_url,
                            "relation": f"{site_name}_profile",
                        }
                    )
                    logger.info(f"{site_name} account found for '{username}'")
                else:
                    logger.info(
                        f"{site_name} account not found for '{username}' (false positive detected)"
                    )
            except Exception as e:
                logger.exception(f"Error checking {site_name} for '{username}': {e}")

        # Generate username variants if enabled in global config.
        if global_config.get("username_permutation_enabled"):
            variants = self.generate_permutations(username)
            for variant in variants:
                results["new_targets"].append(f"username:{variant}")
                results["relations"].append(
                    {
                        "source": username,
                        "target": variant,
                        "relation": "username_variant",
                    }
                )
            if variants:
                logger.info(
                    f"Generated {len(variants)} username variants for '{username}'"
                )

        return results

    def generate_permutations(self, username):
        variants = []
        # Basic numeric suffixes
        for suffix in ["123", "2023", "01", "007", "999"]:
            variants.append(username + suffix)
        # Swap underscores and dots
        if "_" not in username and "." in username:
            variants.append(username.replace(".", "_"))
        if "." not in username and "_" in username:
            variants.append(username.replace("_", "."))
        # Additional common variations
        variants.append(username.lower())
        variants.append(username.upper())
        return list(set(variants))

    def validate_profile(self, response, false_positive_signatures, site_name):
        """
        Validate that a profile exists by:
         - Checking the HTTP status code.
         - If the status code is 404, it's not found.
         - For sites that return 200 even when the account does not exist,
           inspect the response text for known false positive phrases.
        """
        if response.status_code == 404:
            return False

        # For sites like Reddit, if the JSON contains an error, mark as not found.
        if site_name == "Reddit":
            try:
                data = response.json()
                if "error" in data:
                    return False
            except Exception:
                return False

        response_text = response.text.lower()
        for signature in false_positive_signatures:
            if signature.lower() in response_text:
                return False

        return True
