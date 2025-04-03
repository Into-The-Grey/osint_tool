# OSINT Tool

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
