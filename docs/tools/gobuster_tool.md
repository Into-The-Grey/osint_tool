# Gobuster Tool Documentation

## Overview

The Gobuster Tool performs directory and file enumeration on a target URL using the external Gobuster executable.

## Configuration

- **File**: `configs/gobuster_tool.json`
- **Example Content**:

  ```json
  {
    "gobuster_path": "/usr/bin/gobuster",
    "wordlist": "/path/to/wordlist.txt",
    "mode": "dir",
    "required": true
  }
  ```

- **gobuster_path**: Path to the Gobuster executable.
- **wordlist**: Path to the wordlist for enumeration.
- **mode**: Either `"dir"` (directory mode) or `"dns"` for subdomain enumeration.
- **required**: Set to `true` to enable the tool.

## Usage

Invoke the tool by running its `run()` method on a target URL.

## Logging

Output and errors are logged in `logs/gobuster_tool.log`.

---
