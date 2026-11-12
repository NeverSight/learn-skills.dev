---
name: rails-maintenance
type: workflow
description: Use for Rails setup, routine cleanup, code quality, and maintenance tasks that do not center on a new feature or diff review.
---

# Rails Maintenance

Identify the requested maintenance mode and use only the matching procedure: `setup-environment` for first-time setup, `apply-code-conventions` for path-specific conventions, `refactor-code` for behavior-preserving cleanup, or a focused engine procedure for engine work.

Preserve the app's configuration and conventions. Run checks relevant to changed files. Do not force TDD, security scans, full-suite runs, documentation, or PR steps when they do not apply. Use a checkpoint for production, security/authorization, deployment, or irreversible changes.
