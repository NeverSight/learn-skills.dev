---
name: design-feedback-collector
description: Collect, structure, deduplicate, and resolve user and agent feedback on UI/UX skills, subprocesses, design directions, progress-screen gates, Stitch/Pencil/Figma outputs, and implementation steps. Use when comments need statuses such as open, accepted, partially accepted, applied, rejected, or when review-board/progress-page fields must become actionable decisions.
---

# Design Feedback Collector

This skill turns comments into a controlled feedback register. It is not a visual critic by itself; it structures feedback so the chair and specialist skills can act without losing context.

## Operating Modes

- `collect`: gather user comments, agent critiques, and review-board notes.
- `triage`: assign severity, owner, affected skill, affected subprocess, and decision status.
- `resolve`: convert feedback into accepted, partially accepted, rejected, or applied decisions.
- `sync-dashboard`: update review-board or task-plan-facing summaries.
- `sync-progress`: update progress-screen user gates and feedback artifacts after a user decision.
- `handoff`: send accepted feedback to the right specialist skill.

## Required Workflow

1. Read [references/feedback-status-contract.md](references/feedback-status-contract.md).
2. Use [assets/feedback-register.schema.json](assets/feedback-register.schema.json) as the register shape.
3. Separate feedback sources:
   - user comment;
   - colleague/agent critique;
   - validation finding;
   - council decision.
4. Assign each item:
   - target skill or subprocess;
   - severity;
   - status;
   - owner;
   - required action;
   - evidence needed.
5. Use color/status semantics:
   - blue: no comment/open empty state;
   - red: unresolved comment exists;
   - orange: partially accepted or partially applied;
   - green: accepted and applied.
6. For progress-screen gates, preserve `gate_id`, selected option, comment, target phase/subprocess, and source artifact.
7. Do not mark an item applied unless the changed artifact or decision record is referenced.

## Safety Rules

- Remove secrets, tokens, private URLs, `.env` values, recovery codes, and private screenshots from feedback before saving.
- Do not collapse disagreement into a fake consensus; preserve rejected and partially accepted reasoning.
- For high-impact disagreements, route to `senior-ui-ux-orchestrator` in council mode.

## Handoff Shape

```text
Feedback mode:
Target skill/subprocess:
Source:
Status:
Severity:
Decision:
Applied artifact:
Open risk:
Next owner:
```

## Validation

When editing this skill, run:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/design-feedback-collector
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/design-feedback-collector
python3 -m json.tool $CODEX_HOME/skills/design-feedback-collector/evals/evals.json >/dev/null
```
