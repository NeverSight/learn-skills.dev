---
name: logs-repro-harness
description: Reduce flaky or environment-dependent failures to a minimal, reproducible script and capture the exact logs and error lines.
license: MIT
metadata:
  mode: diagnostics
  purpose: repro
---

# Logs Repro Harness

## When to Use

- An issue is flaky, hard to reproduce locally, or depends on environment configuration.

## Responsibilities

- Produce the smallest reproducible commands that trigger the failure.
- Capture key log lines, stack traces, and environment differences needed to reproduce.
- Provide targeted probes to distinguish root-cause hypotheses.

## Rules

- Never request or reveal secrets.
- Use `source setTestEnv.sh` when environment variables are required.
- Prefer `go test -run <TestName> <pkg>` for focused reproduction.

## Output

- **Minimal repro:** 1-3 commands.
- **Observed output:** first actionable error or stack lines.
- **Hypotheses:** 1-3 candidates with next probe commands.

## Examples

- "Test X passes locally but fails in CI" - compare env vars, capture output diff.
- "Intermittent timeout in Redis test" - isolate with `CONNTTL` tuning and retry logic.

## Related Skills

- `test-runner`, `fix-suggester`, `config-loader-helper`

## References

- `logs/` directory, `setTestEnv.sh`, `AGENTS.md`
