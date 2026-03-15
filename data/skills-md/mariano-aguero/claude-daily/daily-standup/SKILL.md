---
name: daily-standup
description: >-
  Generate daily standup reports from git history, PRs, and a persistent work log.
  Use when the user says "daily", "standup", "what did I do yesterday",
  "generate my daily", "daily sync", "weekly review", or asks for a summary of recent work.
license: MIT
metadata:
  author: mariano-aguero
  version: "1.3"
---

# Daily Standup Generator

Generate daily standup reports automatically by cross-referencing git activity, GitHub PRs, and a persistent work log.

## Commands

- `/daily` — Generate the full daily standup report
- `/log <message>` — Manually log a work entry
- `/log-auto` — Auto-log a summary of the current session from git
- `/log-week` — Generate a weekly review summary
- `/log-clear` — Archive the current log and start fresh

## How `/daily` Works

### Step 1: Gather Data

First, check if a `<daily-worklog>` block is already present in the session context (injected at session start by the worklog hook). If it exists, use it as the work log data and skip re-reading the file.

If no `<daily-worklog>` block is in context, run these commands:

```bash
date "+%A %d/%m/%Y"
git branch --show-current
git status --short
```

Get commits since the last working day (Friday-aware on Mondays):

```bash
DAY=$(date +%u)
SINCE=$([ "$DAY" = "1" ] && echo "4 days ago" || echo "2 days ago")
git log --since="$SINCE" --format="%h %s (%ar)" --no-merges
```

If GitHub CLI is available:

```bash
gh pr list --author="@me" --state=all --limit=10
```

Read the work log (only if `<daily-worklog>` was not already in context):

```bash
grep -v '\[COMPACT\]' ~/.daily-worklog/current.md 2>/dev/null || true
```

### Step 2: Generate Report

```
## Daily Standup - [today's date]

### ✅ Yesterday (what I did)
- [summarize commits, merged PRs, completed tasks from work log]

### 🔨 Today (what I'll do)
- [based on: in-progress branches, open PRs, [HOY]/[TODAY] items from work log]

### 🚧 Blockers
- [items marked [BLOCKER] in work log, or PRs waiting for review]
```

### Rules

1. Be concise. One line per item.
2. Group related commits into a single item.
3. If no blockers exist, write "No blockers".
4. Items tagged `[BLOCKER]` always appear in Blockers.
5. Items tagged `[HOY]` / `[TODAY]` are prioritized in Today.
6. Use professional but direct language.
7. Work log entries use `[YYYY-MM-DD HH:MM]` format — use the date to determine recency. Ignore entries older than 3 days.
8. `[AUTO-STOP]` entries are session snapshots — treat as completed work summaries.
9. `[HOY]`/`[TODAY]` entries with a date older than 3 days are excluded from Today. No exceptions.

## How `/log` Works

When the user runs `/log <message>`:

1. Run `mkdir -p ~/.daily-worklog/archive`
2. Auto-archive entries older than 3 days (if the archive script is available):
   ```bash
   ARCHIVE_SCRIPT="$HOME/.claude/skills/daily-standup/scripts/archive-worklog.py"
   if [ -f "$ARCHIVE_SCRIPT" ]; then
     python3 "$ARCHIVE_SCRIPT"
   fi
   ```
   > **Note:** The archive script is only present when installed via `install.sh`. Users who installed via `npx skills add` will skip this step — entries are not auto-archived but can still be read by `/daily`.
3. Get current timestamp: `date "+%Y-%m-%d %H:%M"`
4. Append to `~/.daily-worklog/current.md`:
   ```
   - [YYYY-MM-DD HH:MM] <message>
   ```
5. Confirm what was logged and show entry count.

Supported tags: `[BLOCKER]`, `[HOY]`, `[TODAY]`

## How `/log-auto` Works

When the user runs `/log-auto`:

