---
name: fork
description: Fork the current session with context carried over. Use `/fork <branch>` for a new worktree or `/fork --local` for a new session in the current directory.
license: Apache-2.0
requires:
  - git-worktree  # uses `wt --context` for worktree creation (when not --local)
---

# Fork Session

Fork the current session, carrying context for continuity.

## Usage

```
/fork <branch>                     # Default: open new terminal tab with interactive claude
/fork <branch> --base <ref>        # Fork from a specific base branch/ref
/fork <branch> --move              # Move this session into the worktree
/fork <branch> --team              # Spawn a coordinated teammate in the worktree
/fork <branch> --background        # Spawn autonomous fire-and-forget agent
/fork --local                      # Write handoff for manual pickup
```

## Modes

| Mode | Interactive? | Coordinated? | User stays here? | Best for |
|------|-------------|-------------|-------------------|----------|
| Terminal (default) | Yes | No | Yes | Exploratory/uncertain work |
| Move | Yes | N/A | No | Fully switching focus |
| Team | No | Yes | Yes | Delegated work with oversight |
| Background | No | No | Yes | Well-defined autonomous tasks |
| Local | Manual | N/A | Yes | When other modes aren't available |

## Instructions

### Step 1: Determine Mode and Options

Check the user's input:

| Input | Mode |
|-------|------|
| `/fork <branch>` | Terminal (default) |
| `/fork <branch> --move` | Move |
| `/fork <branch> --team` | Team |
| `/fork <branch> --background` | Background |
| `/fork --local` | Local |
| `/fork` (no args) | Ask: "Branch name for new worktree, or `--local` for same directory?" |

**Options** (combine with any worktree mode):
- `--base <ref>` — Create the worktree from a specific branch, tag, or commit instead of main. Passed through to `wt` as `--base <ref>`.

### Step 2: Generate Context Summary

Create a handoff document summarizing:

1. **Current Task** - what we're working on
2. **Progress** - what's been done so far
3. **Key Decisions** - important choices made
4. **Next Steps** - what the new session should tackle
5. **Relevant Files** - files we've been working with
6. **Open Questions** - unresolved issues

Use this template:

```markdown
# Session Handoff

## Current Task
{Brief description of what we're working on}

## Progress
- {What's been completed}
- {What's in progress}

## Key Decisions
| Decision | Choice | Why |
|----------|--------|-----|
| {topic} | {choice} | {rationale} |

## Next Steps
1. {Immediate next action}
2. {Following action}

## Relevant Files
- `path/to/file.ts` - {why it matters}

## Open Questions
- {Unresolved question or blocker}

---
*Forked from session on {date}*
```

### Step 3: Create Worktree + Transition

Build the `wt` command with appropriate flags. If `--base` was specified, include `--base <ref>` in the wt invocation.

#### Terminal mode (default)

```bash
HANDOFF=$(mktemp)
cat > "$HANDOFF" << 'EOF'
{generated handoff content}
EOF

# Without --base (defaults to main):
wt <branch> --no-editor --context "$HANDOFF" --open

# With --base:
wt <branch> --base <ref> --no-editor --context "$HANDOFF" --open
```

The `--open` flag opens a new terminal tab in the worktree with an interactive claude session. Since `--context` places a handoff file, `--open` automatically tells claude to read it.

#### Move mode

```bash
HANDOFF=$(mktemp)
cat > "$HANDOFF" << 'EOF'
{generated handoff content}
EOF

wt <branch> --no-editor --context "$HANDOFF"  # add --base <ref> if specified
```

After the worktree is created, use Bash to `cd` into `~/.worktrees/<repo>/<branch>`, then read `.context/handoff.md` and continue working from there. The user's session moves into the worktree.

#### Team mode

```bash
HANDOFF=$(mktemp)
cat > "$HANDOFF" << 'EOF'
{generated handoff content}
EOF

wt <branch> --no-editor --context "$HANDOFF"  # add --base <ref> if specified
```

After the worktree is created:

1. Create or reuse team:
```
TeamCreate(team_name: "fork-<branch>", description: "Forked work: <branch>")
```

2. Create task from handoff:
```
TaskCreate(
  subject: "<task from handoff Next Steps>",
  description: "<full handoff content>",
  activeForm: "Working on <branch>"
)
```

