---
name: priority-review
description: Evidence-based code review for diffs, PRs, and commits using P0-P3 severity. Finds actionable defects in changed code (security, correctness, reliability) and avoids style-only feedback.
---

# Priority Code Review

Review code changes for real, actionable defects. Prioritize precision over exhaustive exploration. Report only issues with a plausible failure path tied to the change.

## Scope

- Review diffs, PRs, or commits and the code paths they affect.
- Focus on security, correctness, reliability, data integrity, and breaking regressions.
- Reference unchanged code only when needed to explain a failure introduced by the change.
- Do not report style preferences, feature ideas, or speculative concerns without concrete impact.

## Severity and Confidence

### Severity (P0-P3)

#### P0 - Critical (must fix)

- Security vulnerabilities (hardcoded secrets, injection, auth bypass)
- Data corruption or irreversible loss
- Crashes/outages in reachable paths
- Severe breaking changes that make core flows fail

#### P1 - High (should fix before merge)

- User-visible correctness bugs in common paths
- Missing/incorrect error handling causing request/job failure
- Concurrency/state bugs with realistic reachability
- Incomplete migrations or contract changes likely to break consumers

#### P2 - Medium

- Edge-case correctness bugs with clear impact
- Type or validation gaps likely to fail at runtime
- Performance regressions with concrete user or system impact

#### P3 - Low

- Low-severity correctness or maintainability risk introduced by the change
- Limited-impact fallback/default handling mistakes
- Latent bug risk with narrow reachability and clear evidence

### Confidence

- `high`: Direct code evidence and clear failure path from the change
- `medium`: Strong evidence with one reasonable assumption
- `low`: Plausible concern that needs validation; report under `Needs verification`, not as a blocker

## Review Workflow

### Pass 1: Gather Minimal Context and Triage

- Collect the smallest sufficient git context for the review mode.
- Start with changed files and diff; read surrounding code only when needed.
- Identify risk signals and form defect hypotheses before deep investigation.

Examples (choose only what is needed):
- Uncommitted: `git status --porcelain`, `git diff`, `git diff --cached`
- PR/branch: `git log --oneline {base}..HEAD`, `git diff {base}...HEAD --stat`, `git diff {base}...HEAD`
- Commit: `git show {sha} --stat`, `git diff {sha}^..{sha}`

### Risk Signals (trigger deeper review)

- Auth, permissions, session, secrets, crypto
- Input parsing, validation, serialization, SQL, file/path handling
- Async/concurrency, shared state, retries, idempotency, caching
- Data models, migrations, backfills, schema or contract changes
- Money, billing, quotas, usage accounting
- Error handling, timeouts, fallbacks, feature flags

### Pass 2: Targeted Investigation (Bounded)

- Investigate only when a plausible defect hypothesis exists.
- Prioritize highest-risk hypotheses first.
- Read local context, related callers/callees, and affected invariants.
- Use sub-agents only for complex targeted checks; cap to 2-3 parallel probes.
- Do not spawn broad exploratory investigations for every category.

## Optional Custom Rules

If `.priority-review-rules.json` exists in the repository root, load it and check changed files for rule matches.

Minimal rule format:

```json
{
  "rules": [
    {
      "id": "no-console-log",
      "title": "No console.log in production code",
      "severity": "P2",
      "pattern": "console\\.log"
    }
  ]
}
```

- Report rule violations at the rule severity.
- Check changed files by default unless the rule explicitly requires broader scope.

## Findings: Evidence Standard

Report only issues with a plausible execution or failure path caused by the change.

For each finding, include:

- Severity (`P0`-`P3`) and confidence (`high` or `medium`)
- Changed-file anchor (`file:line`) when possible
- Concrete impact (what fails, breaks, leaks, or corrupts)
- Causal explanation (why the change creates the issue)

If confidence is `low`, place it under `Needs verification` instead of P0/P1/P2/P3.

## Report Format

Report findings by priority (`P0` -> `P3`).

For each finding:

```
**[P{0-3}][{high|medium}] {file}:{line} - {title}**

Impact: {what breaks / risk}
Why: {causal path from the change}
```

Optional section for uncertain concerns:

```
## Needs verification
- [low] {file}:{line} - {concern} ({what to validate})
```

```
## Summary
- P0: N
- P1: N
- P2: N
- P3: N
- Outcome: Blocker | Non-blocking findings | No actionable findings
```

Use `No actionable findings` when no credible defects are identified.

## What Not to Report

- Style, formatting, naming, or preference-only comments
- Theoretical issues without a plausible failure path
- Pre-existing problems in unchanged code (unless the change introduces the failure path through them)
- Feature requests, enhancement ideas, or missing features
- Duplicate findings for the same underlying issue
- Praise-only notes or non-actionable observations

## Tool Defaults

- Do not run linting, type checking, or tests by default.
- Use targeted verification only when necessary to validate a suspected `P0`/`P1` issue that code inspection cannot resolve.
- Focus on semantic review of the change, not automated tooling output.

## Anti-Patterns

- Do not report speculation as a finding.
- Do not escalate severity without concrete user, security, or data impact.
- Do not optimize for quantity of findings over accuracy.
- Do not miss cross-file regressions when the diff clearly changes shared behavior.