1. Run `git log --since="8 hours ago" --format="- %s" --no-merges`
2. Run `git diff --name-only HEAD~3 2>/dev/null || git diff --name-only HEAD 2>/dev/null || true`
3. Run `git branch --show-current`
4. Generate a 1-3 line summary of the session
5. Get current timestamp: `date "+%Y-%m-%d %H:%M"`
6. Append to `~/.daily-worklog/current.md`:
   ```
   - [YYYY-MM-DD HH:MM] [AUTO] <concise session summary>
   ```

## How `/log-week` Works

When the user runs `/log-week`:

### Step 1: Gather Data

```bash
date "+%A %d/%m/%Y"
git log --since="7 days ago" --format="%h %s (%as)" --no-merges
```

If GitHub CLI is available:

```bash
gh pr list --author="@me" --state=all --limit=20
```

Read current worklog and recent archives:

```bash
grep -v '\[COMPACT\]' ~/.daily-worklog/current.md 2>/dev/null || true
```

Also check archive files from the last 7 days:

```bash
python3 -c "
import os, datetime
d = datetime.date.today() - datetime.timedelta(days=7)
archive = os.path.expanduser('~/.daily-worklog/archive')
if not os.path.isdir(archive): exit()
for f in sorted(os.listdir(archive)):
    name = f.replace('.md','')[:10]
    try:
        if datetime.date.fromisoformat(name) >= d:
            with open(os.path.join(archive, f)) as fp: print(fp.read())
    except ValueError: pass
" 2>/dev/null || true
```

### Step 2: Generate Report

```
## Weekly Review - [date range: Mon DD/MM → today]

### 📅 What I shipped
- [commits grouped by day, most recent first]

### 📋 Notable work (non-git)
- [worklog entries that aren't AUTO-STOP, grouped by day]

### 🚧 Blockers this week
- [any [BLOCKER] entries from the week]

### 📊 Stats
- X commits across Y branches
- Z manual log entries
```

### Rules

1. Group commits by branch or feature, not by individual commit.
2. Skip `[AUTO-STOP]` entries in "Notable work" — they're redundant with git.
3. If no blockers, write "No blockers this week".

## How `/log-clear` Works

When the user runs `/log-clear`:

1. Show current log contents and entry count
2. Archive everything to a timestamped file:
   ```bash
   ARCHIVE_SCRIPT="$HOME/.claude/skills/daily-standup/scripts/archive-worklog.py"
   if [ -f "$ARCHIVE_SCRIPT" ]; then
     python3 "$ARCHIVE_SCRIPT" --all
   else
     # Fallback: move current log manually
     ts=$(date "+%Y-%m-%d-%H-%M")
     mkdir -p ~/.daily-worklog/archive
     mv ~/.daily-worklog/current.md ~/.daily-worklog/archive/${ts}.md
     touch ~/.daily-worklog/current.md
   fi
   ```
3. Confirm archival with entry count and archive filename.

## Work Log Persistence

```
~/.daily-worklog/
├── current.md              ← active log (entries from last 3 days)
└── archive/
    ├── 2026-03-08-09-30.md ← from /log-clear (timestamped)
    └── 2026-03-05.md       ← from auto-archival via /log
```

Entries older than 3 days are automatically archived each time `/log` is used.

## Entry Format

```
- [YYYY-MM-DD HH:MM] <message>
- [YYYY-MM-DD HH:MM] [TAG] <message>
```

| Tag | Effect on `/daily` |
|-----|-------------------|
| `[BLOCKER]` | Always shown in Blockers section |
| `[HOY]` / `[TODAY]` | Prioritized in Today (excluded if older than 3 days) |
| `[AUTO]` | Treated as completed work (from `/log-auto`) |
| `[AUTO-STOP]` | Treated as completed work (from session stop hook) |

## Tips for Best Results

- You don't need to log everything manually — `/daily` reads git history automatically
- Use `/log` for things that don't show up in git: meetings, decisions, blockers
- The session stop hook auto-logs `[AUTO-STOP]` entries on every close
- Run `/log-clear` on Monday mornings to start the week fresh
- Use `/log-week` for retrospectives or weekly syncs
