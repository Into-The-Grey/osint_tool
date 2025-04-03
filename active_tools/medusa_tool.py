import os
import json
import subprocess
import logging
import time


def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "medusa_tool.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


logger = logging.getLogger("MedusaTool")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "medusa_tool.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class MedusaTool:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config is not None
        self.name = "MedusaTool"

    def run(self, target):
        # Target is typically a domain for web application testing.
        if not self.enabled:
            logger.warning("MedusaTool is disabled (missing config).")
            return {"active_results": None}

        medusa_path = self.config.get("medusa_path", "medusa") # type: ignore
        options = self.config.get("options", "") # type: ignore

        command = f"{medusa_path} {options} -u {target}"
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
                logger.info("Medusa scan completed successfully.")
            else:
                logger.error(
                    f"Medusa scan failed with return code {result.returncode}: {result.stderr}"
                )
            return {"active_results": result.stdout}
        except Exception as e:
            logger.exception(f"Error executing Medusa scan: {e}")
            return {"active_results": None}
