import os
import json
import subprocess
import logging
import time


def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "hydra_tool.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


logger = logging.getLogger("HydraTool")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "hydra_tool.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class HydraTool:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config is not None
        self.name = "HydraTool"

    def run(self, target):
        # Target is expected to be a service endpoint (e.g., "ssh:192.168.1.100")
        if not self.enabled:
            logger.warning("HydraTool is disabled (missing config).")
            return {"active_results": None}

        hydra_path = self.config.get("hydra_path", "hydra") # type: ignore
        protocols = self.config.get("protocols", []) # type: ignore
        userlist = self.config.get("default_userlist", "") # type: ignore
        passlist = self.config.get("default_passlist", "") # type: ignore

        # This example assumes a simple scenario: use the first protocol in the list.
        if not protocols:
            logger.error("No protocols defined in configuration for HydraTool.")
            return {"active_results": None}
        protocol = protocols[0]

        command = f"{hydra_path} -L {userlist} -P {passlist} {target} {protocol}"
        logger.info(f"Executing command: {command}")

        try:
            start = time.time()
            result = subprocess.run(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=180,
                text=True,
            )
            end = time.time()
            logger.info(f"Command executed in {end - start:.2f} seconds.")
            if result.returncode == 0:
                logger.info("Hydra scan completed successfully.")
            else:
                logger.error(
                    f"Hydra scan failed with return code {result.returncode}: {result.stderr}"
                )
            return {"active_results": result.stdout}
        except Exception as e:
            logger.exception(f"Error executing Hydra scan: {e}")
            return {"active_results": None}
