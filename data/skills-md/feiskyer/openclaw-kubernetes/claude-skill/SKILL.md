---
name: claude-skill
description: 'Use when user asks to leverage claude or claude code to do something (e.g. implement a feature design or review codes, etc). Provides non-interactive automation mode for hands-off task execution without approval prompts.'
---

# Claude Code Agent Skill

Operate Claude Code as a **managed coding agent** — from worktree setup through PR merge.

## Prerequisites

```bash
claude --version  # Verify installed
# Install: npm install -g @anthropic-ai/claude-code
tmux -V             # tmux required for full workflow
```

## CLI Quick Reference

| Flag | Effect |
|------|--------|
| `-p "prompt"` | Non-interactive one-shot, exits when done |
| `--dangerously-skip-permissions` | Skip all permission prompts (safe in containers/VMs) |
| `--permission-mode acceptEdits` | Auto-accept file edits, still prompt for shell commands |
| `--permission-mode plan` | Read-only analysis, no modifications |
| `--model <model>` | Model selection (e.g. `claude-sonnet-4-6`) |
| `--allowedTools "Bash,Read,Write,Edit"` | Restrict available tools |
| `--disallowedTools "Bash,Write"` | Block specific tools |
| `--append-system-prompt "..."` | Add custom instructions to system prompt |
| `--output-format json` | Structured JSON output with cost/duration metadata |
| `--output-format stream-json` | Streaming JSON (each message as it arrives) |
| `--continue` / `-c` | Continue most recent conversation |
| `--resume <id>` / `-r <id>` | Resume specific session by ID |
| `--mcp-config <file>` | Load MCP server configuration |
| `--verbose` | Enable verbose debug logging |

---

## Execution Modes

### Quick Mode — Small Tasks

For trivial fixes, one-file changes, or analysis. Use `-p` (non-interactive).

**Output capture:** Always redirect output to a log file so it's readable regardless
of PTY availability. Use `--output-format stream-json` for structured, parseable
progress events (each message arrives as a separate JSON line).

```bash
LOG_FILE="/tmp/claude-quick-${TASK_ID:-$$}.log"

# Via OpenClaw exec — use background=true + pty=true, NO hard timeout
# pty=true ensures claude CLI flushes output properly (no buffering issues)
# (hard timeout kills the process; instead we poll and extend)
# Redirect both stdout and stderr to log file via tee so output is always captured.
# In -p mode (non-interactive), | tee is safe — no TTY detection issues.
exec(command="claude -p 'fix the typo in README.md' --dangerously-skip-permissions --output-format stream-json 2>&1 | tee -a $LOG_FILE",
     workdir="/path/to/project", background=true, pty=true)
```

**PTY fallback:** If `pty=true` is unavailable (some containers, CI runners), the
command still works because `-p` mode is non-interactive — it doesn't rely on
`isatty(stdout)`. The `2>&1 | tee` ensures both stdout and stderr are captured
to the log file regardless of PTY status. Without PTY, you lose color output
but all content is preserved.

#### Adaptive Timeout (Poll-and-Extend)

**Do NOT use `timeout=` for claude tasks.** Instead, use background execution
with periodic polling. This prevents premature kills on long-running tasks:

1. Launch with `background=true` (no `timeout`)
2. Poll every ~5 min with `process(action="poll", sessionId=<id>, timeout=300000)`
3. If process is still running → check log file for new output
4. If process exited → check exit code and log file, done
5. Safety net: if no new output for 12 hours, ask user before killing
6. Safety net: if output is repeating (loop detection), ask user

**Persistent polling state:** Store polling metadata in the task registry so a
restarted orchestrator agent can resume monitoring without losing state:

```
Registry fields for Quick Mode tasks:
  "lastOutputHash": "<sha256 of last 20 lines>",
  "lastCheckedAt": <unix timestamp>,
  "silentRounds": <int>,
  "repeatingRounds": <int>
```

