---
name: dig
description: Mine Claude Code sessions — timeline, gaps, repo attribution. Use when user says "dig", "sessions", "past sessions", "timeline", "what did I work on".
---

# /dig - Session Goldminer

Mine Claude Code session data for timelines, gaps, and repo attribution. No query needed.

## Usage

```
/dig                    # Current repo, 10 most recent
/dig [N]                # Current repo, N most recent
/dig --all              # All repos, 10 most recent
/dig --all [N]          # All repos, N most recent
/dig --timeline         # Day-by-day grouped (current repo)
/dig --all --timeline   # Day-by-day grouped (all repos)
```

## Step 0: Timestamp

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

---

## Step 1: Discover Project Dirs

**Default** (current repo only):
```bash
PROJECT_BASE=$(ls -d "$HOME/.claude/projects/"*"$(basename "$(pwd)")" 2>/dev/null | head -1)
export PROJECT_DIRS="$PROJECT_BASE"
for wt in "${PROJECT_BASE}"-wt*; do [ -d "$wt" ] && export PROJECT_DIRS="$PROJECT_DIRS:$wt"; done
```

Uses `basename` of `pwd` to match the repo name suffix (avoids `github.com` vs `github-com` encoding mismatch). Also picks up worktree dirs (`-wt`, `-wt-1`, etc.).

**With `--all`** (all repos):
```bash
export PROJECT_DIRS=$(ls -d "$HOME/.claude/projects/"*/ | tr '\n' ':')
```

## Step 2: Extract Session Data

Run the dig script (pass N if user specified a count, default 10):

```bash
python3 ~/.claude/skills/dig/scripts/dig.py [N]
```

## Step 3: Display Timeline

Read the JSON output and display as a table. Sessions are chronological (oldest first). Gap rows (`type: "gap"`) span the session column with `· · ·` prefix:

```markdown
## Session Timeline

| # | Date | Session | Min | Repo | Msgs | Focus |
|---|------|---------|-----|------|------|-------|
|   |      | · · · sleeping / offline | | | | |
| 1 | 02-21 | 08:40–09:08 | 28m | oracle-skills-cli | 5 | Wire /rrr to read pulse data |
|   |      | · · · 45m gap | | | | |
| 2 | 02-21 | 09:55–10:23 | 28m | homelab | 3 | oracle-pulse birth + CLI flag |
|   |      | · · · no session yet | | | | |

**Dirs scanned**: [list PROJECT_DIRS]
**Total sessions found**: [count]
```

Column rendering rules:
- **Gap rows**: `|   |      | · · · [label] | | | | |` — number + date empty, label in Session col
- **Date**: `MM-DD` short format (strip year)
- **Session**: `HH:MM–HH:MM` using `startGMT7` and `endGMT7` (strip date, keep time only)
- **Min**: `[durationMin]m`
- **Repo**: use `repoName` field from dig.py output (resolved via ghq)
- **Msgs**: `realHumanMessages` count

"Msgs" = real typed human messages (not tool approvals).

---

## With --timeline: Group by Date

When `--timeline` flag is present, group sessions by date instead of a flat table. Use `--all` to see all repos (recommended for timeline).

**Step 1**: Run dig.py with large N (e.g. 200 for `--all`, or user-specified count)

**Step 2**: Group sessions by date from `startGMT7`. Render each day as:

```markdown
## Feb 22 (Sun) — [vibe label]

                  · · ·   sleeping / offline
08:48–09:11    23m   homelab        Update Fleet Runbook + Explore black.local
09:11–11:30   139m   homelab        Set Up KVM OpenClaw Node on black.local
09:37–12:51   194m   Nat-s-Agents   /recap → supergateway → CF ZT → oracle-v2 dig
                  · · ·   45m gap
12:51–13:03    12m   Nat-s-Agents   Dig All + Design oracle-v2 ← current
                  · · ·   no session yet

## Feb 21 (Sat) — Long day: Fleet + Brewing + Skills

06:19–08:38   139m   homelab        Moltworker Gateway + MBP Node
08:40           (bg)  openclaw       ClawHub Build Script (idle long)
09:23–16:08   405m   homelab        Debug MBP Node 401 — Gateway Token Auth
```

**Rendering rules**:
- **Day header**: `## MMM DD (Day) — [vibe label]` — infer vibe from session summaries (e.g. "Infrastructure Day", "Brewing + Skills")
- **Session rows**: `HH:MM–HH:MM  [N]m  REPO  Summary` — use `repoName` for repo, `summary` for focus
- **Gap rows**: `· · ·  [label]` between sessions when gap > 30 min
- **Sidechain**: prefix `(bg)` for sessions with `isSidechain: true`
- **Current**: append `← current` marker on the last session of the current day (today only)
- **Sort**: days newest-first, sessions within each day oldest-first (chronological)
- **Date format**: `startGMT7` time portion only (HH:MM), `endGMT7` time portion (HH:MM)
- **Repo width**: pad repo names to align columns

**Step 3**: Show summary footer:
```markdown
**Days**: [count] | **Sessions**: [count] | **Total time**: [sum of durationMin]m
```

---

## No trace log

`/dig` does NOT write a trace log file or call oracle_trace. It's a read-only scan. Output goes to screen only.

---

ARGUMENTS: $ARGUMENTS
