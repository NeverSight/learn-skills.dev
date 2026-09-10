---
name: admin-ui-builder
description: "Use when admin/CMS/back-office screens need to be built or specified after admin-ui-orchestrator defines roles, permissions, workflows, and safety gates. Covers tables, forms, editors, moderation queues, dashboards, CRUD surfaces, and state coverage without production destructive actions."
---

# Admin UI Builder

This skill builds or specifies admin UI surfaces under an existing admin architecture contract.

## Operating Modes

- `screen-spec`: define admin screens, states, forms, tables, filters, and validation.
- `implementation-handoff`: prepare local UI implementation tasks.
- `state-coverage`: cover empty, loading, error, permission denied, audit, and confirm states.

## Required Workflow

1. Read [references/admin-ui-build-contract.md](references/admin-ui-build-contract.md).
2. Use [assets/admin-screen-spec.template.md](assets/admin-screen-spec.template.md).
3. Confirm roles, permissions, destructive actions, and audit requirements from `admin-ui-orchestrator`.
4. Do not hide security and permission states for visual simplicity.

## Safety Rules

- Do not run production admin mutations.
- Every destructive action needs explicit confirmation UI and rollback/audit story.
- Never expose secrets, tokens, private customer data, or raw logs in UI examples.

## Validation

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/admin-ui-builder
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/admin-ui-builder
python3 -m json.tool $CODEX_HOME/skills/admin-ui-builder/evals/evals.json >/dev/null
```