3. Spawn teammate in worktree:
```
Task(
  team_name: "fork-<branch>",
  name: "<branch>-worker",
  subagent_type: "general-purpose",
  prompt: "You are working in a forked worktree at ~/.worktrees/<repo>/<branch>.
    Use absolute paths for all file operations.
    Read .context/handoff.md at that path for full context.

    Work through the task list (TaskList). Update tasks as you progress (TaskUpdate).
    When blocked or done, message the team lead via SendMessage.
    Commit changes with conventional commits."
)
```

4. Assign task to teammate:
```
TaskUpdate(taskId: "<id>", owner: "<branch>-worker", status: "in_progress")
```

The main session stays active. Teammate messages arrive automatically when idle. The user can:
- Check progress: `TaskList`
- Send instructions: `SendMessage` to `<branch>-worker`
- Shut down: `SendMessage(type: "shutdown_request", recipient: "<branch>-worker")`

#### Background mode

```bash
HANDOFF=$(mktemp)
cat > "$HANDOFF" << 'EOF'
{generated handoff content}
EOF

wt <branch> --no-editor --context "$HANDOFF"  # add --base <ref> if specified
```

After the worktree is created, run claude in the background:

```bash
cd ~/.worktrees/<repo>/<branch> && claude --print 'Read .context/handoff.md and complete the work described there. Commit with conventional commits.' > /tmp/fork-<branch>.log 2>&1
```

Use `run_in_background: true` on the Bash tool call.

#### Local mode

```bash
mkdir -p .context
cat > .context/handoff.md << 'EOF'
{generated handoff content}
EOF
```

No worktree created. User opens a new terminal and runs `claude`.

### Step 4: Confirm

Mode-specific confirmation messages:

- **Terminal**: "Forked to `<branch>`. New terminal tab opened with interactive Claude session. Handoff at `~/.worktrees/<repo>/<branch>/.context/handoff.md`."
- **Move**: "Moved into worktree `<branch>`. To return: `cd <original_path>`"
- **Team**: "Forked to `<branch>`. Teammate `<branch>-worker` is working in the worktree. Messages will arrive here when they need input or finish."
- **Background**: "Forked to `<branch>`. Monitor: `tail -f /tmp/fork-<branch>.log`"
- **Local**: "Context written to `.context/handoff.md`. Open a new terminal here and run `claude`."

If `--base` was used, include it in the confirmation: "Based on `<ref>`."

## Examples

### Terminal Fork (default)
```
User: /fork feature-dark-mode

Claude: I'll fork this session to a new worktree with an interactive Claude session.

[Generates handoff summary]
[Runs: wt feature-dark-mode --no-editor --context /tmp/handoff.md --open]

Forked to `feature-dark-mode`. New terminal tab opened with interactive Claude session.
Handoff at ~/.worktrees/dotclaude/feature-dark-mode/.context/handoff.md
```

### Fork from a specific base
```
User: /fork fix-auth-bug --base release/v2.1

Claude: I'll fork from `release/v2.1` to a new worktree.

[Generates handoff summary]
[Runs: wt fix-auth-bug --base release/v2.1 --no-editor --context /tmp/handoff.md --open]

Forked to `fix-auth-bug` based on `release/v2.1`. New terminal tab opened.
```

### Team Fork
```
User: /fork feature-auth --team

Claude: I'll fork and spawn a teammate to work on it.

[Generates handoff summary]
[Creates worktree, team, task, spawns teammate]

Forked to `feature-auth`. Teammate `feature-auth-worker` is working in the worktree.
Messages will arrive here when they need input or finish.
```

### Local Fork
```
User: /fork --local

Claude: I'll prepare a handoff for a new session in this directory.

[Generates handoff summary]
[Writes to .context/handoff.md]

Context written to `.context/handoff.md`.
Open a new terminal here and run `claude`.
```

## Notes

- **Worktree naming**: `<repo>` is derived from `git remote get-url origin` (e.g., `~/.claude` with remote `dotclaude.git` → `~/.worktrees/dotclaude/<branch>`)
- **Requires**: `git-worktree` skill for all modes except `--local`
- The handoff is a snapshot - it won't update if you continue working here
- Use `/chronicle` if you want persistent cross-session memory instead
- Worktree mode runs setup scripts from `conductor.json` if present
- Terminal mode uses `wt --open` which requires macOS (osascript)
- `--base` defaults to `main` if not specified (same as `wt` default)
