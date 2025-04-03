# OSINT Tool

[![OSINT Tool Logo](https://img.shields.io/badge/OSINT%20Tool-Modular-blue?logo=opensourceinitiative)](https://github.com/your-repo-url)
[![Nmap](https://img.shields.io/badge/Nmap-active%20scanning-brightgreen?logo=nmap)](https://nmap.org)
[![Gobuster](https://img.shields.io/badge/Gobuster-directory--enumeration-orange?logo=github)](https://github.com/OJ/gobuster)
[![Nikto](https://img.shields.io/badge/Nikto-web%20vulnerability-red?logo=nikto)](https://cirt.net/Nikto2)
[![Hydra](https://img.shields.io/badge/Hydra-brute--force-purple?logo=github)](https://github.com/vanhauser-thc/thc-hydra)
[![Medeusa](https://img.shields.io/badge/Medeusa-web--scanner-blueviolet?logo=github)](https://github.com/lanmaster53/medeusa)
[![Flask](https://img.shields.io/badge/Flask-web%20UI-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![PyVis](https://img.shields.io/badge/PyVis-graph%20visualization-yellow?logo=pyvis)](https://pyvis.readthedocs.io/)

---

## Overview

The OSINT Tool is a modular and extensible open‑source intelligence gathering platform that combines both passive and active scanning capabilities. It is designed to automatically analyze provided inputs, dynamically discover additional targets, and correlate findings through a unified knowledge graph.

## Capabilities

### Passive Intelligence Gathering

- **Email Module:**  
  Retrieves reputation and breach data for email addresses and extracts associated details such as domain and local part.
- **Username Module:**  
  Searches for user profiles across public platforms (e.g., GitHub, Reddit) and generates username variants.
- **Domain Module:**  
  Conducts WHOIS lookups, DNS queries, and scrapes website content for additional intelligence.
- **IP Module:**  
  Retrieves detailed IP information, including ASN data and network characteristics.
- **Phone Module:**  
  Validates phone numbers and gathers related information using robust parsing libraries.
- **Address Module:**  
  Geocodes street addresses via the OpenStreetMap Nominatim API to obtain geographic details.
- **Real Name Module:**  
  Searches for public records and relevant information (e.g., from Wikipedia) associated with real names.

### Active Scanning Capabilities

- **Nmap Tool:**  
  Performs active port scanning and service detection.
- **Gobuster Tool:**  
  Enumerates directories and files on web servers.
- **Nikto Tool:**  
  Scans web servers for known vulnerabilities.
- **Hydra Tool:**  
  Executes brute-force attacks against network services (active use requires explicit authorization).
- **Medeusa Tool:**  
  Tests web applications for potential vulnerabilities (active use requires explicit authorization).

### Dynamic Discovery and Correlation

- **Automatic Expansion:**  
  The tool dynamically discovers additional targets during a scan (e.g., discovering a phone number associated with an email) and automatically initiates further searches.
- **Knowledge Graph:**  
  All discovered entities and their relationships are aggregated into a NetworkX-based graph for comprehensive correlation and visualization.

### User Interfaces

- **Command-Line Interface (CLI):**  
  Run scans directly via the terminal.
- **Web User Interface (Web UI):**  
  A modern, responsive interface built with Flask and Bootstrap. It includes interactive visualizations powered by PyVis, as well as dedicated pages for configuring settings and viewing detailed logs.

### Modular Architecture

- **Independent Configuration:**  
  Each module (passive and active) is individually configurable through JSON files stored in the `configs/` folder.
- **Extensibility:**  
  The modular design makes it easy to add or update scanning modules and active tools without disrupting the core functionality.

## Additional Information

For detailed usage instructions, please refer to the [usage.md](docs/usage.md) file.  
For license information, please see the [LICENSE](docs/LICENSE) file.  
For contribution guidelines, please check the [CONTRIBUTING.md](docs/CONTRIBUTING.md) file.
