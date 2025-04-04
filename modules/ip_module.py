import os
import logging
import json
from ipwhois import IPWhois
from modules.base_module import BaseModule

# Setup logger for IPModule
logger = logging.getLogger("IPModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "ip_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class IPModule(BaseModule):
    def __init__(self):
        super().__init__("ip_module")
        # Load configuration for IPModule from JSON file.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs", "ip_module.json"
        )
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("IPModule configuration loaded successfully.")
        except Exception as e:
            logger.exception(f"Error loading IPModule config: {e}")
            self.config = {}

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("IPModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        # Expect target in the format "ip:1.2.3.4"
        ip_addr = target.split("ip:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        try:
            logger.info(f"Starting IP lookup for {ip_addr}")
            obj = IPWhois(ip_addr)
            details = obj.lookup_whois()
            summary = {
                "asn": details.get("asn"),
                "asn_description": details.get("asn_description"),
                "country": details.get("asn_country_code"),
                "nets": details.get("nets"),
            }
            results["entities"].append(
                {"type": "ip", "value": ip_addr, "details": summary}
            )
            logger.info(f"IP data retrieved for {ip_addr}")
        except Exception as e:
            logger.exception(f"Error looking up IP {ip_addr}: {e}")
            results["entities"].append(
                {"type": "ip", "value": ip_addr, "details": {"error": str(e)}}
            )
        return results
