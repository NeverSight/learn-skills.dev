---
name: aco-design-guidelines
description: Review files for compliance with ACO UI Design Guidelines. Clean, minimal, brutalist-lite style for plugins and desktop apps.
---

# aco-design-guidelines

Review files for compliance with ACO UI Design Guidelines.

## How It Works
- Fetch the latest guidelines from the source URL below
- Read the specified files (or prompt user for files/pattern)
- Check against all rules in the fetched guidelines
- Output findings in the terse `file:line` format

## Guidelines Source
Fetch fresh guidelines before each review:

https://raw.githubusercontent.com/gustav-glitch/aco-design/main/markdown.md

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage
When a user provides a file or pattern argument:

- Fetch guidelines from the source URL above
- Read the specified files
- Apply all rules from the fetched guidelines
- Output findings using `file:line` format

If no files specified, ask the user which files to review.
