import requests
import re
import dns.resolver
import whois
from bs4 import BeautifulSoup
import os
import logging
import json
from modules.base_module import BaseModule

# Setup logger for DomainModule
logger = logging.getLogger("DomainModule")
logger.setLevel(logging.DEBUG)
log_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "domain_module.log"
)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class DomainModule(BaseModule):
    def __init__(self):
        super().__init__("domain_module")
        # Load configuration for DomainModule from JSON file.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "configs", "domain_module.json"
        )
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            logger.info("DomainModule configuration loaded successfully.")
        except Exception as e:
            logger.exception(f"Error loading domain module config: {e}")
            self.config = {}

    def run(self, target, global_config):
        if not self.enabled:
            logger.info("DomainModule is disabled (missing config).")
            return {"entities": [], "relations": [], "new_targets": []}

        domain = target.split("domain:")[1].strip()
        results = {"entities": [], "relations": [], "new_targets": []}
        headers = {"User-Agent": global_config.get("user_agent", "OSINT Tool")}
        timeout = global_config.get("http_timeout", 10)

        # WHOIS lookup
        try:
            logger.info(f"Performing WHOIS lookup for domain: {domain}")
            whois_data = whois.whois(domain)
            details = {
                "registrar": whois_data.get("registrar"),
                "creation_date": str(whois_data.get("creation_date")),
                "expiration_date": str(whois_data.get("expiration_date")),
                "name_servers": whois_data.get("name_servers"),
            }
            results["entities"].append(
                {"type": "domain", "value": domain, "details": details}
            )
            logger.info(f"WHOIS data retrieved for {domain}: {details}")
        except Exception as e:
            logger.exception(f"Error during WHOIS lookup for {domain}: {e}")
            results["entities"].append(
                {"type": "domain", "value": domain, "details": {"error": str(e)}}
            )

        # DNS A record lookup
        try:
            logger.info(f"Resolving DNS A records for {domain}")
            answers = dns.resolver.resolve(domain, "A")
            ips = [rdata.to_text() for rdata in answers]
            results["entities"].append(
                {
                    "type": "ip",
                    "value": ", ".join(ips),
                    "details": {"source": "DNS A records"},
                }
            )
            for ip in ips:
                results["relations"].append(
                    {"source": domain, "target": ip, "relation": "resolves_to"}
                )
            logger.info(f"DNS A records for {domain}: {ips}")
        except Exception as e:
            logger.exception(f"DNS lookup error for {domain}: {e}")

        # Homepage scraping (if enabled)
        if self.config.get("scrape_homepage", True):
            try:
                url = f"http://{domain}"
                logger.info(f"Fetching homepage for {domain} at {url}")
                resp = requests.get(url, headers=headers, timeout=timeout)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text()
                    emails = re.findall(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", text
                    )
                    emails = list(set(emails))
                    for email in emails:
                        results["new_targets"].append(f"email:{email}")
                        results["relations"].append(
                            {
                                "source": domain,
                                "target": email,
                                "relation": "homepage_email",
                            }
                        )
                    logger.info(f"Found emails on {domain}: {emails}")
                else:
                    logger.error(
                        f"Homepage request for {domain} returned status {resp.status_code}"
                    )
            except Exception as e:
                logger.exception(f"Error fetching homepage for {domain}: {e}")

        return results