```
Poll loop (agent behavior, not a script):

  poll_interval = 5 min (300000 ms)
  max_silent_rounds = 144  (= 12 hours with no new output → ask user)
  max_repeating_rounds = 12 (= 1 hour of identical output → likely stuck)

  # Restore state from registry if resuming after agent restart
  silent_rounds = registry[task_id].silentRounds ?? 0
  repeating_rounds = registry[task_id].repeatingRounds ?? 0
  last_output_hash = registry[task_id].lastOutputHash ?? ""

  repeat:
    result = process(action="poll", sessionId=<id>, timeout=300000)
    if result.completed:
      → check exit code, read $LOG_FILE, report result
      → break
    else:
      # Read latest output directly from the log file
      new_output = tail -20 "$LOG_FILE"
      new_hash = sha256(new_output)

      if new_hash != last_output_hash and new_output != "":
        if last_output_hash != "" and output_looks_similar(new_output, last_output):
          repeating_rounds += 1   # output changing but repetitive (loop)
          silent_rounds = 0
        else:
          silent_rounds = 0       # genuinely new output, keep going
          repeating_rounds = 0
        last_output_hash = new_hash
      else:
        silent_rounds += 1

      # Persist state to registry (survives agent restart)
      update_registry(task_id, {
        lastOutputHash: new_hash,
        lastCheckedAt: now(),
        silentRounds: silent_rounds,
        repeatingRounds: repeating_rounds
      })

      if silent_rounds >= max_silent_rounds:
        → notify user: "Claude has been silent for 12 hours, kill or keep waiting?"
        → wait for user decision
      if repeating_rounds >= max_repeating_rounds:
        → notify user: "Claude appears stuck in a loop (1h of repeated output), kill or keep waiting?"
        → wait for user decision
```

This way tasks that need 5 min or several hours both work without premature kills.

### Full Mode — Features, Bugfixes, Refactors

For non-trivial tasks, use the **full workflow** below. This gives you:
- **Isolated worktree** — no conflicts with other work
- **tmux session** — mid-task steering without killing the agent
- **Task tracking** — know what's running at all times
- **Quality gates** — Definition of Done checklist
- **Smart retries** — don't waste tokens on repeated failures

---

## Full Workflow: Task → Merged PR

### Step 1: Create Worktree

Isolate each task in its own worktree and branch:

```bash
TASK_ID="feat-custom-templates"
BRANCH="feat/$TASK_ID"
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE="/tmp/worktrees/$TASK_ID"

git worktree add -b "$BRANCH" "$WORKTREE" origin/main
cd "$WORKTREE"

# Install dependencies (adapt to your stack)
pnpm install   # or: npm install / go mod tidy / pip install -r requirements.txt
```

### Step 2: Launch Agent in tmux

Start Claude Code in **interactive mode** (no `-p`) so you can steer mid-task.
**Important:** Use `tmux pipe-pane` to log output — do NOT use `| tee` because it
turns stdout into a pipe, which breaks interactive mode (claude detects `!isatty(stdout)`
and may disable interactive features, breaking `send-keys` steering).

**Critical:** Set up `pipe-pane` BEFORE sending the command. Otherwise early output
(startup messages, fast crashes) is lost.

```bash
LOG_FILE="/tmp/worktrees/$TASK_ID/claude-output.log"
MAX_LOG_SIZE=$((100 * 1024 * 1024))  # 100 MB safety cap

# 1. Create session with an idle shell first
tmux new-session -d -s "$TASK_ID" -c "$WORKTREE"

# 2. Start pipe-pane BEFORE the command runs — captures ALL output from the start
#    Strip ANSI escape codes so log files are clean and grep-parseable
tmux pipe-pane -t "$TASK_ID" -o "sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' >> $LOG_FILE"

# 3. NOW send the command — all output is captured
tmux send-keys -t "$TASK_ID" "claude --dangerously-skip-permissions \
  'Your detailed prompt here.

When completely finished:
1. Commit all changes with descriptive messages
2. Push the branch: git push -u origin $BRANCH
3. Create PR: gh pr create --fill
4. Notify: openclaw system event --text \"Done: $TASK_ID\" --mode now'" Enter
```

**Log file management:** For very long-running tasks, the log file can grow large.
Monitor its size and rotate if needed:
```bash
LOG_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
if [ "$LOG_SIZE" -gt "$MAX_LOG_SIZE" ]; then
  mv "$LOG_FILE" "${LOG_FILE}.old"
  # pipe-pane will create a new file on next write
fi
```

**Why interactive mode (no `-p`)?**
- Allows mid-task steering via `tmux send-keys`
- Agent can be redirected without killing and restarting
- `--dangerously-skip-permissions` is safe in container/sandbox environments

**Note on stdout/stderr:** In tmux, both stdout and stderr from the process flow
through the PTY and are captured by `pipe-pane`. They are mixed together — you
cannot separate them after capture. For error diagnosis, grep for keywords like
`error`, `fail`, `panic` in the clean (ANSI-stripped) log file.

### Step 3: Register Task

Track all active tasks in a JSON registry. Use `flock` for atomic updates to
prevent race conditions when multiple agents run in parallel.

