import phonenumbers
from phonenumbers import geocoder, carrier
from modules.base_module import BaseModule

class PhoneModule(BaseModule):
    def __init__(self):
        super().__init__("phone_module")

    def run(self, target, global_config):
        if not self.enabled:
            print("[*] PhoneModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}
        # Expect target in the format "phone:+1234567890"
        phone_number_str = target.split("phone:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        try:
            phone_obj = phonenumbers.parse(phone_number_str, None)
            region = geocoder.description_for_number(phone_obj, "en")
            carrier_name = carrier.name_for_number(phone_obj, "en")
            details = {
                "region": region,
                "carrier": carrier_name,
                "valid": phonenumbers.is_valid_number(phone_obj)
            }
            results["entities"].append({"type": "phone", "value": phone_number_str, "details": details})
            print(f"[+] Phone data retrieved for {phone_number_str}")
        except Exception as e:
            print(f"[-] Error processing phone number {phone_number_str}: {e}")
            results["entities"].append({"type": "phone", "value": phone_number_str, "details": {"error": str(e)}})
        return results
