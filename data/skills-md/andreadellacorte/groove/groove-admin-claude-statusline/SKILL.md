---
name: groove-admin-claude-statusline
description: "Install a rich Claude Code statusline into ~/.claude/hooks/ and ~/.claude/settings.json. Displays model, git context, token usage, effort level, 5h/7d usage limits, and active /loop count with next-fire time."
license: MIT
allowed-tools: Read Write Edit Glob Bash(mkdir:*) Bash(chmod:*) Bash(jq:*) Bash(python3:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-admin-claude-statusline

Install a rich single-line Claude Code statusline. Writes three scripts to `~/.claude/hooks/` and merges config into `~/.claude/settings.json`.

Use `--uninstall` to remove. Use `--list` to show current status.

## Outcome

`~/.claude/settings.json` has `statusLine` pointing to the statusline script, plus PostToolUse and SessionEnd hooks to track active `/loop` cron jobs. The statusline shows on every Claude Code turn.

## What the statusline shows

```
claude-sonnet-4-6 | myrepo@main (+3 -1) | 42k/200k (21%) | effort: high | 5h 12% @8:00pm | 7d 3% @mar 16, 9:00am | 2 loops | check deployment @4:10pm
```

| Section | Description |
|---|---|
| Model | Display name of the active model |
| Repo@branch | CWD folder name, git branch, staged diff `+N -N` |
| Tokens | Used / total context, % used |
| Effort | Current effort level (low / med / high) |
| 5h / 7d | Rate-limit utilisation with reset time (cached 60s) |
| Loops | Count of active `/loop` crons + soonest-firing prompt and time |

## Steps

### `--list`

Read `~/.claude/settings.json`. Report whether `statusLine` is set, and whether each hook script exists in `~/.claude/hooks/`. Exit.

### `--uninstall`

Remove `statusLine` from `~/.claude/settings.json`. Remove the three `CronCreate|CronDelete` / `SessionEnd` hook entries added by this skill. Do not remove hook scripts (leave for manual cleanup). Report changes. Exit.

### Default (install)

1. Create `~/.claude/hooks/` if absent.

2. Write the three scripts below to `~/.claude/hooks/`. Never overwrite without showing a diff and confirming.

3. Make all three scripts executable (`chmod +x`).

4. Read `~/.claude/settings.json` (default `{}`). Merge in the `statusLine` entry and the two hook entries below. Preserve all other keys. Do not create duplicate entries.

5. Write `~/.claude/settings.json`.

6. Report:
   ```
   ✓ statusline.sh         → ~/.claude/hooks/statusline.sh
   ✓ cron-state.sh         → ~/.claude/hooks/cron-state.sh
   ✓ cron-state-clear.sh   → ~/.claude/hooks/cron-state-clear.sh
   ✓ ~/.claude/settings.json updated
   Note: restart Claude Code for changes to take effect.
   ```

## Scripts

The three shell scripts live in `scripts/` per the [Agent Skills specification](https://agentskills.io/specification#scripts):

| Script | Installed to | Purpose |
|---|---|---|
| `scripts/statusline.sh` | `~/.claude/hooks/statusline.sh` | Main statusline renderer |
| `scripts/cron-state.sh` | `~/.claude/hooks/cron-state.sh` | Tracks `/loop` cron jobs in `/tmp/claude/loops.json` |
| `scripts/cron-state-clear.sh` | `~/.claude/hooks/cron-state-clear.sh` | Clears loop state on session end |

Copy each script from `scripts/` to `~/.claude/hooks/`. Never overwrite an existing script without showing a diff and confirming.

## `~/.claude/settings.json` entries

Merge these into the existing settings. Preserve all other keys. Do not create duplicates.

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/hooks/statusline.sh"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "CronCreate|CronDelete",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/cron-state.sh",
            "async": true
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/cron-state-clear.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

## Constraints

- Write to `~/.claude/hooks/` (user-global), not `.claude/` (project-local)
- Never overwrite an existing script without showing a diff and confirming
- Never discard existing keys in `~/.claude/settings.json`
- Requires: `jq`, `curl`, `python3`, `git` (all standard on macOS/Linux)
- The 5h/7d usage section requires a Claude Pro/Max OAuth session; it silently omits if no token is found
- After install: restart Claude Code for the statusLine and hooks to take effect
