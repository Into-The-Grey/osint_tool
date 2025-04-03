# Medeusa Tool Documentation

## Overview

The Medeusa Tool tests web applications for vulnerabilities. This is an active tool and should only be used on authorized targets.

## Configuration

- **File**: `configs/medeusa_tool.json`
- **Example Content**:

  ```json
  {
    "medeusa_path": "/usr/bin/medeusa",
    "options": "--force",
    "required": false
  }
  ```

- **medeusa_path**: Path to the Medeusa executable.
- **options**: Additional options to pass to Medeusa.
- **required**: Set to `false` by default.

## Usage

Run the Medeusa tool on a target URL by invoking its `run()` method.

## Logging

Scan output is logged in `logs/medeusa_tool.log`.

---
