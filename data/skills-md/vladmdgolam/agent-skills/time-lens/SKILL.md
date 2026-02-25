---
name: time-lens
description: >
  Analyze and visualize time spent on software projects by combining data from multiple
  sources: WakaTime coding time, git commit session detection, Claude Code usage,
  Codex CLI usage, and Cursor IDE usage. Produces both an interactive HTML dashboard
  (dark-themed, Chart.js) and a Markdown report with ASCII charts. Use when the user
  asks to: analyze work hours, calculate time spent on a project, generate a work hours
  report, visualize coding activity, create a project time breakdown, or summarize
  development effort across date ranges.
---

# Project Time Tracker

Combines five data sources → reconciles → produces HTML dashboard + Markdown report.

## Scripts

All scripts live in `scripts/` next to this SKILL.md. Run them with `python3`:

| Script | Purpose | Key flags |
|--------|---------|-----------|
| `git_sessions.py` | Parse git history → sessions → hours | `<repo> --since YYYY-MM-DD --until YYYY-MM-DD` |
| `wakatime_fetch.py` | WakaTime API → daily hours, filtered to project | `--start YYYY-MM-DD --end YYYY-MM-DD --project name` |
| `claude_messages.py` | Claude Code user prompts per day + timestamps | `--project-path /abs/path` or `--filter name` |
| `codex_messages.py` | Codex CLI user prompts per day + timestamps | `--project-path /abs/path` or `--filter name` |
| `cursor_messages.py` | Cursor IDE user prompts per day + timestamps | `--project-path /abs/path` or `--filter name` |

## Workflow

### 1. Determine scope

Ask for or infer:
- Project directory/directories (git repos)
- Date range (first commit → last commit, or user-specified)
- Output location for HTML + markdown files

**Auto-discover sub-repos:** By default, scan the project directory for `.git` folders in subdirectories (not just the root). Each parent of a `.git` directory is a sub-repo to analyze.

```bash
# Find all git repos under the project directory
find /path/to/project -name ".git" -type d 2>/dev/null | sort
```

This produces a list like:
```
/path/to/project/frontend/.git
/path/to/project/backend/.git
/path/to/project/libs/shared/.git
```

Each of these (minus the `/.git` suffix) is a repo to run `git_sessions.py`, `claude_messages.py`, and `codex_messages.py` on. Also run these scripts on the root project directory itself (for Claude/Codex messages sent from the root, which is common when using monorepo-style workflows).

### 2. Extract data

Run all five scripts on every discovered repo. For git, Claude, Codex, and Cursor, run per sub-repo. For WakaTime, use the multi-project discovery approach described below.

```bash
# Git sessions — run per sub-repo
python3 git_sessions.py /path/to/project/frontend --since 2026-01-15 --until 2026-02-02
python3 git_sessions.py /path/to/project/backend --since 2026-01-15 --until 2026-02-02

# Claude Code — run per sub-repo AND the root directory
python3 claude_messages.py --project-path /path/to/project
python3 claude_messages.py --project-path /path/to/project/frontend
python3 claude_messages.py --project-path /path/to/project/backend

# Codex CLI — same as Claude
python3 codex_messages.py --project-path /path/to/project
python3 codex_messages.py --project-path /path/to/project/frontend
python3 codex_messages.py --project-path /path/to/project/backend

# Cursor IDE — same as Claude/Codex
python3 cursor_messages.py --project-path /path/to/project
python3 cursor_messages.py --project-path /path/to/project/frontend
python3 cursor_messages.py --project-path /path/to/project/backend
```

**WakaTime multi-project discovery:** WakaTime often tracks sub-directories as separate projects (e.g., a monorepo at `my-project/` may have WakaTime projects named `my-project`, `frontend`, `backend`, `shared`). A single `--project` query will miss the others.

1. First, run `wakatime_fetch.py` **without** `--project` to get the full project list for the date range:
   ```bash
   python3 wakatime_fetch.py --start 2026-01-15 --end 2026-02-02
   # Returns: { "projects": [{"project": "my-project", "hours": 9.2}, {"project": "frontend", "hours": 5.1}, ...] }
   ```

2. Filter the returned `projects` list for names matching any of:
   - The root project directory basename (e.g., `my-project`)
   - Any sub-repo directory basename (e.g., `frontend`, `backend`)
   - Any intermediate directory basename that contains a sub-repo (e.g., `libs`)

