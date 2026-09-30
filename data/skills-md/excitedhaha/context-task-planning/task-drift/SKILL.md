---
name: task-drift
description: Return heuristic route evidence for whether a new request still fits the current context-task-planning task and summarize the routing recommendation. Use this whenever the user asks whether a new ask belongs in the same task, wants a drift check, is about to switch scope, or explicitly invokes /task-drift.
allowed-tools: Bash
---

# Task Drift

Return heuristic route evidence for whether a new request still fits the current `context-task-planning` task.

## Requirements

- Expect the main `context-task-planning` skill to be installed alongside this entry skill.
- Treat the invocation argument text as the candidate new request.
- If no request text was provided, stop and ask the user to provide the request they want to compare against the current task.
- Resolve the core script from the installed host path: prefer `${CLAUDE_SKILL_DIR}/../../skill/scripts/check-task-drift.sh` for Claude plugin installs, `${COCO_PLUGIN_ROOT}/skill/scripts/check-task-drift.sh` for TraeCLI/Coco plugin installs, `$HOME/.codex/plugins/context-task-planning/skill/scripts/check-task-drift.sh` for Codex plugin installs, then standalone skill paths under `$HOME/.claude/skills/`, `$HOME/.codex/skills/`, `$HOME/.config/opencode/skills/`, and finally repo-local `skill/scripts/check-task-drift.sh`.
- Run the command from the current workspace.
- After the command succeeds, summarize the route evidence and mention any routing recommendation; do not present `unclear` as a final drift conclusion.

## Run

```bash
core=""
for candidate in \
  "${CLAUDE_SKILL_DIR:-}/../../skill/scripts/check-task-drift.sh" \
  "${COCO_PLUGIN_ROOT:-}/skill/scripts/check-task-drift.sh" \
  "$HOME/.codex/plugins/context-task-planning/skill/scripts/check-task-drift.sh" \
  "$HOME/.claude/skills/context-task-planning/scripts/check-task-drift.sh" \
  "$HOME/.codex/skills/context-task-planning/scripts/check-task-drift.sh" \
  "$HOME/.config/opencode/skills/context-task-planning/scripts/check-task-drift.sh" \
  "skill/scripts/check-task-drift.sh"; do
  [ -f "$candidate" ] && core="$candidate" && break
done
[ -n "$core" ] || { echo "context-task-planning check-task-drift.sh not found" >&2; exit 1; }
sh "$core" --prompt "<new request>" --json
```
