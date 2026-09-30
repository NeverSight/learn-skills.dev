---
name: task-done
description: Mark a context-task-planning task done after verification and summarize any blockers if completion is refused. Use this whenever the user wants to finish a task, mark tracked work done, close the current task after verification, or explicitly invokes /task-done.
allowed-tools: Bash
---

# Task Done

Mark a `context-task-planning` task done after verification.

## Requirements

- Expect the main `context-task-planning` skill to be installed alongside this entry skill.
- If the user provided an invocation argument, treat it as the task slug; otherwise operate on the current task.
- Resolve the core script from the installed host path: prefer `${CLAUDE_SKILL_DIR}/../../skill/scripts/done-task.sh` for Claude plugin installs, `${COCO_PLUGIN_ROOT}/skill/scripts/done-task.sh` for TraeCLI/Coco plugin installs, `$HOME/.codex/plugins/context-task-planning/skill/scripts/done-task.sh` for Codex plugin installs, then standalone skill paths under `$HOME/.claude/skills/`, `$HOME/.codex/skills/`, `$HOME/.config/opencode/skills/`, and finally repo-local `skill/scripts/done-task.sh`.
- Run the command from the current workspace.
- Do not bypass the script's safety checks. `done-task.sh` requires `state.verify_commands` and matching successful rows in `progress.md` under `## Verification Log`. If the script reports missing verification evidence, blockers, active delegates, or blocked phases, stop and summarize the issue instead of trying to force completion.
- After the command succeeds, summarize which task was marked done and remind the user that they can archive it later when they no longer need it in active lists.

## Run

Run the matching command for whether a slug argument was provided.

```bash
core=""
for candidate in \
  "${CLAUDE_SKILL_DIR:-}/../../skill/scripts/done-task.sh" \
  "${COCO_PLUGIN_ROOT:-}/skill/scripts/done-task.sh" \
  "$HOME/.codex/plugins/context-task-planning/skill/scripts/done-task.sh" \
  "$HOME/.claude/skills/context-task-planning/scripts/done-task.sh" \
  "$HOME/.codex/skills/context-task-planning/scripts/done-task.sh" \
  "$HOME/.config/opencode/skills/context-task-planning/scripts/done-task.sh" \
  "skill/scripts/done-task.sh"; do
  [ -f "$candidate" ] && core="$candidate" && break
done
[ -n "$core" ] || { echo "context-task-planning done-task.sh not found" >&2; exit 1; }
# No slug argument:
sh "$core"

# With a slug argument:
sh "$core" "<slug>"
```
