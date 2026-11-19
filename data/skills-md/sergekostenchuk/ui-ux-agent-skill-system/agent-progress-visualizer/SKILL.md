---
name: agent-progress-visualizer
description: Use this skill when the user wants a human-readable project progress screen, agent work visualization, customer-facing status cockpit, immediate bootstrap progress before TASK-PLAN.md exists, task-plan-derived HTML progress page, user decision gates, or auto-updating UI/UX project status for senior-ui-ux-orchestrator workflows. It renders and validates progress views from project-request.json, workflow-log.jsonl, TASK-PLAN v2, progress-state.json, feedback artifacts, reports, and wiki decisions without becoming the source of truth.
---

# Agent Progress Visualizer

This skill creates and maintains a user-facing progress cockpit for UI/UX Agent Skill System projects. It translates canonical task-plan state into plain-language HTML for non-technical users.

It does not execute project tasks and does not own canonical status. Before planning, `project-request.json` and `workflow-log.jsonl` are only bootstrap sources. After planning, `TASK-PLAN.md` becomes the source of truth.

## Operating Modes

- `bootstrap`: create the first visible progress screen immediately after the system accepts a substantial user request, before `TASK-PLAN.md` exists.
- `init`: create or replace the first task-plan-derived progress-state and progress screen after `TASK-PLAN.md` exists.
- `update`: regenerate state and HTML after task-plan, report, artifact, feedback, or wiki changes.
- `review`: inspect an existing progress screen for source-of-truth drift, fake status, privacy leaks, or confusing copy.
- `feedback-gate`: expose user decisions and comments, then hand them to `design-feedback-collector`.
- `developer-view`: reveal technical task ids, skill routes, dependencies, and artifact paths without changing customer copy.

## Required Workflow

1. Read [references/data-source-contract.md](references/data-source-contract.md).
2. Read [references/decision-framework.md](references/decision-framework.md).
3. Read [references/safety-boundaries.md](references/safety-boundaries.md).
4. In `bootstrap` mode, do not wait for `TASK-PLAN.md`. Immediately create `project-request.json`, append `workflow-log.jsonl`, build a minimal `progress-state.json`, render `agent-progress-screen.html`, and open it in the browser. In the local project implementation, use `bootstrap_progress_screen.py --open-browser`.
5. After the bootstrap screen exists, route to `task-plan-v2-orchestrator` to create canonical `TASK-PLAN.md`.
6. In `init` or `update` mode, locate canonical `TASK-PLAN.md`. If no canonical task plan exists and bootstrap has not run, run bootstrap first, then route to `task-plan-v2-orchestrator`.
7. Build or update `progress-state.json` from canonical task-plan fields, reports, artifacts, feedback state, and sanitized wiki decisions.
8. If a declared journey exists, include `journey_alignment` from the journey registry and route skip/rework/block decisions through `workflow-compliance-supervisor`.
9. Render `agent-progress-screen.html` as a derived view. Do not edit HTML as the only state change.
10. In task-plan-derived `init` mode, open the rendered HTML in the browser immediately after creation. In the local project implementation, pass `--open-browser` to `render_progress_screen.py`. In `update` mode, open it only when the user asks or is actively reviewing.
11. For user choices, comments, approvals, or rejections, route durable capture to `design-feedback-collector`.
12. For large multi-session projects, route accepted decisions to `project-wiki-manager` after sanitization.
13. Validate consistency before claiming the progress screen is ready.

## Source-Of-Truth Rules

- In bootstrap mode, `project-request.json` and `workflow-log.jsonl` are temporary startup sources.
- After planning, `TASK-PLAN.md` is canonical.
- `progress-state.json` is derived machine-readable state.
- `agent-progress-screen.html` is a derived visual layer.
- If Markdown, JSON, and HTML disagree, fix Markdown or the generator first, then regenerate.
- Browser-only `localStorage` or clipboard state is not accepted as the only record of a decision.

## What To Generate

Default local artifacts:

```text
project-request.json
TASK-PLAN.md
progress-state.json
agent-progress-screen.html
workflow-log.jsonl
feedback/progress-feedback-register.schema.json
reports/progress-validation-summary.txt
```

Use [assets/progress-state.template.json](assets/progress-state.template.json) when a project needs a starter state before a generator exists.

## Human-Language Rules

- Customer mode says "Собираем поисковые запросы", not `serp-keyword-harvester`.
- Customer mode says "Ждет ваш выбор", not `required_approvals`.
- Developer mode may show task ids, skill routes, dependencies, and artifact paths.
- Never show secrets, tokens, recovery codes, cookies, `.env` values, private screenshots, or private URLs.

## Validation

When using the local project implementation, prefer these checks:

```bash
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/bootstrap_progress_screen.py" --project-root "$PROJECT_ROOT" --project-title "$PROJECT_TITLE" --user-request "$USER_REQUEST" --journey-registry "$UIUX_SKILL_SYSTEM_ROOT/data/journey-registry.json" --declared-journey new-premium-site --open-browser
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/check_bootstrap_progress.py" --project-root "$PROJECT_ROOT"
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/generate_progress_state.py" --task-plan "$UIUX_SKILL_SYSTEM_ROOT/TASK-PLAN.md" --out "$UIUX_SKILL_SYSTEM_ROOT/progress-state.json"
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/render_progress_screen.py" --state "$UIUX_SKILL_SYSTEM_ROOT/progress-state.json" --out "$UIUX_SKILL_SYSTEM_ROOT/agent-progress-screen.html"
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/check_progress_consistency.py" --task-plan "$UIUX_SKILL_SYSTEM_ROOT/TASK-PLAN.md" --state "$UIUX_SKILL_SYSTEM_ROOT/progress-state.json" --html "$UIUX_SKILL_SYSTEM_ROOT/agent-progress-screen.html"
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/validate_workflow_compliance.py" --fixtures
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/no_secret_scan.py" "$UIUX_SKILL_SYSTEM_ROOT"
```

For first creation of a user-facing project progress screen before `TASK-PLAN.md`, bootstrap with browser opening:

```bash
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/bootstrap_progress_screen.py" --project-root "$PROJECT_ROOT" --project-title "$PROJECT_TITLE" --user-request "$USER_REQUEST" --open-browser
```

After `TASK-PLAN.md` exists, replace the bootstrap state with task-plan-derived state:

```bash
python3 "$UIUX_SKILL_SYSTEM_ROOT/scripts/render_progress_screen.py" --state "$PROJECT_ROOT/progress-state.json" --out "$PROJECT_ROOT/agent-progress-screen.html" --open-browser
```

Skill package checks:

```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py $CODEX_HOME/skills/agent-progress-visualizer
python3 $CODEX_HOME/skills/senior-skill-architect/scripts/lint_production_skill.py $CODEX_HOME/skills/agent-progress-visualizer
```

## Handoff Shape

```text
Progress mode:
Bootstrap request:
Canonical task plan:
Generated state:
Generated HTML:
User gates:
Feedback artifact:
Wiki sync:
Checks run:
Skipped checks:
Next owner:
```
