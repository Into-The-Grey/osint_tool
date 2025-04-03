# Real Name Module Documentation

## Overview

The Real Name Module uses the Wikipedia API to search for a real name and retrieve related information such as titles and snippets.

## Configuration

- **File**: `configs/realname_module.json`
- **Example Content**:

  ```json
  {
    "required": true
  }
  ```

## Usage

Targets must be formatted as:

```plaintext
realname:John Doe
```

## Output

- **Entities**: A `realname` entity with details derived from Wikipedia search results.

---