```bash
mkdir -p "$REPO_ROOT/.clawd"
TASKS_FILE="$REPO_ROOT/.clawd/active-tasks.json"

# Initialize if not exists
[ -f "$TASKS_FILE" ] || echo '{"tasks":[]}' > "$TASKS_FILE"

# Get the PID of the claude process inside tmux for reliable status checks
PANE_PID=$(tmux display-message -t "$TASK_ID" -p '#{pane_pid}')

# Register — use flock to prevent concurrent write races
(
  flock -x 200
  jq --arg id "$TASK_ID" --arg branch "$BRANCH" --arg wt "$WORKTREE" \
    --arg pane_pid "$PANE_PID" \
    '.tasks += [{
      "id": $id,
      "agent": "claude",
      "branch": $branch,
      "worktree": $wt,
      "tmuxSession": $id,
      "panePid": ($pane_pid | tonumber),
      "status": "running",
      "startedAt": (now|floor),
      "pr": null,
      "retries": 0,
      "checks": {},
      "lastOutputHash": "",
      "lastCheckedAt": (now|floor),
      "silentRounds": 0,
      "repeatingRounds": 0
    }]' "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
) 200>"$TASKS_FILE.lock"
```

### Step 4: Monitor & Steer

```bash
# --- Process status check (reliable — checks actual process, not just tmux session) ---

# Method 1: Check if the claude process inside the pane is alive
PANE_PID=$(tmux display-message -t "$TASK_ID" -p '#{pane_pid}' 2>/dev/null)
if [ -z "$PANE_PID" ]; then
  echo "tmux session gone"
elif pgrep -P "$PANE_PID" > /dev/null 2>&1; then
  echo "running"
else
  echo "process exited (tmux session still open)"
  # Get exit code from the shell inside tmux
  tmux send-keys -t "$TASK_ID" 'echo "EXIT_CODE=$?"' Enter
fi

# Method 2: Use tmux's pane_dead flag (if remain-on-exit is set)
# tmux display-message -t "$TASK_ID" -p '#{pane_dead}'  # 1 = process exited

# --- View output ---

# Full output history from log file (ANSI-stripped, grep-friendly)
tail -100 "/tmp/worktrees/$TASK_ID/claude-output.log"

# Search for errors in clean log
grep -i "error\|fail\|panic" "/tmp/worktrees/$TASK_ID/claude-output.log"

# Live view (raw tmux pane, may contain ANSI codes — use for quick glance only)
tmux capture-pane -t "$TASK_ID" -p -S -50

# --- Mid-task steering (DON'T kill — redirect!) ---

# Agent going the wrong direction?
tmux send-keys -t "$TASK_ID" "Stop. Focus on the API layer first, not the UI." Enter

# Agent missing context?
tmux send-keys -t "$TASK_ID" "The schema is in src/types/template.ts. Use that." Enter

# Agent's context window filling up?
tmux send-keys -t "$TASK_ID" "Focus only on these 3 files: api.ts, handler.ts, types.ts" Enter

# Agent needs test guidance?
tmux send-keys -t "$TASK_ID" "Run 'npm test -- --grep auth' to verify your changes." Enter
```

**Monitoring cadence**: Check every 5-10 minutes, not every 30 seconds. Agents need time to work.

### Step 5: Definition of Done

A PR is **NOT ready for review** until all checks pass:

```
✅ PR created              → gh pr list --head "$BRANCH"
✅ No merge conflicts       → gh pr view $PR_NUM --json mergeable -q '.mergeable'
✅ CI passing               → gh pr checks $PR_NUM
✅ AI code review passed    → at least one cross-model review (see Step 6)
✅ UI screenshots included  → (if applicable) screenshot in PR description
```

Quick inline check:
```bash
PR_NUM=$(gh pr list --head "$BRANCH" --json number -q '.[0].number')
echo "PR: #$PR_NUM"
gh pr checks "$PR_NUM"
gh pr view "$PR_NUM" --json mergeable -q '.mergeable'
```

### Step 6: Multi-Model Code Review

Review with a **different model** than the one that wrote the code. Different models catch different issues:

```bash
DIFF=$(gh pr diff "$PR_NUM")

# Option A: Codex reviews Claude's code (best for edge cases & logic errors)
echo "$DIFF" | codex exec -s read-only \
  "Review this PR diff. Focus on: bugs, edge cases, missing error handling, 
   race conditions, security issues. Be specific — cite file and line numbers.
   Output format: list of issues with severity (critical/warning/info)."

# Option B: Claude reviews with security focus
echo "$DIFF" | claude -p \
  --append-system-prompt "You are a security-focused code reviewer. Flag only critical issues." \
  "Review this diff for security vulnerabilities, injection risks, and logic errors."
```

