---
name: context-task-planning
description: Task-scoped context engineering for complex multi-step work. Use when a task needs clarification, phased execution, durable file-backed state, recovery after context loss, or optional sub-agent delegation.
allowed-tools: Read Write Edit Bash Glob Grep
---

# Context Task Planning

Use persistent planning files as a task-scoped context system.

This is the TraeCLI/Coco-visible entry point for the same shared runtime that also supports Claude Code, OpenCode, Codex, and shell-first fallback usage. The full source of truth lives under the plugin root's `skill/` directory.

## When to use

Use this skill when work is multi-step, interruption-prone, or large enough that the live chat history is not a safe source of truth.

## Core workflow

Each task lives under `.planning/<slug>/` with:

- `state.json` for operational truth
- `task_plan.md` for framing and hot context
- `progress.md` for checkpoints and verification
- `findings.md` for durable discoveries

Automatic skill selection does not authorize task creation. First assess whether the request is broad, multi-step, verification-heavy, long-running, or likely to be interrupted. Simple and one-shot work continues without a task question; unclear scope gets a small read-only inspection before deciding. Only when durable tracking would help should you ask whether the user wants a task. Explicit task-init requests skip this opt-in question. After the user opts in, make sure the task has a goal, non-goals, acceptance criteria, constraints, and a next action. If you infer a task title from the request, show both the candidate title and candidate slug, then ask the user to confirm or edit the final title and slug before creating `.planning/<slug>/`.

## TraeCLI/Coco plugin paths

When installed as a TraeCLI/Coco plugin, prefer these paths:

```bash
sh "${COCO_PLUGIN_ROOT}/skill/scripts/init-task.sh" --title "<final task title>" --slug "<final task slug>"
sh "${COCO_PLUGIN_ROOT}/skill/scripts/current-task.sh"
sh "${COCO_PLUGIN_ROOT}/skill/scripts/current-task.sh" --compact
sh "${COCO_PLUGIN_ROOT}/skill/scripts/check-task-drift.sh" --prompt "<new request>" --json
sh "${COCO_PLUGIN_ROOT}/skill/scripts/validate-task.sh"
```

For detailed protocol rules, read `${COCO_PLUGIN_ROOT}/skill/SKILL.md` and `${COCO_PLUGIN_ROOT}/skill/reference.md` if those paths are available. Keep host adapters thin and reuse `skill/scripts/` instead of inventing a parallel workflow.
