---
name: cli-design
description: Use when designing, building, or reviewing a command-line interface (CLI) tool. Provides a checklist of standard CLI conventions. Do not use for non-CLI applications.
---

# CLI design checklist

## Help and version

- Provide --help/-h with clear usage, options, and examples; include required parameters in examples.
- Provide --version (use -V); reserve -v for --verbose.

## Input and output

- Support stdin/stdout piping; allow output redirection (e.g., --output for file creation).
- Offer machine-readable output (e.g., --json) when emitting structured data.

## Safety and control

- For modifying/deleting actions, provide --dry-run and an explicit bypass (--yes/--force).
- Provide controllable logging (--quiet, --verbose, or --trace).
- Use deterministic exit codes (0 success, non-zero failure) and avoid silent fallbacks.
- Implement strictly non-interactive modes for CI/CD environments.

## Configuration

- For JSON configuration, define/update a JSON Schema and validate config on load.
- Support configuration via environment variables for sensitive or environment-specific data.

## Interactive prompts

- Provide required context before asking; for yes/no prompts, Enter means "Yes" and "n" means "No".