Post review results to PR:
```bash
gh pr comment "$PR_NUM" --body "## AI Code Review

$REVIEW_OUTPUT"
```

Update task registry:
```bash
(
  flock -x 200
  jq --arg id "$TASK_ID" \
    '(.tasks[] | select(.id == $id)).checks.codeReviewPassed = true' \
    "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
) 200>"$TASKS_FILE.lock"
```

### Step 7: Notify

If you included the notify command in the agent prompt (Step 2), the agent self-notifies on completion.

Otherwise, notify after DoD passes:
```bash
openclaw system event --text "✅ PR #$PR_NUM ready for review: $TASK_ID — all checks passed" --mode now
```

Update task status:
```bash
(
  flock -x 200
  jq --arg id "$TASK_ID" --argjson pr "$PR_NUM" \
    '(.tasks[] | select(.id == $id)) |= (.status = "done" | .pr = $pr | .completedAt = (now|floor))' \
    "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
) 200>"$TASKS_FILE.lock"
```

### Step 8: Cleanup

After PR is merged:
```bash
git worktree remove "$WORKTREE" 2>/dev/null
git branch -d "$BRANCH" 2>/dev/null

# Remove from registry
(
  flock -x 200
  jq --arg id "$TASK_ID" '.tasks = [.tasks[] | select(.id != $id)]' \
    "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
) 200>"$TASKS_FILE.lock"
```

---

## Smart Retry Strategy

When an agent fails, **analyze the failure and adapt the prompt** — don't just re-run blindly.

| Failure Type | Symptom | Retry Strategy |
|---|---|---|
| Context overflow | Agent loops, produces garbage, or stops mid-task | Narrow scope: *"Focus only on files X, Y, Z"* |
| Wrong direction | Agent implements something unrelated to intent | Correct intent: *"Stop. Customer wanted X, not Y. Spec: ..."* |
| Missing info | Agent makes wrong assumptions about architecture | Add context: *"Auth uses JWT, see src/auth/jwt.ts"* |
| CI failure | Tests, lint, or typecheck fail after PR | Attach CI log: *"Fix these test failures: ..."* |
| Build failure | Dependencies missing or incompatible | Pre-install deps before retry |

**Max 3 retries.** After that, escalate to human.

```bash
RETRY=$((RETRY + 1))
if [ "$RETRY" -gt 3 ]; then
  openclaw system event --text "BLOCKED: $TASK_ID failed after 3 retries — needs human help" --mode now
  (
    flock -x 200
    jq --arg id "$TASK_ID" '(.tasks[] | select(.id == $id)).status = "blocked"' \
      "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
  ) 200>"$TASKS_FILE.lock"
  exit 1
fi

# Capture what went wrong — prefer log file over tmux scrollback
LOG_FILE="/tmp/worktrees/$TASK_ID/claude-output.log"
if [ -f "$LOG_FILE" ]; then
  # Log file is ANSI-stripped (clean text) — extract error-relevant lines
  # Take last 500 lines, but also grep for error context
  FAILURE_LOG=$(tail -500 "$LOG_FILE")
  ERROR_LINES=$(grep -n -i "error\|fail\|panic\|exception\|traceback" "$LOG_FILE" | tail -50)
  if [ -n "$ERROR_LINES" ]; then
    FAILURE_LOG="=== Error lines ===
$ERROR_LINES

=== Last 500 lines ===
$FAILURE_LOG"
  fi
else
  FAILURE_LOG=$(tmux capture-pane -t "$TASK_ID" -p -S -200)
fi
CI_LOG=$(gh pr checks "$PR_NUM" 2>/dev/null || echo "no PR yet")
tmux kill-session -t "$TASK_ID" 2>/dev/null

# Archive old log, start fresh for retry
[ -f "$LOG_FILE" ] && mv "$LOG_FILE" "${LOG_FILE}.retry$((RETRY - 1))"

# Respawn — set up pipe-pane BEFORE sending command (captures all output)
tmux new-session -d -s "$TASK_ID" -c "$WORKTREE"
tmux pipe-pane -t "$TASK_ID" -o "sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' >> $LOG_FILE"
tmux send-keys -t "$TASK_ID" "claude --dangerously-skip-permissions \
  'Previous attempt failed. Error output:
$FAILURE_LOG

CI status: $CI_LOG

Fix the issues above and complete the original task.
[...your enriched instructions here...]

When done: commit, push, gh pr create --fill, then run:
openclaw system event --text \"Done: $TASK_ID (retry $RETRY)\" --mode now'" Enter

# Update registry with flock
PANE_PID=$(tmux display-message -t "$TASK_ID" -p '#{pane_pid}')
(
  flock -x 200
  jq --arg id "$TASK_ID" --argjson r "$RETRY" --arg pane_pid "$PANE_PID" \
    '(.tasks[] | select(.id == $id)) |= (.retries = $r | .status = "running" | .panePid = ($pane_pid | tonumber) | .silentRounds = 0 | .repeatingRounds = 0 | .lastOutputHash = "")' \
    "$TASKS_FILE" > /tmp/tasks.$$.json && mv /tmp/tasks.$$.json "$TASKS_FILE"
) 200>"$TASKS_FILE.lock"
```

