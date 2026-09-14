---
name: gha-audit
description: Audit the GitHub Actions workflows in this repo for security, speed, and correctness, and report findings with a proposed diff.
disable-model-invocation: true
---

Call the Skill tool with "github-actions-workflow-pro" and run its audit path (`references/audit.md`) against the workflows named in `$ARGUMENTS`, or every file under `.github/workflows/` when no argument is given. Produce the report and proposed diff; leave the workflow files untouched unless the user asks you to apply the fixes.
