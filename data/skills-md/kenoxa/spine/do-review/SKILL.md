---
name: do-review
description: >
  Structured code review with severity-bucketed findings and resolution gates.
  Use after code changes or when the user asks for review.
  Do NOT use during active implementation — use the review phase in do-execute instead.
argument-hint: "[file, PR, or scope]"
---

Review changed code against the requested outcome and accepted plan. Produce structured,
severity-bucketed findings. Review is read-only — no file writes, no test execution.

## Workflow

1. **Scope check** — confirm what was requested and what changed.
2. **Evidence check** — validate claims against current code and requirements.
3. **Spec compliance** — verify built behavior matches requested behavior.
4. **Risk pass** — correctness, security, performance, maintainability (scale by risk level).
5. **Quality pass** — readability, cohesion, duplication, test adequacy, edge/failure coverage.
6. **Output** — return findings using severity buckets below.

## Severity Buckets

| Bucket | Gate behavior |
|--------|--------------|
| `blocking` | Must fix before completion. Requires E2+ evidence. |
| `should_fix` | Recommended fix. Blocks completion unless user explicitly defers. |
| `follow_up` | Tracked debt. Does not block completion — record for future action. |

`blocking` findings without code evidence (E2+) are invalid — demote to `should_fix`.

## Risk Scaling

| Risk | Lenses |
|------|--------|
| Low | Spec compliance + quality |
| Medium | + testing-depth |
| High | + security probe |

### High-Risk Security Probe

When risk is high, explicitly check:
- Auth boundary regressions and privilege escalation paths
- Input trust boundaries (injection, unsafe parsing, unvalidated external data)
- Secret/token exposure in logs, configs, or error surfaces
- Failure-mode behavior that leaks data or bypasses controls

For false-positive filtering and security precedents, see [references/security-probe.md](references/security-probe.md).
For deeper security heuristics, use the `security-reviewer` skill.
For visual diff explanations, use the `visual-explainer` skill.
For net-complexity measurement (did this change reduce or increase bloat?), use the `reducing-entropy` skill.

## Noise Filtering

Before raising any finding, verify:
- Issue is introduced or worsened by the reviewed change — pre-existing issues are out of scope
- Finding is discrete and actionable — general codebase observations are not findings
- Finding does not demand rigor absent from the rest of the codebase
- For security findings at high risk: apply exclusion rules from [references/security-probe.md](references/security-probe.md)

## Output Format

Per finding: severity bucket, target file(s), remediation path, evidence level.

For directional findings: numbered issue ID with option set (A/B/C), recommendation first,
include "do nothing" when reasonable. Tradeoff rationale for each option.

## Bug-Fix Review

Require root-cause evidence. Confirm the fix targets the source trigger, not symptom relief.
Missing root-cause evidence → `blocking` finding.

## Documentation Review

When reviewing docs, READMEs, or user-facing text:
- Verify wording precision and actionability
- Flag outdated or contradictory statements
- Verify command, skill, and API names match current surface
- Check doc claims against codebase evidence — unsupported claims → `should_fix`

## Deferral Policy

- Any finding can be deferred with explicit user approval.
- Deferred findings remain visible in output — never silently removed.
- Deferral is an exception path, not the default.

## Completion Declaration

When all findings are resolved or explicitly deferred:

- `Review complete. No unresolved findings.`
- `Review complete. Unresolved findings remain` — followed by the list.

## Evidence Levels

See AGENTS.md for E0–E3 definitions.

## Anti-Patterns

- Reviewing against personal preference instead of requested outcome and plan
- Blocking on E0-only claims without code evidence
- Writing files or executing tests during review
- Silently dropping deferred findings from output
- Skipping security probe on high-risk changes
- Merging review with implementation unless user asked for immediate fixes
