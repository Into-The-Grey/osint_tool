# Nikto Tool Documentation

## Overview

The Nikto Tool scans web servers for vulnerabilities using the Nikto scanner.

## Configuration

- **File**: `configs/nikto_tool.json`
- **Example Content**:

  ```json
  {
    "nikto_path": "/usr/bin/nikto",
    "scan_options": "-Tuning 1234",
    "required": true
  }
  ```

- **nikto_path**: Path to the Nikto executable.
- **scan_options**: Command-line options for the scan.
- **required**: Set to `true` to enable the tool.

## Usage

Run the Nikto tool on a target domain or URL by invoking its `run()` method.

## Logging

All scan output is logged in `logs/nikto_tool.log`.

---