3. Fetch intervals for each matching project:
   ```bash
   python3 wakatime_fetch.py --start 2026-01-15 --end 2026-02-02 --project my-project
   python3 wakatime_fetch.py --start 2026-01-15 --end 2026-02-02 --project frontend
   python3 wakatime_fetch.py --start 2026-01-15 --end 2026-02-02 --project backend
   ```

4. Combine all intervals from all matching WakaTime projects into a single list for reconciliation.

**Why this matters:** In a project with 4 sub-repos, a single `--project` query captured only 9h of the actual 26.5h of WakaTime data. The other 17.5h was tracked under sub-directory project names.

**Folder move detection:** If `claude_messages.py`, `codex_messages.py`, or `cursor_messages.py` return 0 results, check the output for `alternate_paths`. If present, ask the user:
> "No Claude/Codex history found at `/current/path`, but found sessions for `project-name` at `/old/path`. Was this project moved? Should I include that history too?"

If confirmed, re-run with `--project-path /old/path` and merge timestamps from both paths.

See [references/folder-move-detection.md](references/folder-move-detection.md) for full detection logic and edge cases.

### 3. Reconcile hours

**Merged total = best estimate** (git ∪ Claude ∪ Codex ∪ Cursor ∪ WakaTime intervals, no double-counting):

```python
GAP_H = 1.5  # hours between events → new session

# 1. Collect intervals from git (start/end per session, converted to UTC epoch)
# 2. Collect intervals from Claude timestamps (detect sessions via gap threshold)
# 3. Collect intervals from Codex timestamps (same gap threshold)
# 4. Collect intervals from Cursor timestamps (same gap threshold)
# 5. Collect intervals from WakaTime "intervals" field (already [start, end] pairs in UTC epoch)
# 6. Combine all intervals into one list, sort by start
# 7. Merge overlapping/adjacent intervals:
#    for each interval, if next.start - cur.end <= GAP_H * 3600 → extend current
# 8. For each merged interval: est = max(end - start + 0.5h, 0.5h)
# 9. total = Σ est

# Data formats (all UTC epoch floats):
# - git_sessions.py: convert local times using timezone offset from git log
# - claude_messages.py "timestamps": point events → detect sessions via gap
# - codex_messages.py "timestamps": point events → detect sessions via gap
# - cursor_messages.py "timestamps": point events → detect sessions via gap
# - wakatime_fetch.py "intervals": already [start_epoch, end_epoch] pairs
#   (fetched from /durations API, per-file intervals pre-merged with 60s tolerance)
```

Why merge matters: AI agent prompts (Claude/Codex/Cursor) often appear minutes before/after git commits in the same work session. WakaTime captures IDE keystrokes that may fall between commits. A user might research with Claude, use Cursor's AI, write code (WakaTime), then commit (git) — all one session. Union of all five sources captures the true session boundaries without double-counting.

- The merged total replaces "git-only" as the primary estimate
- WakaTime hours shown for reference (active keystrokes only, always lower)

See [references/reconciliation.md](references/reconciliation.md) for full pseudocode, the session detection function, and the hour estimate formula.

### 4. Generate HTML dashboard

Write a single-file HTML with inline Chart.js (CDN). Dark theme (`#0a0a0a` bg, `#1a1a1a` cards).

Required sections:
1. **Stat cards** — Merged total (git∪claude∪codex∪cursor∪waka), Git estimate, WakaTime, Sessions, Commits, Claude prompts, Codex prompts, Cursor prompts
2. **Daily activity chart** — Overlapping bars (git + WakaTime + merged) + AI prompts line on secondary axis
3. **Gantt timeline** — UTC horizontal bars; git, Claude, Codex, and Cursor as separate colored datasets on same chart (separate swimlane rows when they overlap on same day)
4. **Data table** — Session | Time (UTC) | Active | Est. | WakaTime | Claude | Codex | Cursor | Commits

Chart.js essentials:
```javascript
Chart.defaults.color = '#888';
Chart.defaults.borderColor = '#2a2a2a';
// Overlapping bars: same barPercentage/categoryPercentage on both datasets, different opacity
// Mixed chart: type:'bar' on container, each dataset has its own type + yAxisID
// Gantt floating bars: data: [[startH, endH]], indexAxis: 'y'
// Claude as line on secondary axis:
{
  type: 'line',
  yAxisID: 'yClaude',
  // right-side axis, max ~100, different color
}
// All charts: responsive: true, maintainAspectRatio: false
```

