# Email Module Documentation

## Overview

The Email Module queries an API (default is EmailRep.io) to retrieve reputation and breach data for an email address. It also extracts the local part and domain to trigger further scans.

## Configuration

- **File**: `configs/email_module.json`
- **Example Content**:

  ```json
  {
    "api_url": "https://emailrep.io/{email}",
    "required": true
  }
  ```

- **api_url**: Endpoint for the email reputation API. Use `{email}` as a placeholder.
- **required**: Set to `true` to mark this module as required.

## Usage

Targets must be formatted as:

```plaintext
email:someone@example.com
```

## Output

- **Entities**: An entity of type `email` with reputation and breach details.
- **New Targets**: The local part (username) and domain extracted from the email.
- **Relations**: Links from the email to its domain and local part.

---
