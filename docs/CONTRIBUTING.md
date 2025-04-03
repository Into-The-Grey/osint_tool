# Contributing to OSINT Tool

Thank you for your interest in contributing to the OSINT Tool project! Our goal is to create a robust, modular, and extensible open‑source intelligence platform that combines passive scanning and active testing utilities in one unified tool. This document outlines guidelines and best practices for contributing code, documentation, and ideas to this project.

---

## Table of Contents

- [Contributing to OSINT Tool](#contributing-to-osint-tool)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [How to Contribute](#how-to-contribute)
    - [Reporting Issues and Feature Requests](#reporting-issues-and-feature-requests)
    - [Submitting Pull Requests](#submitting-pull-requests)
  - [Development Guidelines](#development-guidelines)
    - [Project Structure](#project-structure)
    - [Coding Style](#coding-style)
    - [Documentation](#documentation)
    - [Testing](#testing)
  - [Branching and Commit Guidelines](#branching-and-commit-guidelines)
  - [Module Contributions](#module-contributions)
  - [Active Tools Contributions](#active-tools-contributions)
  - [Additional Resources](#additional-resources)

---

## Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read and follow it in all your interactions related to this project.

---

## How to Contribute

### Reporting Issues and Feature Requests

- **Issues:**  
  If you encounter a bug, please open an issue on GitHub. Include clear steps to reproduce the problem, any relevant error logs, and your environment details.
  
- **Feature Requests:**  
  If you have an idea for a new module, active tool, or an enhancement, open an issue and describe your idea in detail. We encourage discussion before major work begins.

### Submitting Pull Requests

1. **Fork the Repository:**  
   Create a personal fork of the project and clone it to your local machine.
2. **Create a Feature or Bugfix Branch:**  
   Use a descriptive branch name (e.g., `feature/add-new-email-module` or `bugfix/fix-name-parsing`).
3. **Implement Your Changes:**  
   Follow the development guidelines outlined below.
4. **Commit Your Changes:**  
   Write clear, descriptive commit messages (see [Branching and Commit Guidelines](#branching-and-commit-guidelines)).
5. **Submit a Pull Request:**  
   Open a pull request on GitHub with a detailed description of your changes and reference any related issues.
6. **Respond to Feedback:**  
   Be prepared to answer questions or make adjustments based on reviewer feedback.

---

## Development Guidelines

### Project Structure

The OSINT Tool is organized into several key directories:

- **configs/**  
  Contains JSON configuration files for each module and active tool. Each module loads its configuration from this folder. If a configuration file is missing, the module should disable itself gracefully.

- **modules/**  
  Houses passive scanning modules (e.g., email, username, domain, IP, phone, address, real name).

- **active_tools/**  
  Contains active (and potentially risky) tools such as Nmap, Gobuster, Nikto, Hydra, and Medeusa. Each tool has its own configuration and dedicated logfile.

- **utils/**  
  Includes shared utilities like the GraphBuilder, Module Registry, Output Manager, and Tor Controller.

- **logs/**  
  Active tools and utilities log detailed output to individual files here.

- **docs/**  
  Contains usage guides and per-tool documentation.

- **templates/**  
  Holds the Flask web UI templates.

### Coding Style

- **Language:** Python 3.x  
- **Style Guidelines:** Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Docstrings:** All functions, classes, and modules should have clear docstrings.
- **Imports:** Organize imports in three sections: standard libraries, third-party packages, and local modules.
- **File Naming:** Use lowercase names with underscores (e.g., `email_module.py`).

### Documentation

- **In-code Documentation:**  
  Ensure every module and function includes appropriate docstrings.
  
- **External Documentation:**  
  Update documentation in the **docs/** folder whenever you add or modify functionality. For example, if you add a new module, add or update the corresponding file in **docs/tools/**. The main [usage.md](docs/usage.md) should also be kept current.

### Testing

- **Manual Testing:**  
  Test your changes locally using both CLI and Web UI modes.
  
- **Automated Testing:**  
  Where possible, add unit tests or integration tests for new functionality. Create tests in a dedicated **tests/** folder if applicable.
  
- **Logging:**  
  Make sure any new active tools produce clear log output in the **logs/** folder.

---

## Branching and Commit Guidelines

- **Branch Naming:**  
  Use descriptive names (e.g., `feature/new-active-tool`, `bugfix/fix-parsing-issue`).

- **Commit Messages:**  
  - Write clear, concise commit messages using the imperative mood ("Add", "Fix", "Update").
  - Include a brief summary on the first line, followed by a more detailed explanation if necessary.
  - Reference relevant GitHub issues (e.g., `Fixes #42`).

---

## Module Contributions

When contributing a new **passive module**:

- Follow the structure of existing modules in **modules/**.
- Ensure your module loads its configuration from **configs/** and disables itself if the config is absent.
- Update the relevant documentation in **docs/tools/** with usage, configuration, and output details.
- Provide tests or clear manual testing instructions if possible.

---

## Active Tools Contributions

For contributions to **active tools** in **active_tools/**:

- Follow the pattern established by existing active tool modules (e.g., Nmap, Gobuster).
- Each tool must:
  - Load its own configuration from the **configs/** folder.
  - Write robust log output to a dedicated file in **logs/**.
  - Handle errors gracefully and include timeouts for external commands.
- Update the corresponding documentation in **docs/tools/**.
- Clearly mark these tools as “risky” in both code and documentation, including necessary warnings about legal and ethical use.

---

## Additional Resources

- [PEP 8 – Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

Thank you for contributing to OSINT Tool!
