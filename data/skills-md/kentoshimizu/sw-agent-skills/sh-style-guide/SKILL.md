---
name: sh-style-guide
description: "Style, review, and refactoring standards for POSIX `sh` scripting. Trigger when `.sh` files, files with `#!/usr/bin/env sh` or `#!/bin/sh`, or CI workflow blocks with `shell: sh` are created, modified, or reviewed and portability/safety controls for POSIX shell must be enforced. Do not use for Bash-specific, Zsh-specific, or PowerShell-specific style rules. In multi-language pull requests, run together with other applicable `*-style-guide` skills."
---

# SH Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Use this skill to write and review POSIX `sh` scripts that run reliably across environments where Bash features are unavailable.

## Trigger And Co-activation Reference

- If available, use `references/trigger-matrix.md` for canonical co-activation rules.
- If available, resolve style-guide activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...`.
- If available, validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Quality Gate Command Reference

- If available, use `references/quality-gate-command-matrix.md` for CI check-only and local autofix mapping.

## Quick Start Snippets

### Portable script skeleton

```sh
#!/bin/sh
set -eu

SCRIPT_NAME=$(basename "$0")
TEMP_DIR=$(mktemp -d)

cleanup() {
  rm -rf -- "$TEMP_DIR"
}

on_error() {
  line_number="$1"
  echo "$SCRIPT_NAME: failed at line $line_number" >&2
}

trap cleanup EXIT HUP INT TERM
trap 'on_error "$LINENO"' ERR

main() {
  echo "temp dir: $TEMP_DIR"
}

main "$@"
```

### Required environment variable check (no silent default)

```sh
: "${API_TOKEN:?API_TOKEN is required}"
: "${API_BASE_URL:?API_BASE_URL is required}"
```

### POSIX-safe argument handling (no arrays)

```sh
run_curl() {
  url="$1"

  curl --fail --silent --show-error \
    --header "Authorization: Bearer ${API_TOKEN}" \
    "$url"
}
```

### Bounded retry loop

```sh
MAX_ATTEMPTS=5
RETRY_DELAY_SECONDS=2

retry_command() {
  attempt=1
  while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
    if "$@"; then
      return 0
    fi

    if [ "$attempt" -eq "$MAX_ATTEMPTS" ]; then
      echo "command failed after $MAX_ATTEMPTS attempts" >&2
      return 1
    fi

    sleep "$RETRY_DELAY_SECONDS"
    attempt=$((attempt + 1))
  done
}
```

### Safe line reading

```sh
while IFS= read -r line; do
  printf 'line=%s\n' "$line"
done < "$input_file"
```

## Portability And Readability

1. Target POSIX syntax only; avoid Bash/Zsh-specific features.
2. Use `set -eu` for executable scripts.
3. Prefer small functions and clear `main` orchestration.
4. Use uppercase constants and lowercase local variables.
5. Keep comments short and intent-focused.

## Data Handling And Quoting

1. Quote parameter expansion by default.
2. Avoid `eval` unless strictly required and heavily validated.
3. Replace magic numbers with named constants and explicit units.
4. Use `--` for destructive command path arguments.
5. Validate all external input before using it in commands.

## Error Handling And Safety

1. Return explicit non-zero status for expected failure modes.
2. Use `trap` for cleanup and signal handling.
3. Handle failures intentionally; do not mask with `|| true` unless justified.
4. Fail startup when required configuration is missing.
5. Let failures surface when root-cause fixing is required.

## Testing And Verification

1. Add shell tests (`shunit2` or project equivalent) for core paths.
2. Cover edge cases: empty input, whitespace paths, missing env vars, timeout/retry exhaustion.
3. Document manual verification for environment-dependent behavior.
4. Verify idempotency for repeatable automation scripts.

## CI Required Quality Gates (check-only)

1. Run `shellcheck -s sh`.
2. Run `shfmt -d -ln posix`.
3. Run shell tests (`shunit2`/project equivalent).
4. Reject hidden failure paths and implicit behavior.

## Optional Autofix Commands (local)

1. Run `shfmt -w -ln posix`.
2. Apply safe lint fixes, then rerun check-only commands.
