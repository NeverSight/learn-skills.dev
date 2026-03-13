---
name: code-review-general
description: "Run full-scope code review for correctness, maintainability, and regression risk when no single specialty dominates. Use for broad merge-readiness reviews with explicit findings and evidence; if security or performance risk is primary, prioritize `code-review-security` or `code-review-performance` first."
---

# Code Review General

## Overview
Use this skill for structured merge-readiness review across correctness, readability, maintainability, and change risk.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Diff scope, affected modules, and runtime impact.
- Change intent and acceptance criteria.
- Related incidents/bugs and known fragile areas.
- Existing test coverage and missing verification.

## Deliverables
- Prioritized findings list (severity, rationale, evidence).
- Open questions and risk assumptions.
- Minimal change summary and test/verification gaps.

## Finding Format (Required)
Use this structure for each finding:
- `severity`: blocker/high/medium/low
- `location`: file + line
- `issue`: concrete defect/risk
- `impact`: why this matters
- `fix`: root-cause-oriented recommendation

## Quick Review Heuristics
- Correctness: state transitions, edge-case handling, error propagation.
- Maintainability: naming clarity, duplication, boundary responsibility.
- Safety: hidden fallbacks, implicit defaults, brittle conditionals.
- Verification: missing tests for new branches/failure paths.

## Quality Standard
- Findings are evidence-based and tied to changed code.
- Severity reflects user/business impact, not stylistic preference.
- Recommendations address root causes, not cosmetic patches.
- Residual risks and untested paths are explicitly called out.

## Workflow
1. Build change context and identify high-risk areas.
2. Review for correctness and behavioral regressions.
3. Review maintainability and architectural fit.
4. Assess verification sufficiency and operational risk.
5. Publish findings first, then questions, then concise summary.

## Failure Conditions
- Stop when critical correctness issues block safe merge.
- Escalate when required context or evidence is unavailable for high-risk changes.
