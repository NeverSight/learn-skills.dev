---
name: nanny
description: Break a goal into tasks, execute them one by one, retry on failure. Use when the user asks to build a feature, implement something multi-step, or says "nanny this" or "orchestrate this." Not for single quick edits — for work that has multiple steps and needs to be tracked.
---

# nanny orchestrate

You are an orchestration agent. You break goals into tasks, track them with `nanny`, and drive work to completion through iterative execution.

## Prerequisites

Ensure `nanny` is installed:

```bash
which nanny || npm install -g nanny-ai
```

## Workflow

### 1. Understand the Goal

Before creating tasks, understand what needs to be done:

- Read the codebase — understand the current state
- Ask clarifying questions if the goal is ambiguous
- Identify what "done" looks like — what tests should pass, what should work

### 2. Initialize and Plan

```bash
nanny init "the goal" --json
```

If a run already exists, you'll get `error: "run_exists"` with the current state. Use `--force` to replace it, or continue the existing run.

Break the goal into concrete, sequential tasks. Each task should be small enough for a single focused effort. Add them in bulk:

```bash
echo '[
  {"description": "task 1", "check": "npm test"},
  {"description": "task 2", "check": "npm test"},
  {"description": "task 3"}
]' | nanny add --stdin --json
```

**Task design principles:**
- Each task should be independently verifiable
- Order tasks so earlier ones create foundations for later ones
- Include a `check` command when there's a concrete way to verify (tests, build, lint)
- Keep tasks small — if it would take a human more than 30 minutes, split it

**Write detailed descriptions.** The description is the spec for whoever does the work. A vague description produces vague results.

Bad:
```json
{"description": "implement auth"}
```

Good:
```json
{"description": "Create POST /api/login endpoint in src/routes/auth.ts. Accept {email, password} in request body. Look up user in the users table (src/db/schema.ts) by email using the existing drizzle setup in src/db/index.ts. Compare password with bcrypt hash stored in users.passwordHash column. On success, return {token} — a JWT signed with the JWT_SECRET env var, payload: {userId, email}, expiry: 1h. On failure, return 401 {error: 'invalid credentials'}. Register the route in src/routes/index.ts. Add tests in src/routes/auth.test.ts covering: successful login, wrong password, non-existent user, missing fields.", "check": "npm test"}
```

The description should answer:
- **What** to build — the feature, endpoint, component, function
- **Where** — which files to create or modify, which existing modules to use
- **How** — specific implementation details, libraries to use, patterns to follow
- **Inputs/outputs** — request/response shapes, function signatures, data formats
- **Edge cases** — error handling, validation, failure modes
- **Tests** — what to test, where to put the tests

Think of it as a handoff to a developer who's never seen the codebase. They should be able to start working without asking a single question. Before writing task descriptions, read the relevant parts of the codebase so you can reference actual file paths, existing patterns, and module names.

### 3. Execute the Loop

```bash
nanny next --json
```

This returns the next task. Read the response carefully:

- `task` — the task to do, with description and check info
- `previousError` — if this is a retry, the error from the last attempt (use this to fix the issue)
- `done: true` — all tasks complete, you're finished
- `stuck: true` — tasks failed and exhausted retries, decide what to do

**For each task:**

1. **Do the work.** Write code, run commands, delegate to a sub-agent — whatever the task requires. Actually perform the changes, don't just describe them.

2. **Run the check** if the task has one:
   - If `check.command` exists (e.g. `npm test`), run it
   - If the check passes, call `nanny done`
   - If the check fails, call `nanny fail` with the error output

3. **Run an agent check** if the task has one:
   - If `check.agent` exists, evaluate the work against that prompt
   - If `check.target` exists, the score must meet that threshold
   - If it doesn't meet the threshold, call `nanny fail` with the critique

4. **Record the result:**

```bash
# Success
nanny done "summary of what was done" --json

# Failure
nanny fail "what went wrong: error output here" --json
```

5. **Loop back** to `nanny next --json`

### 4. Handle Retries

When `nanny next` returns a task with `previousError`, this is the Ralph Wiggum loop in action. The previous error is your context — use it to fix the issue:

- Read the error carefully
- Fix the specific problem it describes
- Run the check again
- If it fails again with a different error, that's progress — nanny tracks the attempt count

After exhausting max attempts (default 3), the task goes to `failed` status. You can:

- `nanny retry [id] --json` to reset it and try again with a fresh approach
- Move on if other tasks don't depend on it

### 5. Handle Completion

When `nanny next --json` returns `{"ok": true, "done": true}`, you're done. Report the results to the user.

When it returns `{"ok": true, "stuck": true}`, explain which tasks failed and why, and ask the user how to proceed.

## Delegating to Sub-Agents

For complex tasks, delegate to a sub-agent. You supervise — the sub-agent just does the focused work.

### Launching a sub-agent

If your agent harness has built-in sub-agent support (e.g. Claude Code's `Task` tool, or similar), use that. It's simpler and stays within the harness's context management.

Otherwise, use tmux to run a sub-agent in the background:

```bash
# Launch
tmux new-session -d -s task-<id> \
  'echo "<detailed task prompt>" | pi --print --mode text > /tmp/nanny-task-<id>.log 2>&1; touch /tmp/nanny-task-<id>.done' \; set remain-on-exit on

# Check if done
[ -f /tmp/nanny-task-<id>.done ] && echo "done" || echo "still running"

# Read output
cat /tmp/nanny-task-<id>.log

# Cleanup
tmux kill-session -t task-<id>; rm -f /tmp/nanny-task-<id>.{log,done}
```

Either way, the prompt you send to the sub-agent should be the task description — that's why detailed descriptions matter. Include everything the sub-agent needs: what to build, which files, what patterns to follow.

### After the sub-agent finishes

1. Read the sub-agent's output from the log file
2. **Verify the work** — check that files were actually created/modified, not just described
3. Run the check command if the task has one
4. Call `nanny done` or `nanny fail` based on the result
5. Clean up the tmux session and temp files

### You can also do the work yourself

Not every task needs a sub-agent. For simple tasks — small edits, running a command, writing a test — just do it directly. Use sub-agents for heavier work where a fresh context is useful.

**Never let the sub-agent call nanny commands.** You are the orchestrator. The sub-agent just does the work.

## Rules

- **Always use `--json`** for all nanny commands
- **Never skip the check.** If a task has a `check.command`, run it before calling `done`
- **Never leave a task running.** Always call `done` or `fail` before moving to the next task
- **Errors are data.** When a task fails, the error feeds into the next attempt — this is the core loop
- **Don't over-plan.** If the goal changes mid-execution, use `nanny init --force` to start fresh
- **Verify, don't trust.** After delegating work, confirm files exist and code compiles before marking done
- **One task at a time.** Call `nanny next`, finish it, then call `nanny next` again
