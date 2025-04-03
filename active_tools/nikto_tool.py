import os
import json
import subprocess
import logging
import time


def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "nikto_tool.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


logger = logging.getLogger("NiktoTool")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "nikto_tool.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class NiktoTool:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config is not None
        self.name = "NiktoTool"

    def run(self, target):
        # Target is a domain or URL.
        if not self.enabled:
            logger.warning("NiktoTool is disabled (missing config).")
            return {"active_results": None}

        nikto_path = self.config.get("nikto_path", "nikto")
        options = self.config.get("scan_options", "")

        command = f"{nikto_path} {options} -h {target}"
        logger.info(f"Executing command: {command}")

        try:
            start = time.time()
            result = subprocess.run(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                text=True,
            )
            end = time.time()
            logger.info(f"Command executed in {end - start:.2f} seconds.")
            if result.returncode == 0:
                logger.info("Nikto scan completed successfully.")
            else:
                logger.error(
                    f"Nikto scan failed with return code {result.returncode}: {result.stderr}"
                )
            return {"active_results": result.stdout}
        except Exception as e:
            logger.exception(f"Error executing Nikto scan: {e}")
            return {"active_results": None}
