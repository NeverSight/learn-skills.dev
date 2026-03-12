---
name: litestar-cli
description: Use Litestar CLI for app autodiscovery, explicit app targeting, operational commands, schema generation workflows, and CLI extension points. Use when standardizing local/dev/ops command workflows around Litestar. Do not use for runtime app design decisions that belong in application code.
---

# CLI

## Execution Workflow

1. Ensure app autodiscovery works (canonical module layout) or define explicit app import path.
2. Standardize `litestar` commands in project scripts and team docs.
3. Separate local development commands from production runtime commands.
4. Extend CLI only when command reuse materially improves team workflows.

## Implementation Rules

- Keep one canonical entrypoint for commands and deployment.
- Avoid hidden env assumptions; make required env vars explicit.
- Pin command flags in scripts to avoid accidental behavior drift.
- Prefer explicit app targets in CI/CD for reproducibility.

## Example Pattern

```bash
# Autodiscovery mode
litestar run

# Explicit app target mode
litestar --app path.to.app:app run
```

## Validation Checklist

- Confirm `litestar run` and other core commands resolve the correct app.
- Confirm schema-related CLI commands run in CI without manual steps.
- Confirm command aliases/scripts behave consistently across environments.

## Cross-Skill Handoffs

- Use `litestar-app-setup` when autodiscovery or app factory layout is broken.
- Use `litestar-openapi` for schema generation quality, not just CLI invocation.

## Litestar References

- https://docs.litestar.dev/latest/usage/cli.html
