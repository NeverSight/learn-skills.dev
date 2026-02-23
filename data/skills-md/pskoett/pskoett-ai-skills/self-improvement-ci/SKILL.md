---
name: self-improvement-ci
description: "CI-only self-improvement workflow using gh-aw (GitHub Agentic Workflows). Captures recurring failure patterns and quality signals from pull request checks, emits structured learning candidates, and proposes durable prevention rules without interactive prompts. Use when: you want automated learning capture in CI/headless pipelines."
---

# Self-Improvement CI

## Install

```bash
npx skills add pskoett/pskoett-ai-skills/self-improvement-ci
```

## Purpose

Run self-improvement in CI without interactive chat loops:

- Inspect PR check results and CI failures
- Ingest learning candidates from `simplify-and-harden-ci`
- Deduplicate recurring patterns by stable `pattern_key`
- Emit promotion-ready suggestions for agent context/system prompts

Use `self-improvement` for interactive/local sessions.

## Context Limitation (Important)

CI agents do **not** have peak task context from the original implementation
session. Use this skill to aggregate recurring patterns across runs, not to
infer nuanced one-off intent.

Implications:
- Favor stable `pattern_key` recurrence signals over single-run conclusions
- Require recurrence thresholds before promotion
- Route uncertain or high-impact recommendations to interactive review

## Prerequisites

1. GitHub Actions enabled for the repository
2. GitHub CLI authenticated (`gh auth status`)
3. `gh-aw` installed for authoring/validation:

```bash
gh extension install github/gh-aw
```

## CI Contract

The CI skill must:

1. Read only PR-scoped data (checks, workflow outcomes, existing learning entries)
2. Avoid direct code modifications in CI
3. Emit machine-readable learning output
4. Recommend promotion only when recurrence thresholds are met

## Output Schema

```yaml
self_improvement_ci:
  source:
    pr_number: 123
    commit_sha: "abc123"
  candidates:
    - pattern_key: "harden.input_validation"
      source: "simplify-and-harden-ci"
      recurrence_count: 3
      first_seen: "2026-02-01"
      last_seen: "2026-02-20"
      severity: "high"
      suggested_rule: "Validate and bound-check external inputs before use."
      promotion_ready: true
  summary:
    candidates_total: 4
    promotion_ready_total: 1
    followup_required: true
```

## Recurrence and Promotion Rules

- Track recurrence by `pattern_key`
- Default threshold for promotion:
  - `recurrence_count >= 3`
  - seen in `>= 2` distinct tasks/runs
  - within a 30-day window
- Promotion targets:
  - `CLAUDE.md`
  - `AGENTS.md`
  - `.github/copilot-instructions.md`
  - `SOUL.md` / `TOOLS.md` when using openclaw workspace memory

## Authoring Workflow (gh-aw)

Example-only templates live in `references/workflow-example.md`.
Keep examples outside `.github/workflows` until you explicitly decide to enable CI automation.

When ready:
1. Copy the template into `.github/workflows/self-improvement-ci.md`
2. Customize tool access, outputs, and policy thresholds
3. Validate:

```bash
gh aw compile --validate --strict
```

4. Trigger test run manually:

```bash
gh aw run self-improvement-ci --push
```

## Integration with Other Skills

- Pair with `simplify-and-harden-ci` to ingest
  `simplify_and_harden.learning_loop.candidates`
- Feed promoted patterns back into `self-improvement` memory workflow for durable prevention rules
