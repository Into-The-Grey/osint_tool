import requests
import os
import logging
import json
from modules.base_module import BaseModule

# Setup logger for RealNameModule
logger = logging.getLogger("RealNameModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "realname_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class RealNameModule(BaseModule):
    def __init__(self):
        super().__init__("realname_module")
        # Load configuration for RealNameModule from JSON file.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "configs",
            "realname_module.json",
        )
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("RealNameModule configuration loaded successfully.")
        except Exception as e:
            logger.exception(f"Error loading realname module config: {e}")
            self.config = {}

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("RealNameModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        # Expect target in the format "realname:John Doe"
        realname = target.split("realname:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}

        # Use the configured Wikipedia API URL or default to Wikipedia's API.
        api_url = self.config.get(
            "wikipedia_api_url", "https://en.wikipedia.org/w/api.php"
        )
        params = {
            "action": "query",
            "list": "search",
            "srsearch": realname,
            "format": "json",
        }
        headers = {"User-Agent": global_config.get("user_agent", "OSINT Tool")}
        timeout = global_config.get("http_timeout", 10)

        try:
            logger.info(
                f"Querying Wikipedia API at {api_url} for real name: {realname}"
            )
            resp = requests.get(
                api_url, params=params, headers=headers, timeout=timeout
            )
            resp.raise_for_status()
            data = resp.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                first = search_results[0]
                details = {"title": first.get("title"), "snippet": first.get("snippet")}
                results["entities"].append(
                    {"type": "realname", "value": realname, "details": details}
                )
                logger.info(f"Wikipedia result found for real name: {realname}")
            else:
                logger.warning(f"No Wikipedia results found for real name: {realname}")
                results["entities"].append(
                    {
                        "type": "realname",
                        "value": realname,
                        "details": {"error": "No results"},
                    }
                )
        except Exception as e:
            logger.exception(f"Error querying Wikipedia for real name {realname}: {e}")
            results["entities"].append(
                {"type": "realname", "value": realname, "details": {"error": str(e)}}
            )

        return results