---

## Parallel Execution

Run multiple agents simultaneously on different tasks.
**Important:** Always set up `pipe-pane` before sending the command to avoid losing
early output. Use ANSI stripping for clean logs.

```bash
# Helper: launch an agent in tmux with proper output capture
launch_agent() {
  local TASK_ID="$1" WORKTREE="$2" PROMPT="$3"
  local LOG_FILE="$WORKTREE/claude-output.log"

  # 1. Create session with idle shell
  tmux new-session -d -s "$TASK_ID" -c "$WORKTREE"
  # 2. Start pipe-pane BEFORE command (captures everything, ANSI-stripped)
  tmux pipe-pane -t "$TASK_ID" -o "sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' >> $LOG_FILE"
  # 3. Send command
  tmux send-keys -t "$TASK_ID" "$PROMPT" Enter
}

# Task 1: Feature
git worktree add -b feat/auth /tmp/worktrees/feat-auth origin/main
launch_agent "feat-auth" "/tmp/worktrees/feat-auth" \
  "cd /tmp/worktrees/feat-auth && pnpm install && claude --dangerously-skip-permissions 'Implement JWT auth...'"

# Task 2: Bugfix
git worktree add -b fix/payments /tmp/worktrees/fix-payments origin/main
launch_agent "fix-payments" "/tmp/worktrees/fix-payments" \
  "cd /tmp/worktrees/fix-payments && pnpm install && claude --dangerously-skip-permissions 'Fix payment webhook...'"

# Dashboard: check all agents (uses process check, not just has-session)
echo "=== Agent Status ==="
for s in $(tmux ls -F '#{session_name}' 2>/dev/null); do
  PANE_PID=$(tmux display-message -t "$s" -p '#{pane_pid}' 2>/dev/null)
  if [ -z "$PANE_PID" ]; then
    STATUS="(session gone)"
  elif pgrep -P "$PANE_PID" > /dev/null 2>&1; then
    STATUS="running"
  else
    STATUS="process exited"
  fi
  LOG="/tmp/worktrees/$s/claude-output.log"
  LAST_LINE=$(tail -1 "$LOG" 2>/dev/null || echo "(no log)")
  echo "  $s: $STATUS | last: $LAST_LINE"
done
```

---

## Multi-Turn Conversations

For complex tasks that need iterative refinement:

```bash
# Start session, capture ID
session_id=$(claude -p "analyze the codebase architecture" \
  --output-format json | jq -r '.session_id')

# Continue with context from previous turn
claude -r "$session_id" -p "now implement the changes we discussed" \
  --dangerously-skip-permissions

# Resume in non-interactive mode
claude -r "$session_id" -p "fix the remaining test failures" \
  --dangerously-skip-permissions
```

---

## Best Practices

### Prompt Quality
- **Include file paths**: *"The entry point is src/index.ts, config in src/config/"*
- **Include schemas/types**: Paste relevant type definitions into the prompt
- **Include test commands**: *"Verify with: npm test -- --grep auth"*
- **Include commit convention**: *"Use conventional commits: feat:, fix:, chore:"*
- **Include error logs**: When retrying, always attach the failure output

### Scope Management
- **One task per agent** — don't ask for "refactor everything"
- **Pre-install dependencies** before launching the agent
- **Be specific** — *"Add rate limiting to POST /api/users"* not *"improve the API"*

### When to Interrupt (Ask Human)
- Destructive operations (drop tables, force push main)
- Security decisions (expose credentials, change auth)
- Ambiguous requirements with significant trade-offs
- All other decisions: proceed autonomously

## Examples

See `references/examples.md` for additional usage scenarios.
