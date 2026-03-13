---
name: bash-style-guide
description: "Style, review, and refactoring standards for Bash shell scripting. Trigger when `.sh` files, files with `#!/usr/bin/env bash` or `#!/bin/bash`, or CI workflow blocks with `shell: bash` are created, modified, or reviewed and Bash-specific quality controls (quoting safety, error handling, portability, readability) must be enforced. Do not use for generic POSIX `sh`, PowerShell, or language-specific application style rules. In multi-language pull requests, run together with other applicable `*-style-guide` skills."
---

# Bash Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Use this skill to write and review Bash scripts that are safe, debuggable, and operable in CI and production automation.

## Trigger And Co-activation Reference

- If available, use `references/trigger-matrix.md` for canonical co-activation rules.
- If available, resolve style-guide activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...`.
- If available, validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Quality Gate Command Reference

- If available, use `references/quality-gate-command-matrix.md` for CI check-only and local autofix mapping.

## Quick Start Snippets

### Script skeleton with strict mode and cleanup trap

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_NAME="$(basename "$0")"
readonly TEMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf -- "${TEMP_DIR}"
}

on_error() {
  local line="$1"
  local exit_code="$2"
  echo "${SCRIPT_NAME}: failed at line ${line} (exit=${exit_code})" >&2
}

trap cleanup EXIT
trap 'on_error "$LINENO" "$?"' ERR

main() {
  echo "working dir: ${TEMP_DIR}"
}

main "$@"
```

### Required environment variable check (fail fast)

```bash
: "${API_TOKEN:?API_TOKEN is required}"
: "${API_BASE_URL:?API_BASE_URL is required}"
```

### Safe command assembly with arrays

```bash
run_curl() {
  local url="$1"
  local -a args=(
    --fail
    --silent
    --show-error
    --header "Authorization: Bearer ${API_TOKEN}"
    "${url}"
  )

  curl "${args[@]}"
}
```

### Bounded retry with explicit backoff constants

```bash
readonly MAX_ATTEMPTS=5
readonly RETRY_DELAY_SECONDS=2

retry_command() {
  local attempt=1
  while (( attempt <= MAX_ATTEMPTS )); do
    if "$@"; then
      return 0
    fi

    if (( attempt == MAX_ATTEMPTS )); then
      echo "command failed after ${MAX_ATTEMPTS} attempts" >&2
      return 1
    fi

    sleep "${RETRY_DELAY_SECONDS}"
    ((attempt++))
  done
}
```

### Safe line reading preserving whitespace

```bash
while IFS= read -r line; do
  printf 'line=%s\n' "${line}"
done < "${input_file}"
```

## Structure And Readability

1. Use `#!/usr/bin/env bash` for executable scripts.
2. For executable entrypoints, use strict mode: `set -euo pipefail`.
3. Keep functions focused on one responsibility and use `main` for orchestration.
4. Use uppercase constants (`MAX_RETRIES`) and lowercase locals (`retry_count`).
5. Use `local` inside functions to avoid state leakage.
6. Add short intent comments only for non-obvious logic.

## Data Handling And Quoting

1. Quote expansions by default: `"${var}"`, `"${array[@]}"`.
2. Use arrays for argument lists; avoid string-concatenated command assembly.
3. Replace magic numbers with named constants including units (`TIMEOUT_SECONDS`).
4. Avoid `eval`; treat it as a security-sensitive last resort.
5. Fail fast for required environment variables; do not add silent defaults for required config.

## Error Handling And Control Flow

1. Return explicit non-zero codes for expected failure modes.
2. Use `trap` for cleanup and actionable error reporting.
3. Handle failure paths intentionally (`if ! cmd; then ... fi`) instead of masking.
4. Avoid broad `|| true`; suppress only with explicit rationale.
5. Let failures surface when root cause should be fixed.

## Security And Operational Safety

1. Validate all external input before use.
2. Use `--` before positional paths in destructive commands (`rm -- "$target"`).
3. Prefer `mktemp` for temporary files/directories.
4. Never print secrets or tokens in logs.
5. Use least privilege and avoid unnecessary `sudo`.

## Performance And Scalability

1. Avoid subshell spawning in tight loops when builtins suffice.
2. Prefer single-pass text processing over repeated pipelines.
3. Batch filesystem operations where practical.
4. Use bounded retry loops with named backoff constants.

## Testing And Verification

1. Add `bats` tests for critical behavior and failure paths.
2. Cover edge cases: empty input, whitespace paths, missing env vars, timeout, retry exhaustion.
3. Document manual verification where automation is not feasible.
4. Check idempotency for scripts that may run repeatedly.

### Minimal `bats` example

```bash
#!/usr/bin/env bats

@test "fails when required env var is missing" {
  run ./script.sh
  [ "$status" -ne 0 ]
  [[ "$output" == *"API_TOKEN is required"* ]]
}
```

## CI Required Quality Gates (check-only)

1. Run `shellcheck` with warnings treated as actionable.
2. Run `shfmt -d` (or equivalent check mode) and require zero diff.
3. Run test suite (`bats test/` or repository-specific path).
4. Reject changes that hide failures or rely on implicit behavior.

## Optional Autofix Commands (local)

1. Run `shfmt -w`.
2. Apply safe mechanical fixes suggested by `shellcheck`, then rerun checks.
