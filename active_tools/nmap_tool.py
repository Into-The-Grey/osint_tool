import os
import json
import subprocess
import logging
import time


def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "nmap_tool.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


# Set up logger for Nmap Tool
logger = logging.getLogger("NmapTool")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "nmap_tool.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class NmapTool:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config is not None
        self.name = "NmapTool"

    def run(self, target):
        # For example, target may be an IP or domain.
        if not self.enabled:
            logger.warning("NmapTool is disabled (missing config).")
            return {"active_results": None}

        nmap_path = self.config.get("nmap_path", "nmap")
        options = self.config.get("scan_options", "-sV -O")

        command = f"{nmap_path} {options} {target}"
        logger.info(f"Executing command: {command}")

        try:
            start = time.time()
            result = subprocess.run(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                text=True,
            )
            end = time.time()
            logger.info(f"Command executed in {end - start:.2f} seconds.")
            if result.returncode == 0:
                logger.info("Nmap scan completed successfully.")
            else:
                logger.error(
                    f"Nmap scan failed with return code {result.returncode}: {result.stderr}"
                )
            return {"active_results": result.stdout}
        except Exception as e:
            logger.exception(f"Error executing Nmap scan: {e}")
            return {"active_results": None}
