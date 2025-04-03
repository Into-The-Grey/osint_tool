# Hydra Tool Documentation

## Overview

The Hydra Tool performs brute-force password attacks against network services. Use with extreme caution and only on systems you have explicit permission to test.

## Configuration

- **File**: `configs/hydra_tool.json`
- **Example Content**:

  ```json
  {
    "hydra_path": "/usr/bin/hydra",
    "protocols": ["ssh", "ftp"],
    "default_userlist": "/path/to/userlist.txt",
    "default_passlist": "/path/to/passlist.txt",
    "required": false
  }
  ```

- **hydra_path**: Path to the Hydra executable.
- **protocols**: List of protocols to target (e.g., SSH, FTP).
- **default_userlist** and **default_passlist**: Paths to wordlists.
- **required**: Set to `false` by default since this tool is highly risky.

## Usage

Invoke the Hydra tool by running its `run()` method with a target (e.g., "ssh:192.168.1.100").

## Logging

Output is written to `logs/hydra_tool.log`.

---
