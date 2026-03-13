---
name: agently-output-control
description: Use when the user wants stable structured fields, required keys, reliable machine-readable sections, or downstream-consumable output from one model request, including `.output(...)`, field ordering, and `ensure_keys`.
---

# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

The user does not need to say `.output(...)` or `ensure_keys`. Requests for stable JSON-like fields, structured reports, or machine-readable sections should route here.

## Native-First Rules

- prefer `.output(...)` for machine-readable results
- prefer `ensure_keys` when required fields must be enforced
- keep output schema explicit when downstream systems, workflow branches, or later model steps consume the result

## Anti-Patterns

- do not handwrite JSON post-processors when `.output(...)` already owns the contract
- do not build custom retry loops for missing keys before checking `ensure_keys`

## Read Next

- `references/overview.md`
