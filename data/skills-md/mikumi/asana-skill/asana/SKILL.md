---
name: asana
description: Access Asana workspaces, projects, users, and tasks through executable Python scripts using the official Asana Python SDK v5. Use when users mention Asana or tasks.
---

# Asana

Use this skill to run repeatable Asana actions through scripts instead of embedding one-off inline Python snippets.

## Execution Constraint

1. Use only predefined actions via `scripts/execute_action.py`.
2. Do not run ad hoc Asana SDK commands (`python3 -c`, heredocs, or direct one-off scripts) for skill operations.
3. All actions must be executed outside of the sandbox (otherwise the API calls will fail)

## Workflow

1. Run `scripts/check_prereqs.sh` before any Asana operation.
2. Run all actions through `scripts/execute_action.py`.
3. Treat read actions as default.
4. Require explicit user approval before using `--allow-write` for write actions.

## SDK Compatibility

1. Use Asana Python SDK v5 (`pip3 install asana`).
2. Follow the script implementation pattern: `asana.ApiClient` + `asana.<Resource>Api`.
3. Do not use legacy `asana.Client` examples in this skill.

## Action Execution

Run scripts from the skill folder:

```bash
cd /Users/michael/.codex/skills/asana
```

Show all available actions and modes:

```bash
scripts/execute_action.py --list-actions
```

Read operations:

```bash
scripts/execute_action.py current_user
scripts/execute_action.py list_workspaces
scripts/execute_action.py list_projects --workspace-gid <workspace_gid>
scripts/execute_action.py list_tasks --project-gid <project_gid>
scripts/execute_action.py list_tasks --project-gid <project_gid> --incomplete-only
scripts/execute_action.py get_task --task-gid <task_gid>
scripts/execute_action.py search_tasks --workspace-gid <workspace_gid> --text "<query>"
scripts/execute_action.py my_tasks --workspace-gid <workspace_gid>
```

Write operations (only after explicit approval):

```bash
scripts/execute_action.py --allow-write create_task --project-gid <project_gid> --name "<task title>" --notes "<optional notes>"
scripts/execute_action.py --allow-write update_task --task-gid <task_gid> --completed true
scripts/execute_action.py --allow-write update_task --task-gid <task_gid> --name "<new title>" --due-on 2026-03-10
scripts/execute_action.py --allow-write add_comment --task-gid <task_gid> --text "<comment>"
```

## Safety Rules

1. Keep default mode read-only.
2. Do not pass `--allow-write` without explicit user confirmation.
3. Do not print or expose `ASANA_ACCESS_TOKEN`.
4. Use minimal output fields and summarize results in clean tables.

## References

- Setup and privacy rules: `references/setup-and-privacy.md`
- Operation mapping and examples: `references/operations.md`
