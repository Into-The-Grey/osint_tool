import os
import json

def load_config(args):
    # Base configuration from command-line arguments.
    config = {
        "dark_web_enabled": args.darkweb,
        "username_permutation_enabled": args.permutations,
        "output_file": args.output,
        "http_timeout": 10,
        "user_agent": "Mozilla/5.0 (OSINTTool)"
    }
    # Load global configuration if available.
    global_config_path = os.path.join(os.path.dirname(__file__), "configs", "global_config.json")
    if os.path.exists(global_config_path):
        with open(global_config_path, "r") as f:
            global_config = json.load(f)
        config.update(global_config)
    return config
