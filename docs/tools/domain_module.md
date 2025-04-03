# Domain Module Documentation

## Overview

The Domain Module performs WHOIS lookups, DNS queries, and optionally scrapes the homepage of a domain to retrieve associated data.

## Configuration

- **File**: `configs/domain_module.json`
- **Example Content**:

  ```json
  {
    "scrape_homepage": true,
    "required": true
  }
  ```

- **scrape_homepage**: Boolean flag to enable homepage scraping for email extraction.
- **required**: Module is required if set to `true`.

## Usage

Targets must be formatted as:

```plaintext
domain:example.com
```

## Output

- **Entities**: A `domain` entity with WHOIS details.
- **Entities**: An `ip` entity for DNS A record data.
- **New Targets**: Email addresses found on the homepage.
- **Relations**: Links connecting the domain with its DNS and email data.

---
