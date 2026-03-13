---
name: git-history-investigation
description: "Reconstruct change history using log/show/diff/blame evidence to explain when and why behavior changed. Use when teams need evidence-based history analysis for regressions or ownership questions; do not use for CI workflow design or application behavior implementation."
---

# Git History Investigation

## Overview
Use this skill to produce an auditable evidence chain from symptom to likely root-cause commits.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Evidence quality rules:
  - `references/history-evidence-quality-rules.md`

## Templates And Assets
- Investigation log:
  - `assets/history-investigation-log-template.md`
- Root-cause hypothesis template:
  - `assets/root-cause-hypothesis-template.md`

## Inputs To Gather
- Reproducible symptom or unexpected behavior.
- Candidate paths/modules and relevant time window.
- Issue/PR/review metadata for context.
- Required confidence threshold for decision-making.

## Deliverables
- Chronological evidence trail.
- Root-cause hypothesis with alternative hypotheses.
- Confidence-rated conclusion and next action recommendation.

## Workflow
1. Define scope and symptom timeline in `assets/history-investigation-log-template.md`.
2. Gather direct evidence from log/show/diff/blame.
3. Form and test hypotheses with `assets/root-cause-hypothesis-template.md`.
4. Apply `references/history-evidence-quality-rules.md` to validate claim strength.
5. Publish findings and root-cause-oriented follow-up actions.

## Quality Standard
- Evidence chain links symptom timeline to concrete commit behavior.
- Root-cause claim includes supporting and disconfirming evidence.
- Alternatives are explicitly considered and resolved.
- Follow-up actions address cause, not just surface symptoms.

## Failure Conditions
- Stop when symptom cannot be scoped to a meaningful history window.
- Stop when evidence is mostly inferential without diff-level support.
- Escalate when confidence is too low for production-impacting decisions.
