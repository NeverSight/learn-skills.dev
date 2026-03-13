---
name: github-codeowners-management
description: "Govern CODEOWNERS rules so review routing reflects real ownership and risk boundaries on GitHub. Use when repository ownership mapping or mandatory reviewer rules must be defined, updated, or audited; do not use for non-GitHub runtime architecture or data-layer design."
---

# Github Codeowners Management

## Overview
Use this skill to keep CODEOWNERS enforceable, low-noise, and aligned with actual maintainer responsibility.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- CODEOWNERS pattern guidance:
  - `references/codeowners-patterns.md`

## Templates And Assets
- CODEOWNERS change plan:
  - `assets/codeowners-change-plan-template.md`

## Inputs To Gather
- Repository ownership map by criticality and change frequency.
- Team boundaries, backup owners, and staffing constraints.
- Required reviewer policy for sensitive paths.
- Recent PR routing pain points (over-review, no-owner paths, stale owners).

## Deliverables
- CODEOWNERS update plan with rationale.
- Ownership gap/overlap report.
- Verification results for routing behavior.
- Maintenance plan for owner lifecycle changes.

## Workflow
1. Capture proposed changes in `assets/codeowners-change-plan-template.md`.
2. Map high-risk paths to explicit primary and backup owners.
3. Resolve overlap and wildcard precedence issues.
4. Validate with lint scripts and sample PR routing.
5. Publish changes with ownership maintenance rules.

## Scripts
- Lint CODEOWNERS:
  - `python3 scripts/lint_codeowners.py --path .github/CODEOWNERS --policy team`
- Enforce required patterns:
  - `python3 scripts/lint_codeowners.py --path .github/CODEOWNERS --policy team --require-pattern '/.github/workflows/*'`
- GitHub semantics mode (without strict team catch-all ordering):
  - `python3 scripts/lint_codeowners.py --path .github/CODEOWNERS --policy github`

## Quality Standard
- Critical paths always have active owners and backup coverage.
- Wildcards do not mask sensitive-path ownership.
- Rules are maintainable and avoid unnecessary reviewer fan-out.
- Routing behavior matches expected maintainers on real PR samples.

## Failure Conditions
- Stop when critical paths are left without accountable owners.
- Stop when CODEOWNERS rules cannot be validated by lint and sample checks.
- Escalate when staffing gaps prevent enforceable ownership policy.
