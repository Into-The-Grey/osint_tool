# IP Module Documentation

## Overview

The IP Module uses the IPWhois library to retrieve detailed information (ASN, country, etc.) about an IP address.

## Configuration

- **File**: `configs/ip_module.json`
- **Example Content**:

  ```json
  {
    "required": true
  }
  ```

## Usage

Targets must be formatted as:

```plaintext
ip:1.2.3.4
```

## Output

- **Entities**: An `ip` entity with details such as ASN, description, and network information.

---
