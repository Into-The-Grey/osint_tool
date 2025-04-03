# Username Module Documentation

## Overview

The Username Module checks for user accounts on platforms such as GitHub and Reddit. It can also generate permutations (variants) of a username if enabled.

## Configuration

- **File**: `configs/username_module.json`
- **Example Content**:

  ```json
  {
    "check_github": true,
    "check_reddit": true,
    "required": true
  }
  ```

- **check_github**: Boolean flag to enable checking on GitHub.
- **check_reddit**: Boolean flag to enable checking on Reddit.
- **required**: Module is required if set to `true`.

## Usage

Targets must be formatted as:

```plaintext
username:someuser
```

## Output

- **Entities**: A `username` entity with details from GitHub/Reddit.
- **New Targets**: Additional username variants if permutations are enabled.
- **Relations**: Links between the original username and found profiles/variants.

---
