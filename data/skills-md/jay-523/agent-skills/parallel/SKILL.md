---
name: parallel
description: Split implementation tasks into independent workstreams running as parallel agents in git worktrees
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[task description or 'plan' to use current plan]"
---

# /parallel -- Parallel Agent Orchestration via tmux + git Worktrees

Split a task into independent workstreams and run them as parallel Claude
Code agents in separate tmux panes, each in its own git worktree.

## Argument

Either a task description to plan and decompose, or the word "plan" to
use the current plan from this conversation.

## Procedure

### Phase 1 -- Plan

If the argument is "plan": use the existing plan from the current
conversation context.

Otherwise: create a plan for the given task. Identify what needs to be
built, the modules involved, and the dependencies between them.

### Phase 2 -- Decompose into Workstreams

Split the plan into 3-4 independent workstreams (hard maximum: 4).

Decomposition rules:
- Divide by **domain/module**, NOT by task type. Each agent owns a
  vertical slice (e.g., "auth module", "payment module"), not a
  horizontal layer (e.g., "write all tests", "write all implementations").
  Horizontal decomposition causes 3-10x token waste because each agent
  must re-read the same context.
- Each agent owns its files **exclusively**. No two agents write to the
  same file. Shared dependencies are read-only for non-owning agents.
- If a workstream depends on another's output, mark it and sequence
  the launch accordingly.

Present the decomposition table and wait for user approval:

```
| Agent | Domain | Owned Files | Read-Only Files | Depends On |
|-------|--------|-------------|-----------------|------------|
| auth  | Authentication | src/auth/* | src/models/* | none |
| api   | API endpoints  | src/api/*  | src/auth/*   | auth |
| ui    | Frontend       | src/ui/*   | src/api/*    | none |
```

Do NOT proceed until the user approves this decomposition.

### Phase 3 -- Setup Worktrees

For each agent in the approved decomposition:

```bash
git worktree add ./worktrees/{agent-name} -b parallel/{agent-name}
```

Add `worktrees/` to `.gitignore` if not already present.

For each worktree:
```bash
# Copy environment files
cp .env ./worktrees/{agent-name}/.env 2>/dev/null || true
cp -r venv ./worktrees/{agent-name}/venv 2>/dev/null || true

# Create coordination directories
mkdir -p ./worktrees/{agent-name}/run
mkdir -p ./shared/progress
```

Install dependencies if needed:
```bash
cd ./worktrees/{agent-name} && source venv/bin/activate && uv pip install -e . 2>/dev/null || true
```

### Phase 4 -- Generate Agent Prompts

For each agent, write `./worktrees/{agent-name}/run/prompt.md` containing:

1. **Scope**: What this agent is responsible for building
2. **File Ownership**: Files this agent may create/modify (exclusive)
3. **Read-Only Files**: Files this agent may read but must not modify
4. **Success Criteria**: How to know when the work is done
5. **Constraints**:
   - Follow all CLAUDE.md conventions (copy relevant entries)
   - Add docstrings to all functions with algorithm in English
   - Expected schema for loose objects in docstrings
   - `if __name__ == '__main__'` blocks with hardcoded examples
   - No argparse, no emojis
   - Use `uv pip install`, `source venv/bin/activate`
6. **Progress Tracking**: Write status to
   `../shared/progress/{agent-name}.json` after each major milestone
   using this format:
   ```json
   {
     "agent": "{agent-name}",
     "timestamp": "ISO-8601",
     "status": "in_progress|blocked|done",
     "completed": ["list of completed items"],
     "remaining": ["list of remaining items"],
     "blocked_by": null,
     "notes": ""
   }
   ```

### Phase 4.5 -- Create Launcher Script

Write `./run-agent.sh` in the project root:

```bash
#!/bin/bash
# Usage: bash run-agent.sh /path/to/worktree [model]
# Pipes the agent prompt to claude -p with pre-approved tools.
# Writes output to run/output.md and prints a COMPLETE marker when done.
cd "$1"
source venv/bin/activate 2>/dev/null || true
MODEL="${2:-claude-sonnet-4-6}"
echo "=== Starting agent: $(basename $1) with model $MODEL ==="
echo "=== $(date) ==="
echo ""
cat run/prompt.md | claude -p \
  --model "$MODEL" \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  2>&1 | tee run/output.md
echo ""
echo "=== Agent $(basename $1) COMPLETE at $(date) ==="
```

Make it executable: `chmod +x run-agent.sh`

CRITICAL: **Pipe the prompt via stdin** (`cat prompt.md | claude -p`).
NEVER pass the prompt content through `tmux send-keys` -- any quotes,
backticks, `$`, backslashes, or newlines in the prompt will be
shell-expanded or break the command. The launcher script avoids this
entirely by keeping the prompt in a file and piping it.

### Phase 5 -- Launch Agents

Create a tmux session and launch agents via the launcher script:

```bash
# Create session
tmux new-session -d -s parallel -x 200 -y 50

# First agent gets the first pane
tmux send-keys -t parallel "bash run-agent.sh $(pwd)/worktrees/{agent-1}" Enter

# Additional agents get split panes
tmux split-window -t parallel -h
tmux send-keys -t parallel "bash run-agent.sh $(pwd)/worktrees/{agent-2}" Enter

# Repeat for agents 3-4 if needed
tmux split-window -t parallel -v
tmux send-keys -t parallel "bash run-agent.sh $(pwd)/worktrees/{agent-3}" Enter
```

