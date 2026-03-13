---
name: review-team
description: Run multi-agent code review by profiling risk, selecting reviewer personas, spawning sub-agents, and merging structured findings into one severity-ordered report.
---

# Review Team

Use this skill when review quality matters and one reviewer would miss things.

## Load references in this order

- `references/scope-discovery.md`
- `references/intent-discovery.md`
- `references/preflight-risk-model.md`
- `references/persona-selection.md`
- `references/orchestration.md`
- `references/subagent-template.md`
- `references/findings-schema.json`
- `references/merge-normalization.md`
- `references/arbiter-pass.md`
- `references/action-synthesis.md`
- `references/severity-rubric.md`
- `references/output-format.md`
- `references/personas/catalog.md`
- Only the selected persona files in `references/personas/`

## Workflow

1. **Resolve review scope**
   - If there are working-copy changes, treat those as the default scope.
   - If working copy is clean, inspect unpushed commits and decide if they are the intended scope.
   - If scope is ambiguous, ask the user one direct question with options.

2. **Understand intent before reviewing**
   - Gather intent from conversation context, commit messages, PR/bead references, and docs.
   - If intent is still fuzzy, ask one short clarifying question.

3. **Run preflight profile and risk tagging**
   - Measure file count, changed lines, file types, and critical-path indicators.
   - Apply `references/preflight-risk-model.md` and record risk tags.
   - Use this profile as input for persona scoring and concurrency plan.

4. **Choose personas and assignment matrix**
   - Score personas with deterministic rules from `references/persona-selection.md`.
   - Build disjoint ownership slices by directory, service, or commit chunk.
   - Duplicate overloaded personas for large scopes (`-a`, `-b`, `-c`).

5. **Announce execution note before spawn**
   - Publish scope, intent, risk summary, reviewer designations, and wave plan.
   - This is progress reporting, not a blocking confirmation step.

6. **Spawn sub-agents with hard constraints**
   - Respect platform sub-agent limits when known.
   - If no clear limit is available, use a conservative cap of `6` concurrent sub-agents and run in waves.
   - Sub-agents are reviewers only; they do not edit code.
   - Each sub-agent must return JSON that matches `references/findings-schema.json`.

7. **Merge and normalize findings**
   - Apply `references/merge-normalization.md` for validation, dedupe, and reconciliation.
   - Reconcile severity with `references/severity-rubric.md`.
   - If conflicts remain after merge rules, run targeted arbitration from `references/arbiter-pass.md`.
   - Keep only actionable findings with concrete code evidence.
   - Suppress findings below `0.50` confidence.

8. **Synthesize top actions**
   - Derive grouped remediation actions from merged findings using `references/action-synthesis.md`.
   - Prioritize actions by severity and confidence.

9. **Produce one final report**
   - Organize primarily by severity.
   - Include secondary domain summary plus coverage gaps.
   - Do not output an overall pass/fail verdict.
   - Keep the report issues-first and actionable.

## Non-negotiables

- No style-only nits unless they carry real operational risk.
- Every finding must include concrete `file` and `line` references.
- Every finding must include `evidence` and `confidence`.
- Suppress findings below `0.50` confidence.
- Sub-agent output must conform to `references/findings-schema.json`.
- If no actionable findings exist, say so directly and list residual risks/testing gaps.
