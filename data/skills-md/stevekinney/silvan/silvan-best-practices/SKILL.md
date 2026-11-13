---
name: silvan-best-practices
description: Guidelines for Silvan CLI and UI UX consistency, output conventions, JSON and verbosity behavior, error recovery, onboarding, and operator workflows. Use when implementing or reviewing CLI output, help or onboarding flows, error handling, JSON schemas, run lifecycle UX, or dashboard features in this repo.
---

# Silvan Best Practices

## Overview

Use this skill to keep Silvan's UX consistent and operator-grade. It provides a shared checklist and references for CLI output, errors, JSON behavior, onboarding, and UI surfaces.

## Quick workflow

1. Identify the UX surface (CLI output, JSON, errors, onboarding/help, UI).
2. Read `references/best-practices.md` for conventions and guardrails.
3. Reuse or extend shared utilities instead of adding one-off formatting.
4. Ensure success confirmations, next steps, and actionable errors.
5. Update tests and docs when behavior or output changes.

## Definition of done

- Output uses semantic colors and consistent formatting.
- `--json` output is schema-stable and error-safe.
- Errors include recovery steps and docs links when relevant.
- Commands never exit silently on success.
- TTY and non-TTY output are both readable.

## References

- `references/best-practices.md`: canonical UX and output standards.
