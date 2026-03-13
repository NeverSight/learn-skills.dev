---
name: transcript-viewer
version: 1.2.0
description: |
  Convert and browse session transcripts as HTML or Markdown.
  Supports Claude Code JSONL logs (auto-saved to ~/.claude/projects/) and
  GitHub Copilot CLI JSONL logs (auto-saved to ~/.copilot/session-state/*/events.jsonl).
  Auto-detects log source based on available directories and file format.
  Supports viewing the current session, a specific session by ID, agent background task
  output files, or all project sessions with optional date-range filtering.
auto_activate_keywords:
  - "view transcript"
  - "show transcript"
  - "browse transcript"
  - "read transcript"
  - "view session log"
  - "show session log"
  - "transcript viewer"
  - "convert jsonl"
  - "view jsonl"
  - "browse sessions"
  - "session history"
  - "agent output"
  - "background task output"
  - "copilot transcript"
  - "copilot session"
  - "copilot log"
  - "view copilot"
  - "show copilot session"
  - "copilot history"
  - "copilot export"
  - "copilot events"
priority_score: 35.0
evaluation_criteria:
  frequency: MEDIUM
  impact: HIGH
  complexity: LOW
  reusability: HIGH
  philosophy_alignment: HIGH
  uniqueness: HIGH
dependencies:
  tools:
    - Bash
    - Glob
    - Read
  external:
    - claude-code-log (npm package, optional — falls back to npx)
maturity: production
---

# Transcript Viewer Skill

## Purpose

This skill converts and browses session transcripts from two supported tools:

- **Claude Code** — JSONL logs auto-saved to `~/.claude/projects/`
- **GitHub Copilot CLI** — JSONL logs auto-saved to `~/.copilot/session-state/*/events.jsonl`

It provides four browsing modes:

1. **Current session** — View the active session's transcript
2. **Specific session** — View a session by its ID
3. **Agent output** — View background task output files produced by subagents
4. **All sessions** — Browse all project sessions, with optional date-range filtering

## Tool Context Auto-Detection

Before browsing, detect which tool is active to set default log paths.
Prefer directory-based detection (more reliable than env vars); fall back to env vars
from `src/amplihack/hooks/launcher_detector.py` when directories don't exist:

```bash
# Primary: directory-based detection (most reliable)
if [[ -d "$HOME/.copilot/session-state" ]]; then
  # Check if there are any sessions present
  COPILOT_SESSIONS=$(ls -d "$HOME/.copilot/session-state/"*/ 2>/dev/null | wc -l)
  CLAUDE_SESSIONS=$(ls "$HOME/.claude/projects/"*/*.jsonl 2>/dev/null | wc -l)
  if [[ "$COPILOT_SESSIONS" -gt 0 && "$CLAUDE_SESSIONS" -eq 0 ]]; then
    TOOL_CONTEXT="copilot"
    DEFAULT_LOG_DIR="$HOME/.copilot/session-state"
  elif [[ "$CLAUDE_SESSIONS" -gt 0 ]]; then
    TOOL_CONTEXT="claude-code"
    DEFAULT_LOG_DIR="$HOME/.claude/projects"
  else
    # Both dirs exist but empty — use env vars to decide
    TOOL_CONTEXT="claude-code"
    DEFAULT_LOG_DIR="$HOME/.claude/projects"
  fi
elif [[ -d "$HOME/.claude/projects" ]]; then
  TOOL_CONTEXT="claude-code"
  DEFAULT_LOG_DIR="$HOME/.claude/projects"
# Fallback: env var detection (same vars as launcher_detector.py)
elif [[ -n "${CLAUDE_CODE_SESSION:-}${CLAUDE_SESSION_ID:-}${ANTHROPIC_API_KEY:-}" ]]; then
  TOOL_CONTEXT="claude-code"
  DEFAULT_LOG_DIR="$HOME/.claude/projects"
elif [[ -n "${GITHUB_COPILOT_TOKEN:-}${COPILOT_SESSION:-}" ]]; then
  # Note: GITHUB_TOKEN is intentionally excluded — it's too generic and
  # appears in non-Copilot CI contexts, causing false positives.
  TOOL_CONTEXT="copilot"
  DEFAULT_LOG_DIR="$HOME/.copilot/session-state"
else
  # Default to claude-code — safe fallback (most users)
  TOOL_CONTEXT="claude-code"
  DEFAULT_LOG_DIR="$HOME/.claude/projects"
fi
```

When both `~/.copilot/session-state/` and `~/.claude/projects/` exist with sessions,
offer the user a choice: "Found sessions for both Claude Code and GitHub Copilot CLI.
Which would you like to browse? [1] Claude Code  [2] GitHub Copilot CLI"

The user can always override with an explicit path.

## Log Format Auto-Detection

When given a file path, detect its format before processing:

```bash
detect_log_format() {
  local file="$1"
  if [[ "$file" == *.jsonl ]]; then
    echo "jsonl"
  elif [[ "$file" == *.md ]]; then
    # Check for Copilot /share export signature — specific header only
    # Note: do NOT match on "/share" alone (too generic — appears in docs, READMEs)
    if grep -q "Copilot Session Export\|copilot-session" "$file" 2>/dev/null; then
      echo "copilot-markdown"
    else
      echo "markdown"
    fi
  elif [[ "$file" == *.log ]]; then
    # .log files may be plain text or agent JSONL; check content
    local first_char
    first_char=$(head -c 1 "$file" 2>/dev/null)
    if [[ "$first_char" == "{" ]]; then
      echo "jsonl"
    else
      echo "plain-log"
    fi
  else
    # Inspect first byte for other extensions
    local first_char
    first_char=$(head -c 1 "$file" 2>/dev/null)
    if [[ "$first_char" == "{" ]]; then
      echo "jsonl"
    else
      echo "unknown"
    fi
  fi
}
```

| Format | Handler |
|--------|---------|
| `jsonl` | Pass to `claude-code-log` |
| `copilot-markdown` | Display inline (already readable Markdown) |
| `markdown` | Display inline |
| `unknown` | Warn and display raw |

## Tool Detection

Before running any command, check whether `claude-code-log` is available:

```bash
# Step 1: direct install check
which claude-code-log 2>/dev/null

# Step 2: npx fallback
npx --yes claude-code-log --version 2>/dev/null
```

Set `CCL` to the resolved command:

```bash
if which claude-code-log &>/dev/null; then
  CCL="claude-code-log"
elif npx --yes claude-code-log --version &>/dev/null 2>&1; then
  CCL="npx claude-code-log"
else
  CCL=""
fi
```

### Missing Tool — Graceful Error

If `CCL` is empty, display this message and stop:

```
claude-code-log is not installed.

To install it globally:
  npm install -g claude-code-log

Or run without installing (requires npx):
  npx claude-code-log --help

After installing, retry your request.
```

Do not attempt to install it automatically.

## Modes

### Mode 1: Current Session

**Trigger phrases**: "view current transcript", "show my current session", "current log"

**What to do**:

For **Claude Code** (`TOOL_CONTEXT="claude-code"`):

1. Find the most recently modified JSONL file under `~/.claude/projects/`:
   ```bash
   ls -t ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1
   ```
2. Run:
   ```bash
   $CCL <path-to-jsonl> --format markdown
   ```
3. Display the Markdown output inline.

For **GitHub Copilot CLI** (`TOOL_CONTEXT="copilot"`):

1. Find the most recently modified session directory under `~/.copilot/session-state/`:
   ```bash
   ls -dt ~/.copilot/session-state/*/ 2>/dev/null | head -1
   ```
2. Read its `events.jsonl`:
   ```bash
   LATEST_SESSION=$(ls -dt ~/.copilot/session-state/*/ 2>/dev/null | head -1)
   $CCL "${LATEST_SESSION}events.jsonl" --format markdown
   ```
3. Display the Markdown output inline.

**Example output**:

```markdown
# Session: 2025-11-23 19:32
**Model**: claude-sonnet-4-6
**Messages**: 42

---

**User**: Fix the authentication bug in login.py
**Assistant**: I'll examine the file...
...
```

### Mode 2: Specific Session by ID

**Trigger phrases**: "view session <ID>", "show transcript <ID>", "open log <ID>"

**What to do**:

For **Claude Code** (`TOOL_CONTEXT="claude-code"`):

1. Search for the JSONL file matching the session ID:
   ```bash
   find ~/.claude/projects -name "*.jsonl" | xargs grep -l "<SESSION_ID>" 2>/dev/null | head -1
   ```
   Or, if the ID looks like a filename fragment, use:
   ```bash
   ls ~/.claude/projects/*/ | grep "<SESSION_ID>"
   ```
2. Run:
   ```bash
   $CCL <path-to-jsonl> --format markdown
   ```
3. Display the output. If no file matches, report:
   ```
   No session found with ID: <SESSION_ID>
   Available sessions: run "view all sessions" to list them.
   ```

For **GitHub Copilot CLI** (`TOOL_CONTEXT="copilot"`):

1. The session ID is the directory name under `~/.copilot/session-state/`. Check directly:
   ```bash
   SESSION_DIR="$HOME/.copilot/session-state/<SESSION_ID>"
   if [[ -d "$SESSION_DIR" ]]; then
     EVENTS_FILE="$SESSION_DIR/events.jsonl"
   fi
   ```
   If the full ID is not known, search for a partial match:
   ```bash
   ls -d ~/.copilot/session-state/*/ 2>/dev/null | grep "<SESSION_ID>"
   ```
2. Run:
   ```bash
   $CCL "$EVENTS_FILE" --format markdown
   ```
3. Display the output. If no directory matches, report:
   ```
   No Copilot session found with ID: <SESSION_ID>
   Available sessions: run "browse all sessions" to list them.
   ```

### Mode 3: Agent Background Task Output

**Trigger phrases**: "view agent output", "show background task output", "agent log"

**What to do**:

1. Find `.log` or `.jsonl` files created by background agent tasks. These are
   typically written to the current working directory or a temp path with a name
   matching `.agent-step-*.log` or similar:
   ```bash
   ls -t .agent-step-*.log 2>/dev/null
   ls -t /tmp/*.agent*.log 2>/dev/null
   ```
2. For each file found, run `detect_log_format <file>` to classify it:
   - `jsonl` → run `$CCL <file> --format markdown`
   - `plain-log` → display directly with `cat`
3. This ensures JSONL-formatted `.log` files (rare but possible) are rendered properly.
4. If no agent output files are found:
   ```
   No agent background task output files found in the current directory.
   Background agents write their output to files named .agent-step-<ID>.log.
   ```

### Mode 4: All Sessions (Browse)

**Trigger phrases**: "browse all sessions", "list transcripts", "view all sessions",
"show session history"

**What to do**:

For **Claude Code** (`TOOL_CONTEXT="claude-code"`):

1. List all JSONL files under `~/.claude/projects/`:
   ```bash
   find ~/.claude/projects -name "*.jsonl" -printf "%T@ %p\n" 2>/dev/null \
     | sort -rn | awk '{print $2}'
   ```
2. For each file, extract the session date and first user message:
   ```bash
   $CCL <file> --format markdown --summary
   # If --summary flag is not supported, just show filename and date
   head -1 <file> | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('timestamp',''))"
   ```
3. Print a summary table:
   ```
   Available Sessions (Claude Code)
   =================================
   #   Date                  Session ID / File
   1   2025-11-23 19:32:36   ~/.claude/projects/foo/abc123.jsonl
   2   2025-11-22 14:10:05   ~/.claude/projects/foo/def456.jsonl
   ...
   ```
4. Offer to open a specific session: "Enter a number to view that session."

For **GitHub Copilot CLI** (`TOOL_CONTEXT="copilot"`):

1. List all session directories under `~/.copilot/session-state/` sorted by modification time:
   ```bash
   ls -dt ~/.copilot/session-state/*/ 2>/dev/null
   ```
2. For each session directory, read its `events.jsonl` to extract the timestamp:
   ```bash
   for session_dir in $(ls -dt ~/.copilot/session-state/*/); do
     session_id=$(basename "$session_dir")
     events_file="$session_dir/events.jsonl"
     if [[ -f "$events_file" ]]; then
       timestamp=$(head -1 "$events_file" | python3 -c \
         "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('timestamp',''))" 2>/dev/null)
       echo "$timestamp  $session_id"
     fi
   done
   ```
3. Print a summary table:
   ```
   Available Sessions (GitHub Copilot CLI)
   ========================================
   #   Date                  Session ID
   1   2025-11-23 19:32:36   abc1234567890abcdef1234567890abcd
   2   2025-11-22 14:10:05   def4567890abcdef1234567890abcdef
   ...
   ```
4. Offer to open a specific session: "Enter a number to view that session."

#### Date-Range Filtering

When the user specifies a date range (e.g., "last 7 days", "between 2025-11-01 and 2025-11-30"):

```bash
# Filter by modification time (last N days)
find ~/.claude/projects -name "*.jsonl" -mtime -7

# Filter by date range using find -newer
find ~/.claude/projects -name "*.jsonl" \
  -newer /tmp/start_date_ref \
  ! -newer /tmp/end_date_ref
```

Create the reference files with `touch -d`:
```bash
touch -d "2025-11-01" /tmp/start_date_ref
touch -d "2025-11-30" /tmp/end_date_ref
```

## Output Formats

### Markdown (default)

Pass `--format markdown` to `claude-code-log`. The output is printed inline in the
conversation. Best for quick reading in the terminal or Claude Code.

### HTML

Pass `--format html` to `claude-code-log`. Write the output to a file and open it:

```bash
$CCL <file> --format html > /tmp/transcript-view.html
open /tmp/transcript-view.html 2>/dev/null \
  || xdg-open /tmp/transcript-view.html 2>/dev/null \
  || echo "HTML saved to /tmp/transcript-view.html — open it in your browser."
```

The user can request HTML explicitly: "view transcript as HTML" or "export to HTML".

## GitHub Copilot CLI Support

### Automatic Log Persistence

GitHub Copilot CLI **automatically saves** session data to disk at:

```
~/.copilot/session-state/{session-id}/
```

Each session directory contains:
- `events.jsonl` — JSONL session history (similar format to Claude Code logs)
- `workspace.yaml` — session metadata (working directory, session ID, etc.)
- `plan.md` — implementation plan for the session
- `checkpoints/` — compaction history (older event snapshots)

Legacy sessions may also exist at `~/.copilot/history-session-state/`.

### JSONL Format

Copilot `events.jsonl` contains one JSON object per line, similar to Claude Code format:

```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"Fix the bug"}]},"timestamp":"2025-11-23T19:32:36Z","sessionId":"abc1234567890"}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"I'll examine the file..."}]},"timestamp":"2025-11-23T19:32:40Z","sessionId":"abc1234567890"}
```

`claude-code-log` handles parsing these files since the format is compatible.

### Viewing a Copilot Session

When the user wants to view a Copilot session (by directory detection or explicit path):

1. Locate the `events.jsonl` for the session:
   ```bash
   # Current session (most recent)
   LATEST_SESSION=$(ls -dt ~/.copilot/session-state/*/ 2>/dev/null | head -1)
   EVENTS_FILE="${LATEST_SESSION}events.jsonl"

   # Specific session by ID
   EVENTS_FILE="$HOME/.copilot/session-state/<SESSION_ID>/events.jsonl"
   ```
2. Run:
   ```bash
   $CCL "$EVENTS_FILE" --format markdown
   ```
3. Display the output inline.

### Detecting Available Sessions

To check if Copilot sessions exist:

```bash
if [[ -d "$HOME/.copilot/session-state" ]]; then
  SESSION_COUNT=$(ls -d "$HOME/.copilot/session-state/"*/ 2>/dev/null | wc -l)
  if [[ "$SESSION_COUNT" -gt 0 ]]; then
    echo "Found $SESSION_COUNT Copilot session(s)"
  fi
fi
```

## Full Workflow

When the user invokes this skill, follow this decision tree:

```
0. Detect tool context (directory-based first, then env var fallback):
   - ~/.copilot/session-state/ exists with sessions → copilot
   - ~/.claude/projects/ exists with sessions       → claude-code
   - Both exist with sessions → offer user a choice
   - Directory detection fails, use env vars:
     - CLAUDE_CODE_SESSION / CLAUDE_SESSION_ID / ANTHROPIC_API_KEY set → claude-code
     - GITHUB_COPILOT_TOKEN / COPILOT_SESSION set → copilot
   - Neither → default to claude-code (safe fallback)

1. Detect CCL (which claude-code-log / npx fallback)
   → If missing: show install instructions and STOP
   → Required for ALL modes (both Claude Code and Copilot use JSONL format)

2. If user provides an explicit file path:
   a. Detect its format (detect_log_format function above)
   b. jsonl or events.jsonl → pass to $CCL
   c. unknown → warn and display raw

3. Determine mode from user message:
   - mentions "current" or no session specified → Mode 1 (Current Session)
   - mentions a session ID or hash             → Mode 2 (Specific Session)
   - mentions "agent" or "background"          → Mode 3 (Agent Output)
   - mentions "all", "browse", "list"          → Mode 4 (All Sessions)

4. Determine output format:
   - "as HTML" or "export HTML" → html
   - default                    → markdown

5. Execute the appropriate mode (using TOOL_CONTEXT to choose correct paths) and display results.
```

## Error Handling

| Situation | Response |
|-----------|----------|
| `claude-code-log` not installed | Show install instructions, stop |
| JSONL file not found | "No session file found at <path>" |
| Session ID not found | "No session with ID <ID>. Run 'browse all sessions' to list available ones." |
| No agent output files | "No agent background task output found in current directory." |
| Empty JSONL file | "Session file is empty — no messages to display." |
| Date range produces no results | "No sessions found between <start> and <end>." |
| `claude-code-log` returns non-zero exit | Display stderr and suggest `--help` |
| `~/.copilot/session-state/` exists but empty | "No Copilot sessions found. Start a session with GitHub Copilot CLI to create logs." |
| Copilot session dir exists but no events.jsonl | "Session directory found but events.jsonl is missing at <path>" |
| Unknown file format | Warn user and display raw content |

## Implementation Notes

### Detecting Session IDs

Claude Code session IDs are UUID-like strings. If the user writes something like
"view session abc123" or "show log def456", treat the last word as the session ID
and search for matching JSONL filenames.

### JSONL Structure (Claude Code)

Claude Code session JSONL files contain one JSON object per line:

```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"..."}]},"timestamp":"...","sessionId":"..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"..."}]},"timestamp":"..."}
```

`claude-code-log` handles parsing; this skill does not re-implement it.

### Copilot JSONL Structure (GitHub Copilot CLI)

Copilot CLI `events.jsonl` files contain one JSON object per line, stored at
`~/.copilot/session-state/{session-id}/events.jsonl`:

```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"..."}]},"timestamp":"...","sessionId":"..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"..."}]},"timestamp":"...","sessionId":"..."}
```

The format is compatible with `claude-code-log`. Additional per-session files:
- `workspace.yaml` — session metadata
- `plan.md` — implementation plan
- `checkpoints/` — compaction history (older snapshots)

Legacy sessions may be stored at `~/.copilot/history-session-state/` with the same structure.

### Philosophy Alignment

- **Thin wrapper**: Delegates to `claude-code-log` for all JSONL (both Claude Code and Copilot)
- **Graceful degradation**: Clear error messages when tool is missing or no sessions found
- **Single responsibility**: Only views/converts transcripts, never modifies them
- **No hidden state**: All file paths are shown to the user

## Limitations

- Requires `claude-code-log` (npm) or `npx` to convert JSONL (both Claude Code and Copilot) to HTML/Markdown
- Cannot view transcripts from remote machines
- Date filtering relies on filesystem modification times, not session timestamps
- `--summary` flag availability depends on `claude-code-log` version
- Legacy Copilot sessions in `~/.copilot/history-session-state/` are not auto-discovered (must use explicit path)
- When both Claude Code and Copilot sessions exist, the skill prompts the user to choose rather than merging them

## Quick Reference

| User says | Tool | Mode | Command |
|-----------|------|------|---------|
| "view current transcript" | Claude Code | Current session | `$CCL <latest.jsonl> --format markdown` |
| "show session abc123" | Claude Code | Specific session | `$CCL ~/.claude/projects/**/*abc123*.jsonl --format markdown` |
| "view agent output" | Claude Code | Agent output | `cat .agent-step-*.log` or `$CCL *.jsonl` |
| "browse all sessions" | Claude Code | All sessions | list + summarize all `~/.claude/projects/**/*.jsonl` |
| "view transcript as HTML" | Claude Code | Any + HTML | `$CCL <file> --format html > /tmp/view.html` |
| "last 7 days" (with browse) | Claude Code | Date filter | `find ... -mtime -7` |
| "view current copilot session" | Copilot | Current session | `$CCL ~/.copilot/session-state/<latest>/events.jsonl --format markdown` |
| "show copilot session abc123" | Copilot | Specific session | `$CCL ~/.copilot/session-state/abc123/events.jsonl --format markdown` |
| "browse copilot sessions" | Copilot | All sessions | list dirs in `~/.copilot/session-state/`, show session IDs |
| "view copilot session as HTML" | Copilot | Any + HTML | `$CCL <events.jsonl> --format html > /tmp/view.html` |
