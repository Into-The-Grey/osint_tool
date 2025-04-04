import requests
import os
import logging
from modules.base_module import BaseModule

# Setup logger for AddressModule
logger = logging.getLogger("AddressModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "address_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class AddressModule(BaseModule):
    def __init__(self):
        super().__init__("address_module")

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("AddressModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        # Extract the address from the target string (expected format: "address:...")
        address = target.split("address:")[1].strip()
        logger.info(f"Received address: {address}")

        # Process the address to check for completeness.
        # Split by commas and strip whitespace.
        parts = [part.strip() for part in address.split(",") if part.strip()]

        # If only the street is provided or if there are too few components,
        # append ", USA" as the default country.
        if len(parts) < 2:
            address += ", USA"
            logger.info(
                "Incomplete address detected (fewer than 2 parts). Appended default country 'USA'."
            )
        elif len(parts) == 2:
            # Assuming that two parts may be street and city,
            # append the default country.
            address += ", USA"
            logger.info(
                "Address appears incomplete (missing state/country). Appended default country 'USA'."
            )

        results = {"entities": [], "relations": [], "new_targets": []}

        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {"format": "json", "q": address, "addressdetails": 1}
            headers = {"User-Agent": global_config.get("user_agent", "OSINT Tool")}
            logger.info(f"Querying Nominatim API with address: {address}")
            resp = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=global_config.get("http_timeout", 10),
            )
            resp.raise_for_status()
            data = resp.json()

            if data:
                # Use the first result from the API response
                location = data[0]
                display_name = location.get("display_name")
                lat = location.get("lat")
                lon = location.get("lon")

                # Extract detailed address information if available
                addr_details = location.get("address", {})
                country = addr_details.get(
                    "country", "USA"
                )  # Default to USA if missing
                state = addr_details.get("state", "Unknown")
                city = (
                    addr_details.get("city")
                    or addr_details.get("town")
                    or addr_details.get("village")
                    or "Unknown"
                )

                details = {
                    "lat": lat,
                    "lon": lon,
                    "display_name": display_name,
                    "city": city,
                    "state": state,
                    "country": country,
                    "raw_address": addr_details,
                }
                results["entities"].append(
                    {"type": "address", "value": address, "details": details}
                )
                logger.info(f"Geocoding successful for address: {address}")
            else:
                logger.error(f"No geocoding results for address: {address}")
                results["entities"].append(
                    {
                        "type": "address",
                        "value": address,
                        "details": {"error": "No results"},
                    }
                )
        except Exception as e:
            logger.exception(f"Error geocoding address {address}: {e}")
            results["entities"].append(
                {"type": "address", "value": address, "details": {"error": str(e)}}
            )

        return results
