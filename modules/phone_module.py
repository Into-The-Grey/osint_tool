import phonenumbers
from phonenumbers import geocoder, carrier
import os
import logging
import json
from modules.base_module import BaseModule

# Setup logger for PhoneModule
logger = logging.getLogger("PhoneModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "phone_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class PhoneModule(BaseModule):
    def __init__(self):
        super().__init__("phone_module")
        # Load configuration for PhoneModule from JSON file.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs", "phone_module.json"
        )
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("PhoneModule configuration loaded successfully.")
        except Exception as e:
            logger.exception(f"Error loading phone module config: {e}")
            self.config = {}

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("PhoneModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        # Expect target in the format "phone:+1234567890"
        phone_number_str = target.split("phone:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}

        # Use the default region from the PhoneModule configuration, if provided.
        default_region = self.config.get("default_region", None)

        try:
            phone_obj = phonenumbers.parse(phone_number_str, default_region)
            region = geocoder.description_for_number(phone_obj, "en")
            carrier_name = carrier.name_for_number(phone_obj, "en")
            details = {
                "region": region,
                "carrier": carrier_name,
                "valid": phonenumbers.is_valid_number(phone_obj),
            }
            results["entities"].append(
                {"type": "phone", "value": phone_number_str, "details": details}
            )
            logger.info(f"Phone data retrieved for {phone_number_str}: {details}")
        except Exception as e:
            logger.exception(f"Error processing phone number {phone_number_str}: {e}")
            results["entities"].append(
                {
                    "type": "phone",
                    "value": phone_number_str,
                    "details": {"error": str(e)},
                }
            )

        return results
