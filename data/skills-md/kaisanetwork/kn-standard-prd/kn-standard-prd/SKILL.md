---
name: kn-standard-prd
description: Create high-quality Product Requirements Documents (PRDs) with a rigorous discovery interview, measurable requirements, clear scope boundaries, and validation checks. Use for requests like "create/write a PRD", "feature requirements", "one-pager", "lean PRD", or AI-feature specification.
compatibility:
  runtime: "POSIX shell environment with Bash available"
---

# KN Standard PRD

## Purpose

Produce execution-ready PRDs that align business, product, design, and engineering. This skill combines strict requirement quality, practical templates, and deterministic validation.

## When To Use

Use when the user asks to:

- Create or improve a PRD
- Document feature requirements
- Define scope and acceptance criteria
- Produce lean, one-pager, technical, or AI-feature PRDs

## Operating Principles

- Ask before drafting: do not write a full PRD without discovery.
- Be measurable: replace vague words with thresholds and target values.
- Separate `what/why` from `how`: avoid over-specifying implementation.
- Guard scope: explicitly list in-scope and out-of-scope.
- Preserve uncertainty: unknowns are written as `TBD` with owner and due date.

## Workflow

### 1) Discovery Interview (Required)

Ask focused questions and fill missing context. Use `references/discovery_question_bank.md`.

Minimum discovery bar:

- If user context is vague: ask at least 5 questions.
- If user gives a detailed brief: ask at least 2 critical gap questions.

Required topics:

- Problem and urgency
- Target users and use cases
- Business outcomes and success metrics
- Constraints (timeline, legal, platform, budget)
- Scope boundaries and non-goals

### 2) Select PRD Mode

Choose one mode with the user:

- `standard`: end-to-end production PRD
- `lean`: agile-friendly compact PRD
- `one-pager`: executive-level brief
- `technical`: engineering-heavy requirements
- `ai-feature`: adds model/tool/evaluation sections

Template sources:

- `references/prd_template_standard.md`
- `references/prd_template_lean.md`

### 3) Draft Requirements

For each major capability:

- Write user stories in standard format.
- Add acceptance criteria that are testable.
- Add non-functional requirements (performance, reliability, security, accessibility).

Story patterns: `references/user_story_examples.md`

### 4) Define Metrics

Pick a framework using `references/metrics_framework_selector.md`.

- Always define one North Star metric.
- Include leading and lagging indicators.
- Add baseline, target, and timeframe.

### 5) Quality Gate (Required)

Run validation:

```bash
scripts/validate_prd.sh <file.md> --mode <standard|lean|one-pager|technical|ai-feature>
```

Compatibility note:

- `scripts/validate_prd.sh` is a Bash script and must be run with Bash (`bash scripts/validate_prd.sh ...`).
- If Bash is unavailable in the environment, skip script execution and run a manual checklist from `references/prd_review_checklist.md`.

If validation reports critical issues, revise before presenting as final.

## Output Contract

A final PRD must contain at minimum:

- Problem statement
- Goals/objectives
- User stories with acceptance criteria
- Success metrics (with numeric targets)
- Scope (in + out)
- Risks and dependencies

For `ai-feature` mode, also include:

- Model/provider assumptions
- Evaluation dataset/benchmark plan
- Safety/privacy constraints
- Fallback behavior on low confidence

## Requirement Quality Standard

Bad:

- "Search should be fast"

Good:

- "p95 search latency <= 250ms on 100k records"

Bad:

- "Onboarding should be intuitive"

Good:

- "Activation rate >= 45% within first session"

## Anti-Patterns To Reject

- Writing PRD without discovery
- Missing out-of-scope section
- Acceptance criteria that are not testable
- Metrics without baseline/target/time window
- Placeholder-heavy drafts presented as final

## Bundled Resources

### references/

- `prd_template_standard.md`: full PRD structure
- `prd_template_lean.md`: compact structure for smaller changes
- `discovery_question_bank.md`: interview questions by scenario
- `metrics_framework_selector.md`: framework selection and examples
- `mode_selection_matrix.md`: how to choose the right PRD mode quickly
- `user_story_examples.md`: story and acceptance-criteria patterns
- `prd_review_checklist.md`: pre-signoff quality checklist

### scripts/

- `validate_prd.sh`: structure and quality checks with mode support

## Execution Notes

- Prefer concise, skimmable markdown.
- Keep stakeholder language clear and implementation-neutral.
- Where confidence is low, explicitly mark assumptions and open questions.
