import subprocess
import time
import logging
import os

# Set up logger for the Tor Controller
logger = logging.getLogger("TorController")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(os.path.dirname(__file__), "..", "logs", "tor_controller.log")
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class TorController:
    def __init__(self):
        self.process = None

    def start(self):
        logger.info("Starting Tor process...")
        try:
            # Launch Tor; ensure that the 'tor' executable is in your system PATH.
            self.process = subprocess.Popen(
                ["tor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            # Wait for a few seconds to allow Tor to fully initialize.
            time.sleep(5)
            logger.info("Tor started successfully.")
        except Exception as e:
            logger.error(f"Error starting Tor: {e}")

    def stop(self):
        if self.process:
            logger.info("Stopping Tor process...")
            self.process.terminate()
            self.process.wait()
            logger.info("Tor stopped.")
