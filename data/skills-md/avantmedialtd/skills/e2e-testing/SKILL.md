---
name: e2e-testing
description: E2E and visual regression testing with Playwright. Use when writing tests, running E2E tests, debugging test failures, or working with visual baselines. Contains test commands, patterns, and debugging tips.
---

# E2E Testing

Playwright-based E2E and visual regression testing, run exclusively inside Docker.

## Commands

```bash
af e2e                                              # Run all tests (--max-failures=1 by default)
af e2e npm run e2e -- --grep "test name"            # Run specific test by name
af e2e npm run e2e -- tests/Feature.spec.ts         # Run specific file
af e2e npm run e2e -- --update-snapshots            # Update all visual baselines
af e2e npm run e2e -- --grep "page" --update-snapshots  # Update specific baseline
```

**Never** run Playwright directly outside Docker.

## Critical Requirements

- **ONLY run E2E tests through `af`** — never invoke Playwright, Docker, or test scripts directly
- **ALWAYS add E2E tests** for every feature change
- **ALWAYS run the full suite** (no `--grep`) before finishing, to confirm nothing else broke
- **NEVER use `waitForLoadState('networkidle')`** — it's unreliable and causes timeouts. Wait for a specific visible element instead

## Debugging Failures

The test runner output is already optimized for AI consumption — do NOT pipe to `head`, `tail`, or other commands.

1. **Read the reporter output first** — it includes error messages, DOM snapshots, and file paths
2. **For deeper debugging**, read `./test-results/*/error-context.md` for the full DOM snapshot at failure time
3. **HTML report** with traces: `./playwright-report/index.html`
4. **Trace files**: `./test-results/*/trace.zip`

Common failure causes:
- **Strict mode violations**: Multiple elements matched — add `level` to headings, scope to a section, or use `.first()`
- **Timeout**: Element not found — check the DOM snapshot for actual structure vs expected selectors
- **Visual diff**: Screenshot mismatch — if the change is intentional, update baselines

## Output Directories

- `playwright-report/` — HTML report with traces
- `test-results/` — Failure artifacts including `error-context.md`

## Anti-patterns

- `waitForLoadState('networkidle')` — unreliable, use visible element waits
- Running Playwright directly outside Docker
- If statements in assertions — use proper matchers
- Mock auth keys — use real generated keys from seed data
- Hardcoded dates that conflict between test files

For test code patterns, selectors, and visual testing guidance, see [PATTERNS.md](PATTERNS.md).
