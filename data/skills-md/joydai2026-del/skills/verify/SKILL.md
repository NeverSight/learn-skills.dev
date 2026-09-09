---
name: verify
description: |
  6-phase post-implementation verification loop: Build, Type Check, Lint, Test Suite,
  Security Scan, Diff Review. Outputs structured pass/fail report.
  Use when: "verify", "check everything", "run verification", "pre-PR check",
  "run all checks", "make sure everything works", "verify the build", "post-implementation check".
  PROACTIVE TRIGGER (CRITICAL): After completing any implementation task, before shipping.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
gotchas_count: 0
---

# Verify, 6-Phase Post-Implementation Verification

Run a systematic quality check across build, types, lint, tests, security, and diff.
Outputs a structured report with PASS/FAIL/WARN/SKIP per phase.

## When to Activate

- After implementing a feature or fix (before PR)
- When asked to "verify", "check everything", "pre-PR check"
- Proactively after substantial code changes
- As the final step before `/ship`

## Quick Mode

When invoked as `/verify quick`, run only: Build + Test + Diff Review (skip lint, type check, security). Use for rapid iteration.

## Procedure

### Phase 0: Detect Project Type

Auto-detect from files in the working directory:

| File | Project Type | Build | Type Check | Lint | Test | Security |
|------|-------------|-------|------------|------|------|----------|
| `pubspec.yaml` | Flutter/Dart | `flutter build` | `dart analyze` | `dart analyze` | `flutter test` | `grep` patterns |
| `package.json` | Node.js | `npm run build` | `tsc --noEmit` | `eslint .` | `npm test` | `npm audit` |
| `Cargo.toml` | Rust | `cargo build` | (built-in) | `cargo clippy` | `cargo test` | `cargo audit` |
| `go.mod` | Go | `go build ./...` | `go vet ./...` | `golangci-lint run` | `go test ./...` | `govulncheck ./...` |
| `pyproject.toml` | Python | (skip) | `mypy .` | `ruff check .` | `pytest` | `pip-audit` |

If no recognized file, ask the user what commands to run.

### Phase 1: Build Verification

```
Run the project's build command.
- PASS: exit code 0, no errors
- FAIL: non-zero exit, show first 20 lines of errors
- SKIP: no build step for this project type
```

### Phase 2: Type Check

```
Run the type checker.
- PASS: 0 errors
- WARN: 0 errors but warnings present (show count)
- FAIL: errors found (show first 10)
- SKIP: no type checker available
```

### Phase 3: Lint Check

```
Run the linter.
- PASS: 0 issues
- WARN: only style warnings, no errors
- FAIL: errors found (show first 10)
- SKIP: no linter configured
```

### Phase 4: Test Suite

```
Run tests with coverage if available.
- PASS: all tests pass
- WARN: tests pass but coverage below 70%
- FAIL: test failures (show first 5 failures)
- SKIP: no tests found
```

Report: total tests, passed, failed, skipped, coverage %.

### Phase 5: Security Scan

Run two checks:

**5a: Secret Detection**, grep staged/changed files for:
- API keys: `sk-`, `AKIA`, `ghp_`, `gho_`, `glpat-`
- Tokens: `token\s*[:=]`, `secret\s*[:=]`, `password\s*[:=]`
- Private keys: `-----BEGIN.*PRIVATE KEY-----`

**5b: Dependency Vulnerabilities**, run the project's audit command (npm audit, cargo audit, pip-audit, etc.)

```
- PASS: no secrets found, no high/critical vulns
- WARN: low/medium vulns only
- FAIL: secrets detected OR critical vulns
- SKIP: no audit tool available
```

### Phase 6: Diff Review

Review `git diff --cached` (or `git diff` if nothing staged) for:
- Debug statements: `console.log`, `print(`, `debugger`, `TODO`, `FIXME`, `HACK`
- Large files: any file > 500 lines changed
- Binary files accidentally committed
- Merge conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`

```
- PASS: clean diff
- WARN: TODOs or debug statements found (show locations)
- FAIL: merge conflict markers or binary files
```

## Output Format

```
=== VERIFICATION REPORT ===
Project: <detected type> (<directory name>)
Date: <timestamp>
Mode: <full | quick>

Phase 1 — Build:         PASS  (2.3s)
Phase 2 — Type Check:    PASS  (1.1s)
Phase 3 — Lint:          WARN  (0.8s) — 3 style warnings
Phase 4 — Tests:         PASS  (5.2s) — 47/47 passed, 82% coverage
Phase 5 — Security:      PASS  (1.5s)
Phase 6 — Diff Review:   WARN  (0.3s) — 2 TODO comments found

VERDICT: PASS (2 warnings)
Total time: 11.2s
```

**Verdict logic:**
- **PASS**: all phases PASS or SKIP (warnings OK)
- **FAIL**: any phase FAIL

## Integration Points

- Run after `/simplify` (de-sloppify pattern)
- Run before `/ship` (gate the PR)
- Run after `/qa` (code quality complement to browser QA)
- Can be scheduled: `/loop 15m /verify quick`

## Anti-Patterns

- Running verify but ignoring failures ("it's just a warning")
- Skipping security scan because "it's an internal tool"
- Not re-running after fixing issues found by verify
- Running only tests without the other phases
