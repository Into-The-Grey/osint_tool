import os
import json
import logging


class BaseModule:
    def __init__(self, module_name):
        self.name = module_name
        self.enabled = False
        self.config = self.load_module_config(module_name)

    def load_module_config(self, module_name):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(base_dir, "configs", f"{module_name.lower()}.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                self.enabled = True
                return config
            except Exception as e:
                logging.error(f"Error loading config file for {module_name}: {e}")
                self.enabled = False
                return {}
        else:
            logging.warning(
                f"[!] Config file for {module_name} not found at {config_path}. Module disabled."
            )
            self.enabled = False
            return {}

    def run(self, target, global_config):
        raise NotImplementedError("Subclasses must implement the run() method.")