Save as `<project-dir>/work-hours-analysis.html`.

### 5. Generate Markdown report

```markdown
# [Project] - Work Hours Analysis
## Summary
**Estimated Total Working Hours: Xh** (based on commit timing analysis)

| Date | Sessions | Time Range | Git Est. | WakaTime | Commits | Project |
...

## Timeline
- Start: [date], End: [date], Duration: N days

## Per-Project Breakdown
[sub-project sections with commit/session counts]

## Charts
### Daily Activity (ASCII)
Jan 15  ██░░░░░░░░░░░░░░░░░░  0.5h
...
### Project Distribution
project-a  ████████████████████  45%  (~18h)
...

## Methodology
- Session Detection: commits within 1.5h gap = same session
- Hour Estimate: Σ(session_duration + 0.5h buffer), min 0.5h/session
- Why Git > WakaTime: WakaTime only tracks active IDE typing; git includes thinking/research/AI prompting
```

ASCII bar: `blocks = round(hours / max_hours * 20)`, `█` filled, `░` empty, 20 cols wide.

Save as `<project-dir>/total_hours.md`.

---

## Validation Checklist

### Before running

- [ ] **WakaTime API key** — `~/.wakatime.cfg` exists and contains `api_key = waka_...` under `[settings]`. Run `cat ~/.wakatime.cfg` to verify. If missing, the WakaTime script will fail silently or with an auth error.
- [ ] **Git repo accessible** — the project directory is a git repo with commits (`git log --oneline -5 /path/to/repo` returns results). If not, `git_sessions.py` will return 0 sessions.
- [ ] **Claude history exists** — `~/.claude/history.jsonl` is present and non-empty, OR `~/.claude/projects/` contains session files for the project. If both are missing, Claude hours will be 0.
- [ ] **Cursor data accessible** — the Cursor state database exists at the platform-specific path (macOS: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`, Windows: `%APPDATA%\Cursor\User\globalStorage\state.vscdb`, Linux: `~/.config/Cursor/User/globalStorage/state.vscdb`). If missing, Cursor hours will be 0. The script auto-detects the platform and reads SQLite databases in read-only mode.
- [ ] **Date range is valid** — `--since` is before `--until`; the range covers dates when work actually happened.

### After generation

- [ ] **HTML loads without errors** — open `work-hours-analysis.html` in a browser; all charts render; no JS console errors.
- [ ] **Total hours match** — the "Merged total" stat card in HTML equals the "Estimated Total Working Hours" in `total_hours.md` (allow ±0.01h for rounding).
- [ ] **Date range matches input** — the first and last dates in the data table and the Timeline section match the requested `--since`/`--until` values.
- [ ] **Session count non-zero** — at least one source contributed sessions. If all sources return 0, something is wrong (wrong path, wrong project name, date range outside project history).

---

## Examples

### Example 1: Single repo, standard report

**Trigger phrase:** "How many hours did I spend on the api-server project this month? Generate the full report."

**Actions:**

1. Determine scope: project at `/Users/alice/code/api-server`, date range inferred as 2026-02-01 → 2026-02-23 (current month to today).

2. Extract data:
   ```bash
   python3 git_sessions.py /Users/alice/code/api-server --since 2026-02-01 --until 2026-02-23
   python3 wakatime_fetch.py --start 2026-02-01 --end 2026-02-23 --project api-server
   python3 claude_messages.py --project-path /Users/alice/code/api-server
   python3 codex_messages.py --project-path /Users/alice/code/api-server
   python3 cursor_messages.py --project-path /Users/alice/code/api-server
   ```

3. Reconcile: `git_sessions.py` returns 14 sessions (22.5h), WakaTime returns 11.2h, Claude returns 47 prompts across 9 days, Codex returns 0, Cursor returns 12 prompts across 3 days. Merged total after union + gap merging: **27.1h**.

4. Generate `work-hours-analysis.html` and `total_hours.md` in `/Users/alice/code/api-server/`.

**Result:** "You spent approximately **27.1 hours** on api-server in February 2026 (14 git sessions, 47 Claude prompts, 12 Cursor prompts, WakaTime reference: 11.2h active typing). Report saved to `/Users/alice/code/api-server/work-hours-analysis.html`."

---

### Example 2: Multi-repo project with folder move

**Trigger phrase:** "Calculate the total dev time for the marketplace project — it has a frontend and backend repo. Also I think I renamed the folder at some point."

**Actions:**

1. Determine scope: two repos at `/Users/bob/marketplace-backend` and `/Users/bob/marketplace-frontend`, user specifies date range 2025-11-01 → 2026-01-31.

2. Extract data:
   ```bash
   python3 git_sessions.py /Users/bob/marketplace-backend --since 2025-11-01 --until 2026-01-31
   python3 git_sessions.py /Users/bob/marketplace-frontend --since 2025-11-01 --until 2026-01-31
   python3 wakatime_fetch.py --start 2025-11-01 --end 2026-01-31 --project marketplace
   python3 claude_messages.py --project-path /Users/bob/marketplace-backend
   python3 codex_messages.py --project-path /Users/bob/marketplace-backend
   python3 cursor_messages.py --project-path /Users/bob/marketplace-backend
   ```

3. `claude_messages.py` returns 0 results with `alternate_paths: ["/Users/bob/old-market/backend"]`.

4. Ask user: "No Claude history found at `/Users/bob/marketplace-backend`, but found sessions for `backend` at `/Users/bob/old-market/backend`. Was this the previous location? Should I include that history?"

5. User confirms. Re-run: `python3 claude_messages.py --project-path /Users/bob/old-market/backend`. Merge timestamps from both runs.

6. Merge git sessions from both repos (backend + frontend), sort, re-merge within 1.5h gap. Reconcile with all sources.

**Result:** "Total estimated time: **84.7h** across 3 months (backend + frontend combined, including Claude history from the old path `/Users/bob/old-market/backend`)."

---

## Troubleshooting

### WakaTime API key missing or invalid

**Symptom:** `wakatime_fetch.py` exits with an auth error, HTTP 401, or `KeyError: 'api_key'`.

**Fix:**
1. Check if the config exists: `cat ~/.wakatime.cfg`
2. If missing, create it:
   ```ini
   [settings]
   api_key = waka_xxxx...
   ```
3. Get your key from [wakatime.com/settings/api-key](https://wakatime.com/settings/api-key).
4. If the key exists but returns 401, it may be expired or revoked — generate a new one.

**Also check:** The `--project` flag matches the project name exactly as WakaTime recorded it (case-sensitive). You can verify project names in the WakaTime dashboard under Projects.

---

### Git returns 0 sessions

**Symptom:** `git_sessions.py` returns `"sessions": []` or `"total_hours": 0`.

**Possible causes and fixes:**

| Cause | Fix |
|---|---|
| Date range is outside project history | Check `git log --oneline` for actual date range; adjust `--since`/`--until` |
| Path is not a git repo | Verify with `git -C /path/to/repo log --oneline -1` |
| No commits in range by the current user | Pass `--author` flag if filtering by author, or remove it |
| Shallow clone | Run `git fetch --unshallow` to restore full history |

---

### Claude, Codex, or Cursor returns 0 sessions (no alternate_paths)

**Symptom:** Both `timestamps: []` and `alternate_paths: []`.

**Possible causes and fixes:**

| Cause | Fix |
|---|---|
| The tool was not used on this project | Expected — note it in the report |
| Wrong `--project-path` (typo, symlink, trailing slash) | Use `realpath /path/to/repo` to get the canonical absolute path; pass that |
| History files don't exist | Check `~/.claude/history.jsonl` and `~/.claude/projects/` exist; check `~/.codex/sessions/` exists; check Cursor's `state.vscdb` exists at the platform-specific path (see Validation Checklist) |
| Project path uses a symlink that resolves differently | Use the resolved path: `python3 -c "import os; print(os.path.realpath('/your/path'))"` |
| Cursor database locked by running Cursor instance | The script opens databases in read-only mode — this should not happen, but if it does, try closing Cursor temporarily |

---

### `alternate_paths` found but user says the path is wrong

**Symptom:** The script reports alternate paths but the user says none of them are the old project location.

**Fix:** Fall back to `--filter <project-name>` which does a substring match on directory names rather than an exact path match. Be aware this may pick up unrelated projects with similar names — review the session list with the user before merging.

```bash
python3 claude_messages.py --filter marketplace
```

---

### HTML chart renders blank or shows NaN

**Symptom:** The HTML file opens but charts are empty or show "NaN" values.

**Possible causes:**
- Reconciliation produced `null` or `None` values that were serialized into the JS data arrays.
- Timestamps were not converted to UTC before writing to HTML (local epoch vs UTC epoch mismatch).
- Chart.js CDN failed to load (offline environment).

**Fix:**
1. Open browser DevTools console — the specific JS error pinpoints the issue.
2. Verify all epoch timestamps are UTC floats, not strings.
3. For offline environments, download Chart.js and embed it inline: `<script>/* chart.js source */</script>`.

---

### Total hours mismatch between HTML and Markdown

**Symptom:** The HTML stat card shows a different merged total than `total_hours.md`.

**Cause:** The reconciliation was run twice independently and produced slightly different results (e.g., due to floating-point rounding, or one file used stale data).

**Fix:** Run reconciliation once, store the result in a variable, and write the same computed value to both output files. Do not recompute independently for each output.

---

## Notes

**WakaTime auth and config:** The script reads `~/.wakatime.cfg` automatically. Always pass `--project` for per-project data. WakaTime tracks active keystrokes only — always lower than git estimate. Heavy Claude Code usage creates a large gap between WakaTime and actual effort. See [references/data-sources.md](references/data-sources.md) for full auth setup, config format, and limitations.

**Codex CLI data source:** `codex_messages.py` reads `~/.codex/sessions/YYYY/MM/DD/rollup-*.jsonl`. Each file has `session_meta` (first entry with `payload.cwd` + `payload.id`), `event_msg` entries with `payload.type == "user_message"` for actual prompts, and `turn_context` entries for boundaries. Output includes `timestamps` (UTC epoch floats) and `alternate_paths` for folder-move detection. See [references/data-sources.md](references/data-sources.md) for full file structure.

**Claude Code data sources:** `claude_messages.py` uses two sources: `~/.claude/history.jsonl` (primary; `project` field = abs path, `timestamp` in ms) and `~/.claude/projects/<encoded>/*.jsonl` (session files; `cwd` field, `type=="user"` entries, ISO timestamps). Encoded dir name format: `/Users/foo/bar` → `-Users-foo-bar`. Always prefer `--project-path` over `--filter`. See [references/data-sources.md](references/data-sources.md) for full field reference.

**Cursor IDE data sources:** `cursor_messages.py` reads from Cursor's SQLite databases (`.vscdb` files). Primary source is the platform-specific `state.vscdb` (macOS: `~/Library/Application Support/Cursor/User/globalStorage/`, Windows: `%APPDATA%\Cursor\User\globalStorage\`, Linux: `~/.config/Cursor/User/globalStorage/`) — the `cursorDiskKV` table contains `composerData:{sessionId}` entries (with `workspaceUri` for project matching) and `bubbleId:{sessionId}:{messageId}` entries (with per-message timestamps). Fallback source is workspace-level `state.vscdb` files under `workspaceStorage/*/`, with `workspace.json` mapping each workspace to its project folder. Databases are opened read-only. The script auto-detects the platform. Output format matches Claude/Codex scripts: `timestamps` array + `alternate_paths` for folder-move detection. See [references/data-sources.md](references/data-sources.md) for full field reference.

**Reconciliation algorithm:** Gap threshold is 1.5h. All sources converted to UTC epoch float intervals. Intervals merged if gap ≤ threshold. Per-interval estimate: `max(duration + 0.5h, 0.5h)`. Merged total = Σ estimates. See [references/reconciliation.md](references/reconciliation.md) for full pseudocode and the session detection helper function.

**Folder move detection:** `claude_messages.py`, `codex_messages.py`, and `cursor_messages.py` all scan known history for matching project names when 0 results are found at the provided path. Returns `alternate_paths` list. If non-empty, ask user to confirm, re-run with old path, merge timestamps. See [references/folder-move-detection.md](references/folder-move-detection.md) for detection logic and edge cases.

**Multi-repo projects:** By default, scan for `.git` subdirectories to auto-discover all sub-repos. Run `git_sessions.py`, `claude_messages.py`, `codex_messages.py`, and `cursor_messages.py` on each sub-repo plus the root directory. Use WakaTime multi-project discovery to find all matching WakaTime project names. Merge all session arrays, re-sort by date, recompute daily totals and grand total.