After launching, verify processes are running:

```bash
ps aux | grep "claude -p" | grep -v grep | wc -l
```

Print monitoring instructions for the user:

```
## Parallel Agents Running

Attach to the session:
  tmux attach -t parallel

Monitor progress:
  cat shared/progress/*.json | jq .

Switch between panes:
  Ctrl-b + arrow keys

Kill session when done:
  tmux kill-session -t parallel
```

### Phase 5.5 -- Wait for Completion

Use the `wait-for-text.sh` helper from the `/tmux` skill to
automatically detect when each agent finishes:

```bash
WAIT="$HOME/Developer/personal_projects/agent-skills/skills/tmux/scripts/wait-for-text.sh"
TIMEOUT=600  # 10 minutes per agent; adjust as needed

all_done=true
for pane_id in {list of parallel:0.N targets}; do
  agent_name="{name for this pane}"
  if bash "$WAIT" -t "$pane_id" -p "COMPLETE" -T "$TIMEOUT" -i 5; then
    echo "$agent_name: DONE"
  else
    echo "$agent_name: TIMED OUT or FAILED -- check pane manually"
    all_done=false
  fi
done

if $all_done; then
  echo "All agents complete. Ready to merge."
else
  echo "Some agents did not finish. Check timed-out panes before merging."
fi
```

The loop watches for the `COMPLETE` marker that `run-agent.sh` prints
when `claude -p` exits. Each agent gets the full timeout before moving
to the next check.

You can also manually check progress via `cat shared/progress/*.json`.

### Phase 6 -- Merge Strategy

After all agents report "done", provide merge commands:

```bash
# Merge each agent branch with --no-ff to preserve history
git merge --no-ff parallel/{agent-1} -m "Merge {agent-1}: {description}"
git merge --no-ff parallel/{agent-2} -m "Merge {agent-2}: {description}"
git merge --no-ff parallel/{agent-3} -m "Merge {agent-3}: {description}"
```

Conflict resolution guidance:
- If two agents touched the same file despite ownership rules, the
  owning agent's version wins
- For shared config files (package.json, pyproject.toml), merge both
  sets of changes manually
- Run the full test suite after each merge

Cleanup commands:
```bash
# Remove worktrees
git worktree remove ./worktrees/{agent-1}
git worktree remove ./worktrees/{agent-2}
git worktree remove ./worktrees/{agent-3}

# Delete branches
git branch -d parallel/{agent-1}
git branch -d parallel/{agent-2}
git branch -d parallel/{agent-3}

# Remove shared progress
rm -rf ./shared/progress/
```

## Troubleshooting

**Check agent status**
Run the health-check recipe from `/tmux` to classify every pane:
```bash
DIAG="$HOME/Developer/personal_projects/agent-skills/skills/tmux/scripts/diagnose-agents.sh"
bash "$DIAG" parallel "worktrees/*/run/output.md"
```
Each pane is classified as DONE, WORKING, FAILED, or UNKNOWN. See the
`/tmux` skill's "Health-Check Running Agents" recipe for details on
what each state means and how it's detected.

**FAILED state -- what to do**
Inspect the pane for the root cause:
```bash
tmux capture-pane -t parallel:0.{pane} -p -S - | tail -30
```
Common causes: rate limit hit, permission denial (missing
`--allowedTools`), Python/Node traceback, or OOM. Fix the cause and
re-launch the agent (see below).

**DONE but no run/output.md**
This is a `tee` buffering issue. The agent finished (COMPLETE marker
present in the pane) but the file wasn't flushed. Capture the pane
scrollback directly:
```bash
tmux capture-pane -t parallel:0.{pane} -p -S - > worktrees/{agent}/run/output.md
```

**Re-running a single failed agent**
Send the launcher command to the same pane:
```bash
tmux send-keys -t parallel:0.{pane} "bash run-agent.sh $(pwd)/worktrees/{agent-name}" Enter
```
The previous output.md will be overwritten by `tee`.

**tmux session died**
Re-create the session (Phase 5). Run `diagnose-agents.sh` or check
which agents have the COMPLETE marker in their `run/output.md`. Only
re-launch agents that didn't complete. Completed agents already
committed their work to their worktree branch.

**Worktree in a bad state after agent crash**
Check the branch for partial commits: `cd worktrees/{agent} && git log --oneline -5`.
If the agent made useful partial progress, you can keep the branch and
re-launch to continue. If the state is unrecoverable:
```bash
git worktree remove ./worktrees/{agent-name}
git branch -D parallel/{agent-name}
```
Then re-create the worktree (Phase 3) and re-launch.

**Merge conflicts during Phase 6**
If agents violated file ownership rules and both modified the same file,
the owning agent's version wins. Use `git checkout --theirs {file}` or
`git checkout --ours {file}` accordingly. Run tests after each merge.

## Important

- Maximum 3-4 parallel agents. More than 4 has diminishing returns
  and burns credits rapidly.
- Always decompose by domain/module, never by task type.
- Always wait for user approval of the decomposition before creating
  worktrees.
- Each agent MUST have exclusive file ownership. Overlapping writes
  guarantee merge conflicts and wasted work.
- Do not launch agents for tasks that have sequential dependencies.
  If B depends on A's output, A must finish first.
