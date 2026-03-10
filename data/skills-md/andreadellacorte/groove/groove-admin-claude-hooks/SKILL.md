---
name: groove-admin-claude-hooks
description: "Install groove's Claude Code native shell hooks into .claude/settings.json. Enables deterministic session-end reminders, git activity capture, and managed-path protection."
license: MIT
allowed-tools: Read Write Edit Glob Bash(git:*) Bash(mkdir:*) Bash(chmod:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-claude-hooks

Install groove's Claude Code native shell hooks. These run outside the model — deterministic, unconditional — and complement groove's advisory markdown hooks (`.groove/hooks/start.md`, `end.md`).

Use `--disable <hook>` to remove a specific hook. Use `--list` to show current status.

## Outcome

Selected hooks are registered in `.claude/settings.json` and shell scripts are written to `.groove/hooks/claude/`. Hooks fire automatically on Claude Code lifecycle events without any model involvement.

## Available hooks

| Name | Event | Matcher | What it does |
|---|---|---|---|
| `daily-end-reminder` | `Stop` | — | If hour is 16–21 local time and `.groove/index.md` exists, prints a reminder to run `/groove-daily-end` |
| `git-activity-buffer` | `PostToolUse` | `Bash` | If the Bash command contains `git commit`, appends a timestamped line to `.groove/.cache/git-activity-buffer.txt` |
| `block-managed-paths` | `PreToolUse` | `Write`, `Edit` | If `file_path` starts with `.agents/skills/groove` or `skills/groove`, exits non-zero to block the write with an explanatory message |
| `context-reprime` | `SessionStart` | `startup\|compact` | Runs the prime script directly — ensures full workflow context is loaded after every session start and compaction |
| `version-check` | `PostToolUse` | — | Checks for a new groove version once per hour; calls `groove-utilities-check` |

## Steps

### `--list`

Read `.claude/settings.json` if it exists. Report which groove hooks are registered and which scripts exist in `.groove/hooks/claude/`. Exit.

### `--disable <hook>`

Remove the named hook's entry from `.claude/settings.json` (leave the script in place). Report removed / not found. Exit.

### Default (install)

1. Ask which hooks to enable (default: all five):
   ```
   Which hooks to install? (all / comma-separated: daily-end-reminder, git-activity-buffer, block-managed-paths, context-reprime, version-check)
   Press enter for all.
   ```

2. Read `.claude/settings.json` if it exists; parse as JSON (default `{}`). Never discard existing non-groove entries.

3. Create `.groove/hooks/claude/` directory if absent. Make each script executable (`chmod +x`).

4. For each selected hook: write the shell script and merge the hook entry into `.claude/settings.json`.

5. Write `.claude/settings.json` with the merged result.

6. Report summary:
   ```
   ✓ daily-end-reminder  — Stop hook → .groove/hooks/claude/daily-end-reminder.sh
   ✓ git-activity-buffer — PostToolUse/Bash hook → .groove/hooks/claude/git-activity-buffer.sh
   ✓ block-managed-paths — PreToolUse/Write+Edit hook → .groove/hooks/claude/block-managed-paths.sh
   ✓ context-reprime     — SessionStart hook → groove-utilities-prime.sh
   ✓ version-check       — PostToolUse hook → .groove/hooks/claude/version-check.sh
   ✓ .claude/settings.json updated
   ```

## Shell script templates

Write these verbatim to `.groove/hooks/claude/`. Never overwrite an existing script without showing a diff and confirming.

### `daily-end-reminder.sh`

```bash
#!/usr/bin/env bash
# groove: Stop hook — remind about /groove-daily-end during work hours
hour=$(date +%H)
if [ -f ".groove/index.md" ] && [ "$hour" -ge 16 ] && [ "$hour" -le 21 ]; then
  echo "groove: end of work hours — consider running /groove-daily-end"
fi
```

### `git-activity-buffer.sh`

```bash
#!/usr/bin/env bash
# groove: PostToolUse/Bash hook — buffer git commits for memory log
input=$(cat)
command=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)
if echo "$command" | grep -q "git commit"; then
  msg=$(echo "$command" | grep -oP '(?<=-m ")[^"]+' | head -1)
  mkdir -p .groove/.cache
  echo "$(date '+%Y-%m-%d %H:%M') | ${msg:-<no message>}" >> .groove/.cache/git-activity-buffer.txt
fi
```

### `block-managed-paths.sh`

```bash
#!/usr/bin/env bash
# groove: PreToolUse/Write+Edit hook — block edits to managed groove paths
input=$(cat)
path=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
if echo "$path" | grep -qE '^(\.agents/skills/groove|skills/groove)'; then
  echo "groove: blocked — '$path' is managed by groove update. Edit under skills/ and rsync to .agents/skills/." >&2
  exit 1
fi
```

### `version-check.sh`

```bash
#!/usr/bin/env bash
# groove: PostToolUse hook — check for new groove version (once per hour)
CACHE=".groove/.cache/last-version-check-ts"
mkdir -p .groove/.cache
now=$(date +%s)
if [ -f "$CACHE" ]; then
  last=$(cat "$CACHE")
  diff=$((now - last))
  [ "$diff" -lt 3600 ] && exit 0
fi
echo "$now" > "$CACHE"
bash .agents/skills/groove-utilities-check/scripts/check.sh 2>/dev/null || true
```

## `.claude/settings.json` entries

Merge these into the `hooks` key. Preserve all other keys.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "bash .groove/hooks/claude/daily-end-reminder.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash .groove/hooks/claude/git-activity-buffer.sh" }
        ]
      },
      {
        "hooks": [
          { "type": "command", "command": "bash .groove/hooks/claude/version-check.sh" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "bash .groove/hooks/claude/block-managed-paths.sh" }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          { "type": "command", "command": "bash .groove/hooks/claude/block-managed-paths.sh" }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|compact",
        "hooks": [
          {
            "type": "command",
            "command": "bash .agents/skills/groove-utilities-prime/scripts/groove-utilities-prime.sh"
          }
        ]
      }
    ]
  }
}
```

When merging: if a `hooks` key already exists, append groove entries to the relevant event arrays. Do not create duplicates — check if a groove command entry already exists before appending.

## Constraints

- Never overwrite non-groove entries in `.claude/settings.json`
- Never overwrite an existing script without diff + confirmation
- Scripts use `python3` to parse JSON stdin — if python3 is absent, skip that hook and warn
- `block-managed-paths` is aggressive: if it causes false positives the user can disable it with `--disable block-managed-paths`
- After install: remind the user that hooks take effect on the next Claude Code session restart
- `.groove/hooks/claude/` follows the `git.hooks` git strategy from `.groove/index.md`
