# Address Module Documentation

## Overview

The Address Module uses the OpenStreetMap Nominatim API to geocode physical addresses and return location details.

## Configuration

- **File**: `configs/address_module.json`
- **Example Content**:

  ```json
  {
    "required": true
  }
  ```

## Usage

Targets must be formatted as:

```plaintext
address:123 Main St, City, Country
```

## Output

- **Entities**: An `address` entity with geocoding details such as latitude, longitude, and display name.

---
