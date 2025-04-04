import requests
import os
import logging
import json
from modules.base_module import BaseModule

# Setup logger for EmailModule
logger = logging.getLogger("EmailModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "email_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class EmailModule(BaseModule):
    def __init__(self):
        super().__init__("email_module")
        # Load configuration for EmailModule from JSON file.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs", "email_module.json"
        )
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("EmailModule configuration loaded successfully.")
        except Exception as e:
            logger.exception(f"Error loading email module config: {e}")
            self.config = {}

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("EmailModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        # Expect target in the format "email:john.doe@example.com"
        email = target.split("email:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {
            "User-Agent": global_config.get("user_agent", "OSINT Tool"),
            "Accept": "application/json",
        }
        timeout = global_config.get("http_timeout", 10)

        # Build the API URL from the configuration (substitute {email} placeholder)
        api_url_template = self.config.get("api_url", "https://emailrep.io/{email}")
        api_url = api_url_template.replace("{email}", email)
        logger.info(f"Querying Email API at {api_url} for {email}")

        try:
            response = requests.get(api_url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                rep_data = response.json()
                details = {
                    "reputation": rep_data.get("reputation"),
                    "suspicious": rep_data.get("suspicious"),
                    "details": rep_data.get("details"),
                    "references": rep_data.get("references"),
                }
                results["entities"].append(
                    {"type": "email", "value": email, "details": details}
                )
                logger.info(f"Email data retrieved for {email}")
            else:
                logger.error(f"API returned status {response.status_code} for {email}")
                results["entities"].append(
                    {
                        "type": "email",
                        "value": email,
                        "details": {"error": "No data retrieved"},
                    }
                )
        except Exception as e:
            logger.exception(f"Error querying API for {email}: {e}")
            results["entities"].append(
                {"type": "email", "value": email, "details": {"error": str(e)}}
            )

        # If the email contains '@', split into local part and domain, and add them as new targets.
        if "@" in email:
            local_part, domain = email.split("@", 1)
            results["new_targets"].extend(
                [f"username:{local_part}", f"domain:{domain}"]
            )
            results["relations"].append(
                {"source": email, "target": domain, "relation": "email_domain"}
            )
            results["relations"].append(
                {"source": email, "target": local_part, "relation": "email_localpart"}
            )

        return results
