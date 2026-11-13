---
name: scoped-tests
description: >-
  Use after changing code, before claiming work is done — picks the correctly
  scoped pytest command instead of running the whole suite. Helps avoid the
  timeout-and-context-waste of full-suite runs on a one-service change.
paths:
  - services/**
  - packages/**
  - tests/**
---

# Scoped test runner

The article's rule: running the full suite on a one-service change wastes
context and time. Pick the narrowest command that still covers the change.

| What you changed | Run |
|------------------|-----|
| `services/auth/**` | `uv run pytest services/auth tests/test_auth.py` |
| `services/billing/**` | `uv run pytest services/billing tests/test_billing.py` |
| `services/api/**` | `uv run pytest services/api tests/test_api.py` |
| `services/notifications/**` | `uv run pytest services/notifications` |
| `services/search/**` | `uv run pytest services/search` |
| `packages/core/**` or `packages/db/**` | `uv run pytest -q` (FULL — these are imported everywhere) |

**Rule:** a change in `packages/core` or `packages/db` always runs the full
suite. A change in a single service runs only that service plus its test file.
