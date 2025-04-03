import os
import json
import subprocess
import logging
import time


def load_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "configs", "gobuster_tool.json"
    )
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return None


logger = logging.getLogger("GobusterTool")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "gobuster_tool.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class GobusterTool:
    def __init__(self):
        self.config = load_config()
        self.enabled = self.config is not None
        self.name = "GobusterTool"

    def run(self, target):
        # Target is typically a domain (or URL) for directory enumeration.
        if not self.enabled:
            logger.warning("GobusterTool is disabled (missing config).")
            return {"active_results": None}

        gobuster_path = self.config.get("gobuster_path", "gobuster") # type: ignore
        mode = self.config.get("mode", "dir") # type: ignore
        wordlist = self.config.get("wordlist", "") # type: ignore

        command = f"{gobuster_path} {mode} -u {target} -w {wordlist}"
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
                logger.info("Gobuster scan completed successfully.")
            else:
                logger.error(
                    f"Gobuster scan failed with return code {result.returncode}: {result.stderr}"
                )
            return {"active_results": result.stdout}
        except Exception as e:
            logger.exception(f"Error executing Gobuster scan: {e}")
            return {"active_results": None}
