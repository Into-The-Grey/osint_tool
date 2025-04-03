# OSINT Tool Documentation

This document provides instructions for installing, configuring, and using the OSINT Tool. It also links to detailed documentation for each module under **docs/tools/**.

The OSINT Tool is designed to be modular and extensible, allowing users to gather open-source intelligence on various target types. It can be run in both command-line interface (CLI) mode and web UI mode, making it versatile for different use cases.

The tool supports scanning for:

- Email addresses
- Usernames
- Domains
- IP addresses
- Phone numbers
- Street addresses
- Real names

In addition to these passive modules, the tool includes several **active** (or "risky") utilities:

- **Nmap Tool**: Performs active port scanning and service detection.
- **Gobuster Tool**: Conducts directory and file enumeration.
- **Nikto Tool**: Scans web servers for vulnerabilities.
- **Hydra Tool**: Executes brute-force attacks against network services.
- **Medusa Tool**: Tests web applications for vulnerabilities.

Each module and active tool loads its configuration from the **configs/** folder and writes detailed logs to its own logfile in the **logs/** folder.

## Table of Contents

- [OSINT Tool Documentation](#osint-tool-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
    - [CLI Mode](#cli-mode)
    - [Web UI Mode](#web-ui-mode)
  - [Configuration](#configuration)
  - [Modules and Tools](#modules-and-tools)
    - [Passive Modules](#passive-modules)
    - [Active Tools](#active-tools)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

## Introduction

The OSINT Tool is a modular, extensible application for gathering open‑source intelligence. It supports scanning for email addresses, usernames, domains, IP addresses, phone numbers, street addresses, and real names using passive techniques. In addition, it provides active utilities (such as Nmap, Gobuster, Nikto, Hydra, and Medusa) for more advanced testing scenarios. **Warning:** Active tools may perform intrusive scans. Ensure you have authorization before using them.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd osint_tool
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install required packages individually:*

   ```bash
   pip install requests beautifulsoup4 dnspython networkx python-whois stem flask pyvis ipwhois phonenumbers
   ```

3. **Install and configure Tor** (if using dark web scanning):

   ```bash
   sudo apt-get install tor
   ```

## Usage

### CLI Mode

Run the tool with one or more targets:

```bash
python main.py -t email:john.doe@example.com -t ip:8.8.8.8 -t phone:+1234567890 -t address:"1600 Amphitheatre Parkway, Mountain View, CA" -t realname:"John Doe" --darkweb --permutations --output results.json
```

### Web UI Mode

Run the web UI:

```bash
python webapp.py
```

Then open your browser and navigate to [http://0.0.0.0:5000](http://0.0.0.0:5000).

## Configuration

Configuration files are located in the **configs/** folder:

- **global_config.json** holds global settings.
- Each module (passive or active) has its own configuration file (e.g., **email_module.json**, **nmap_tool.json**).  
If a module’s config file is missing, that module will be disabled.

## Modules and Tools

### Passive Modules

- **Email Module**: [Documentation](tools/email_module.md)
- **Username Module**: [Documentation](tools/username_module.md)
- **Domain Module**: [Documentation](tools/domain_module.md)
- **IP Module**: [Documentation](tools/ip_module.md)
- **Phone Module**: [Documentation](tools/phone_module.md)
- **Address Module**: [Documentation](tools/address_module.md)
- **Real Name Module**: [Documentation](tools/realname_module.md)

### Active Tools

- **Nmap Tool**: [Documentation](tools/nmap_tool.md)
- **Gobuster Tool**: [Documentation](tools/gobuster_tool.md)
- **Nikto Tool**: [Documentation](tools/nikto_tool.md)
- **Hydra Tool**: [Documentation](tools/hydra_tool.md)
- **Medusa Tool**: [Documentation](tools/medusa_tool.md)

## Troubleshooting

- Ensure all dependencies are installed.
- Verify that Tor is installed if dark web scanning is enabled.
- Check the **configs/** folder to confirm that configuration files exist for the modules you wish to use.
- Review individual logfiles in the **logs/** folder for detailed error messages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
