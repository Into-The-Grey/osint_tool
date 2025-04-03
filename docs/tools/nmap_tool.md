# Nmap Tool Documentation

## Overview

The Nmap Tool provides active port scanning and service detection. It uses the external Nmap executable and logs detailed scan output.

## Configuration

- **File**: `configs/nmap_tool.json`
- **Example Content**:

  ```json
  {
    "nmap_path": "/usr/bin/nmap",
    "scan_options": "-sV -O",
    "required": true
  }
  ```

- **nmap_path**: Path to the Nmap executable.
- **scan_options**: Default scan options (e.g., version detection and OS fingerprinting).
- **required**: Set to `true` to enable the tool.

## Usage

Run the Nmap tool on a target (IP or domain) by calling its `run()` method.
Example CLI:

```bash
python main.py -t ip:8.8.8.8
```

Then, from your active tools interface, the Nmap tool can be triggered for further analysis.

## Logging

All output is written to `logs/nmap_tool.log` for troubleshooting.

---
