---
name: ci-integration
description: >-
  Deterministic CI/CD interaction patterns. Push-and-wait discipline, failure
  triage, self-healing for lint/format/infra failures, structured output for
  pipeline consumption. Activate when interacting with CI/CD systems.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: [debugging-protocol]
  context: [ci-results, git-history]
  phase: ship
  standalone: true
---

# CI Integration

**Value:** Feedback -- CI pipelines produce signals. Deterministic interaction
patterns ensure those signals are received, classified, and acted on correctly.
Undisciplined CI interaction (pushing over failing runs, ignoring flaky tests)
degrades the signal until the pipeline is noise.

## Purpose

Teaches disciplined CI/CD interaction: one pending run at a time, structured
failure triage, automated self-healing for mechanical failures, and structured
evidence output for pipeline consumption. Prevents the most common CI failure
mode: pushing again before understanding why the last run failed.

## Practices

### Push-and-Wait Discipline

One pending CI run at a time. Never push while a run is in progress.

1. Push the commit
2. Poll or wait for the CI run to complete
3. Read the full result before taking any action
4. Only after the run completes (pass or fail) may you push again

**Do:**
- Wait for CI completion before starting new work that would require a push
- Read the complete CI output, not just the status badge

**Do not:**
- Push a "fix" while the previous run is still pending
- Assume a run will pass and push follow-up commits
- Cancel a run to push a new one (unless the run is clearly stale)

### Failure Triage

Classify every CI failure before attempting a fix. The classification
determines the fix strategy.

| Classification | Signal | Fix Strategy |
|----------------|--------|--------------|
| `test-failure` | Test assertions fail | Route to `debugging-protocol` |
| `lint-failure` | Linter or formatter errors | Auto-fix: run formatter, commit, re-push |
| `build-failure` | Compilation or dependency errors | Dependency analysis, check lockfiles |
| `flaky-test` | Test fails then passes on retry without code changes | Flag and track (see below) |
| `infra-failure` | Network, runner, or service errors | Retry (max 2), then escalate |

Read the full CI log to classify. Do not guess from the status alone.

### Self-Healing

Mechanical failures that have deterministic fixes should be resolved
automatically:

1. **Lint/format failures:** Run the project's formatter or linter with
   auto-fix, commit the result, re-push. This is a single retry -- if the
   formatter does not resolve the issue, classify as `build-failure`.
2. **Infra failures:** Retry the CI run (max 2 retries). If all retries fail,
   escalate to the user with the infra error details.
3. **Test failures:** Never auto-retry. Route to `debugging-protocol` for
   investigation. A test failure is a signal, not noise.
4. **Build failures:** Check dependency lockfiles, build configuration, and
   environment differences. Do not blindly retry.

### Flaky Test Detection

A test is flaky if it passes on retry without any code changes.

When detected:
1. Flag the test with its name, file, and the failure output from the flaky run
2. Record in project memory (`.factory/audit-trail/flaky-tests.json` if
   factory mode is active, or project notes otherwise)
3. Report to the user -- flaky tests erode CI trust and must be addressed
4. Do not treat a flaky pass as a real pass for quality gate purposes until
   the flakiness is resolved

### Structured Output

Every CI interaction produces a `CI_RESULT` evidence packet:

```json
{
  "run_id": "string (CI run identifier)",
  "status": "string (passed | failed | cancelled)",
  "duration": "number (seconds)",
  "failure_type": "string (test-failure | lint-failure | build-failure | flaky-test | infra-failure) -- omit if passed",
  "failure_details": "string (summary of failure) -- omit if passed",
  "fixes_applied": ["string (description of each auto-fix applied)"],
  "retry_count": "number (0 if no retries)"
}
```

This packet is consumed by pipeline orchestrators and audit trails. Always
produce it, even for passing runs.

## Enforcement Note

This skill provides advisory guidance. It instructs the agent to follow
push-and-wait discipline and structured triage but cannot mechanically prevent
concurrent pushes. When used within a pipeline orchestrator, the pipeline can
enforce the one-pending-run constraint. In standalone use, the agent follows
these practices by convention.

## Verification

After each CI interaction, verify:

- [ ] Waited for the previous CI run to complete before pushing
- [ ] Read the complete CI output (not just status)
- [ ] Classified the failure type before attempting a fix
- [ ] Applied the correct fix strategy for the classification
- [ ] Did not retry a test failure (routed to debugging-protocol instead)
- [ ] Lint/format auto-fixes were limited to one attempt
- [ ] Infra retries did not exceed 2
- [ ] Flaky tests were flagged and recorded
- [ ] Produced a CI_RESULT evidence packet

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone for any project with a CI/CD pipeline. It
integrates with:

- **debugging-protocol:** Test failures route to the debugging protocol for
  systematic investigation rather than blind fix attempts
- **tdd:** CI failures during TDD cycles feed back into the RED-GREEN loop;
  a CI test failure means the cycle is not complete
- **pipeline:** When used within factory mode, the pipeline orchestrator
  consumes CI_RESULT packets to evaluate quality gates

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill debugging-protocol
```
