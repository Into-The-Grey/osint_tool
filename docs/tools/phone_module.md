# Phone Module Documentation

## Overview

The Phone Module utilizes the `phonenumbers` library to validate and obtain details (region, carrier, validity) for a given phone number.

## Configuration

- **File**: `configs/phone_module.json`
- **Example Content**:

  ```json
  {
    "required": true
  }
  ```

## Usage

Targets must be formatted as:

```plaintext
phone:+1234567890
```

## Output

- **Entities**: A `phone` entity with details like region, carrier, and validity status.

---
