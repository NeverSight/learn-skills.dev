---
name: sca-pip-audit
description: Run pip-audit for Python dependency vulnerability scanning. Checks installed packages and requirements files against the OSV and PyPI advisory databases.
---

# SCA Scan with pip-audit (Python)

You are a security engineer running Software Composition Analysis (SCA) on a Python project using **pip-audit**.

## When to use

Use this skill when asked to check Python dependencies for vulnerabilities.

## Prerequisites

- pip-audit installed (`pip install pip-audit`)
- Verify: `pip-audit --version`

## Instructions

1. **Identify the target** — Determine the Python project or requirements file.
2. **Run the scan:**
   ```bash
   pip-audit --format=json --output=pip-audit-results.json
   ```
   - From requirements file: `pip-audit -r requirements.txt --format=json --output=results.json`
   - Strict mode (fail on any vuln): `pip-audit --strict --format=json`
   - Fix automatically: `pip-audit --fix`
   - With descriptions: `pip-audit --desc --format=json`
3. **Parse the results** — Read JSON output and present findings:

```
| # | Package | Installed | Fixed Versions | Vulnerability ID | Description |
|---|---------|-----------|---------------|-----------------|-------------|
```

4. **Summarize** — Provide:
   - Total packages audited vs vulnerabilities found
   - Packages with available fixes
   - Upgrade commands: `pip install --upgrade <package>==<fixed-version>`
   - Packages with no fix available (may need alternatives)
