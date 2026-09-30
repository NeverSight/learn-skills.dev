---
name: task-init
description: Initialize a new context-task-planning task for this workspace from a confirmed task title and final task slug. Use this whenever the user wants to start tracking a new task, create a planning lane, initialize task files, or explicitly invokes /task-init.
allowed-tools: Bash
---

# Task Init

Initialize a new `context-task-planning` task for this workspace using a confirmed task title and the final task slug.

## Requirements

- Expect the main `context-task-planning` skill to be installed alongside this entry skill.
- Treat the invocation argument text as an already-confirmed task title. Derive the slug that the core `slugify.sh` script would produce unless the user explicitly asks to override it.
- If no task title was provided but the surrounding user request implies a task, infer a concise candidate title, derive the slug that the core `slugify.sh` script would produce, and show both the candidate title and candidate slug before running `init-task.sh`.
- If no task title was provided and there is not enough surrounding request context to infer one, stop and ask the user for a task title.
- Do not create a task from an agent-inferred title until the user confirms the final title and slug.
- When you surface a candidate task, ask the user to confirm or edit both the title and the slug.
- If the user edits the title but does not explicitly override the slug, recompute the slug from the final title before running the command.
- If the user explicitly edits the slug, pass that slug through `init-task.sh --slug`; the core script will still normalize it with `slugify.sh` before creating the task.
- Resolve the core script from the installed host path: prefer `${CLAUDE_SKILL_DIR}/../../skill/scripts/init-task.sh` for Claude plugin installs, `${COCO_PLUGIN_ROOT}/skill/scripts/init-task.sh` for TraeCLI/Coco plugin installs, `$HOME/.codex/plugins/context-task-planning/skill/scripts/init-task.sh` for Codex plugin installs, then standalone skill paths under `$HOME/.claude/skills/`, `$HOME/.codex/skills/`, `$HOME/.config/opencode/skills/`, and finally repo-local `skill/scripts/init-task.sh`.
- Run the command from the current workspace.
- If the dirty-worktree guard asks for a decision, stop and ask the user instead of choosing `--stash` or `--allow-dirty` yourself.
- After the command succeeds, summarize the created task slug and the next action.

## Run

```bash
core=""
for candidate in \
  "${CLAUDE_SKILL_DIR:-}/../../skill/scripts/init-task.sh" \
  "${COCO_PLUGIN_ROOT:-}/skill/scripts/init-task.sh" \
  "$HOME/.codex/plugins/context-task-planning/skill/scripts/init-task.sh" \
  "$HOME/.claude/skills/context-task-planning/scripts/init-task.sh" \
  "$HOME/.codex/skills/context-task-planning/scripts/init-task.sh" \
  "$HOME/.config/opencode/skills/context-task-planning/scripts/init-task.sh" \
  "skill/scripts/init-task.sh"; do
  [ -f "$candidate" ] && core="$candidate" && break
done
[ -n "$core" ] || { echo "context-task-planning init-task.sh not found" >&2; exit 1; }
sh "$core" --title "<final task title>" --slug "<final task slug>"
```
