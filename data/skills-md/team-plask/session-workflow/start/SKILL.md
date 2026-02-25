---
name: start
description: Start a task session — creates a Linear issue, git worktree, and launches a new Claude session. Use when the user says /start or wants to begin a new isolated task.
user-invocable: true
allowed-tools: Bash(git:*) Bash(osascript:*) Bash(bash:*) mcp__linear-server__create_issue mcp__claude_ai_Linear__create_issue mcp__claude_ai_Supabase__create_branch mcp__claude_ai_Supabase__get_cost mcp__claude_ai_Supabase__confirm_cost
---

> **Implementation note:** Steps 1, 3, 4, 5 are purely mechanical — execute them without deliberation. Only Step 2 (Linear issue) requires judgment for the title.

# Start Task Session

Create a Linear issue, git worktree, and launch a new Claude session for the task.

**Task:** $ARGUMENTS

## Instructions

### Step 0: Load Config

Read `.claude/session-config.json` from the project root. If it doesn't exist, use these defaults:

```json
{
  "linear": { "team": "Engineering", "labels": ["claude-session"], "startState": "started" },
  "github": { "baseBranch": "main" },
  "supabase": { "branchingEnabled": false, "projectId": "", "organizationId": "" },
  "entire": { "enabled": false },
  "worktrees": { "directory": ".worktrees" }
}
```

Use config values throughout (referred to as `config.linear.team`, etc.).

### Step 1: Clean Up Previous Worktrees

Run the cleanup script to remove any completed worktrees from previous sessions:

```bash
bash "$(dirname "$(claude skill path start")")/scripts/done-cleanup.sh" 2>/dev/null || true
```

If the skill script path isn't resolvable, fall back to:
```bash
# Find the done-cleanup.sh in .claude/skills
find -L .claude/skills -name "done-cleanup.sh" -exec bash {} \; 2>/dev/null || true
```

### Step 2: Create Linear Issue

Use the Linear MCP tool (try `mcp__linear-server__create_issue` first, fall back to `mcp__claude_ai_Linear__create_issue`) to create a new issue:

- **team**: `config.linear.team`
- **title**: Derive a short, descriptive title from `$ARGUMENTS` (e.g., "Fix login bug on reservation form")
- **labels**: `config.linear.labels`
- **state**: `config.linear.startState`
- **assignee**: "me"

From the response, extract:
- `id` (UUID)
- `identifier` (e.g., "LNY-350")
- `gitBranchName` (e.g., "junho/lny-350-fix-login-bug")
- `url` (e.g., "https://linear.app/.../LNY-350")

### Step 3: Create Worktree

Build the state JSON object:

```json
{
  "linearIssueId": "<id from step 2>",
  "linearIssueIdentifier": "<identifier from step 2>",
  "linearIssueUrl": "<url from step 2>",
  "linearBranchName": "<gitBranchName from step 2>",
  "worktreePath": "<repo-root>/<config.worktrees.directory>/<sanitized-branch>",
  "mainRepoPath": "<repo-root>",
  "taskDescription": "$ARGUMENTS",
  "createdAt": "<current ISO timestamp>",
  "status": "active"
}
```

Where `<sanitized-branch>` is the `gitBranchName` with `/` replaced by `-`.

Run the worktree creation script:

```bash
# Find the start-worktree.sh script
SCRIPT=$(find -L .claude/skills -name "start-worktree.sh" | head -1)
bash "$SCRIPT" "<gitBranchName>" '<state-json>'
```

The script will:
- Create the worktree directory with a new branch from `origin/<baseBranch>`
- Write `.claude/session-state.json` inside the worktree
- Write `.claude/worktree-sessions/<sanitized-branch>.json` in the main repo

### Step 4: Create Supabase Branch

If `config.supabase.branchingEnabled` is true and `config.supabase.projectId` is set:

Use `mcp__claude_ai_Supabase__get_cost` with:
- type: "branch"
- organization_id: config.supabase.organizationId

Then `mcp__claude_ai_Supabase__confirm_cost` with the returned amount.

Then `mcp__claude_ai_Supabase__create_branch` with:
- project_id: config.supabase.projectId
- name: the Linear branch name (sanitized)
- confirm_cost_id: from confirm_cost response

From the response, extract the branch's `project_ref` (the branch's own project ID for queries).

Add to the session-state JSON:
- "supabaseBranchId": "<branch ID>"
- "supabaseBranchProjectRef": "<branch project_ref>"

Update the worktree's `.claude/session-state.json` with these fields.

### Step 5: Launch Claude in Worktree

Open Claude in a new split pane in Ghostty (or fall back to Terminal.app):

If running inside Ghostty (check `$GHOSTTY_RESOURCES_DIR`):

```bash
osascript <<'APPLESCRIPT'
tell application "System Events"
    tell (first process whose bundle identifier is "com.mitchellh.ghostty")
        keystroke "d" using command down
        delay 0.8
        set the clipboard to "cd <worktree-path> && claude \"$(cat .claude/initial-prompt.txt)\""
        keystroke "v" using command down
        delay 0.1
        keystroke return
    end tell
end tell
APPLESCRIPT
```

Otherwise fall back to Terminal.app:

```bash
osascript -e 'tell application "Terminal" to do script "cd <worktree-path> && claude \"$(cat .claude/initial-prompt.txt)\""'
```

Replace `<worktree-path>` with the actual worktree path returned from Step 3.

### Step 6: Confirm

Print a summary:

```
Linear: <identifier> - <url>
Branch: <gitBranchName>
Worktree: <worktrees-dir>/<sanitized-branch>/
Supabase Branch: <supabaseBranchId> (project ref: <supabaseBranchProjectRef>)
New split opened with Claude session
```

If Supabase branching was not enabled, omit the Supabase line.

Tell the user to switch to the new split pane to start working.
