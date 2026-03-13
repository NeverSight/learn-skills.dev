---
name: addon-human-pr-review-gate
description: Use when agent-generated code must pass a human PR review gate with trusted checks and merge blocks; pair with addon-decision-justification-ledger and architect-stack-selector.
---

# Add-on: Human PR Review Gate

Use this skill when agent-generated changes must be quickly and safely reviewed by humans before merge.

## Compatibility

- Works with all `architect-*` skills.
- Recommended default for `production-default` mode.

## Inputs

Collect:
- `RISK_LEVEL`: `standard` | `high`.
- `REQUIRED_HUMAN_APPROVALS`: default `1` (`2` for `high`).
- `BUNDLE_DIR`: default `REVIEW_BUNDLE`.

## Integration Workflow

1. Add review bundle artifacts:
```text
REVIEW_BUNDLE/SUMMARY.md
REVIEW_BUNDLE/FILE_MANIFEST.txt
REVIEW_BUNDLE/RISK_REPORT.md
REVIEW_BUNDLE/DEPENDENCY_DIFF.md
REVIEW_BUNDLE/DOCKER_REPORT.md
REVIEW_BUNDLE/TEST_EVIDENCE.md
REVIEW_BUNDLE/DECISION_TRACE.md
REVIEW_BUNDLE/POLICY_CHECKLIST.md
```

2. Add bundle generation script:
```text
scripts/review/generate_review_bundle.sh
```
- Copy and adapt this skill's bundled script:
- `scripts/generate_review_bundle.sh`
- Place the adapted result in the target project at `scripts/review/generate_review_bundle.sh`.
- Script should be deterministic and avoid network calls.
- It should collect:
- changed files
- dependency changes
- container/runtime changes
- test command outputs (or explicit failures)
- decision trace mapping (file to decision ID)

3. Add trusted PR gate policy:
```text
CODEOWNERS
.github/workflows/review-gate.yml
```
- Protect `CODEOWNERS`, `.github/workflows/*`, and `scripts/review/*` with required human review.
- Require review-gate status + human approvals before merge.

4. Ensure branch/merge policy (repo settings):
- Require pull requests to merge.
- Require status checks to pass.
- Require linear history/signed commits as org policy dictates.
- Disallow bypass for agent identity.

## Required Templates

### `REVIEW_BUNDLE/POLICY_CHECKLIST.md`
```markdown
# Policy Checklist

- [ ] Review bundle generated for this PR
- [ ] No secrets in source, history, or config
- [ ] New dependencies reviewed (license + risk)
- [ ] Docker changes reviewed (base image, user, ports, caps)
- [ ] High-risk APIs reviewed (`subprocess`, `eval/exec`, network egress, crypto)
- [ ] Every non-trivial change maps to a decision entry with explicit rationale
- [ ] Human approval count meets policy
```

### `CODEOWNERS` (minimum)
```text
.github/workflows/* @your-org/platform-reviewers
scripts/review/* @your-org/platform-reviewers
REVIEW_BUNDLE/* @your-org/security-reviewers
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not rely on “run app and eyeball” as sole verification.
- Do not run untrusted PR code with elevated secrets/permissions.
- Keep review bundle concise; optimize for <10 minute human scan.
- Fail closed: missing bundle artifacts should block merge.
- Treat workflow/policy changes as high-risk and require elevated review.
- Treat missing decision rationale as a merge blocker.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f REVIEW_BUNDLE/SUMMARY.md
test -f REVIEW_BUNDLE/FILE_MANIFEST.txt
test -f REVIEW_BUNDLE/RISK_REPORT.md
test -f REVIEW_BUNDLE/DEPENDENCY_DIFF.md
test -f REVIEW_BUNDLE/DOCKER_REPORT.md
test -f REVIEW_BUNDLE/TEST_EVIDENCE.md
test -f REVIEW_BUNDLE/DECISION_TRACE.md
test -f REVIEW_BUNDLE/POLICY_CHECKLIST.md
test -f scripts/review/generate_review_bundle.sh
test -f .github/workflows/review-gate.yml
test -f CODEOWNERS
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
