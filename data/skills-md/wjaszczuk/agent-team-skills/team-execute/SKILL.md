---
name: team-execute
description: Use when you have a plan created by team-plan. Orchestrates Developer and Architect agents per task with progress tracking and state persistence for resumability.
---

# Team Execute

Orchestrate implementation of a plan using named Developer and Architect agents.

**Announce at start:** "I'm using the team-execute skill to implement this plan."

## Setup

### Step 1: Locate plan and state

Ask user for plan path if not provided. State file is `<plan-path-without-extension>.state.json`.

Read both files. If state file doesn't exist, assume all tasks pending.

### Step 2: Set up worktree

**REQUIRED SUB-SKILL:** Use `superpowers:using-git-worktrees` to create or switch to the feature worktree.

Save worktree path and branch to `.state.json`.

### Step 3: Generate and display resume prompt

Generate the resume prompt and show it to the user:

```
=== RESUME PROMPT ===
If this session is interrupted, start a new session and paste this:

Resume implementation:
- Plan: <plan path>
- State: <state.json path>
- Worktree: <worktree path> (branch: <branch>)
- Next task: #<N> "<title>"

Use team-execute skill to continue.
====================
```

Save this prompt to `.state.json` → `resumePrompt` field.

### Step 4: Determine starting point

Check `.state.json` for tasks with `status: "completed"` — skip those.
Find first `pending` or `in_progress` task — start there.

Show initial progress checklist:

```
Progress:
✅ Task 1: <title>    (completed)
🔄 Task 2: <title>    (in progress / next up)
⏳ Task 3: <title>    (pending)
```

## Per-Task Loop

For each pending task (in order):

### Phase A: Developer

**Step A1: Update state**
Set task `status: "in_progress"`, `startedAt: <timestamp>`, `agent: "developer"` in `.state.json`.

**Step A2: Print checklist update**

```
🔄 Task N: <title> — Developer agent starting...

Progress:
✅ Task 1: <title>
🔄 Task 2: <title>
⏳ Task 3: <title>
```

**Step A3: Dispatch Developer agent**

Use the Agent tool to launch a `team-developer` agent. Provide:
- Full task text (copy from plan — do NOT ask agent to read the plan)
- Project context: tech stack, conventions, ADRs location, design doc location
- Worktree path and branch
- `.state.json` path

Wait for Developer agent to complete and report back.

**Step A4: Handle questions**
If Developer agent asks questions before starting, answer them. Provide all needed context.

**Step A5: Update state with commit**
Update `.state.json`: set `commit: <SHA>` from Developer report.

### Phase B: Architect Review

**Step B1: Get diff**

```bash
git -C <worktree> diff HEAD~1 HEAD
```

**Step B2: Dispatch Architect agent**

Use the Agent tool to launch a `team-architect` agent. Provide:
- The git diff
- Full task spec (copy from plan)
- Paths to ADRs and design documents (let agent read them)
- Project conventions summary

Wait for Architect agent verdict.

**Step B3: Handle CHANGES_REQUIRED**

If `CHANGES_REQUIRED`:
- Show issues to user
- Dispatch Developer agent again with: original task + list of issues to fix
- After fix: re-dispatch Architect agent
- Repeat until `APPROVED`

**Step B4: Mark task complete**

Update `.state.json`:

```json
{
  "status": "completed",
  "completedAt": "<timestamp>"
}
```

Update plan file — check off task in `## Progress`:

```markdown
- [x] Task N: <title>
```

**Step B5: Push and print checklist**

```bash
git -C <worktree> push origin <branch>
```

Print updated checklist:

```
✅ Task N complete — pushed to <branch>

Progress:
✅ Task 1: <title>
✅ Task 2: <title>
🔄 Task 3: <title>
⏳ Task 4: <title>
```

## Completion

After all tasks complete:

### Step 1: Cleanup state file

```bash
rm docs/plans/*.state.json
git add -A docs/plans/
git commit -m "chore: remove plan state file (implementation complete)"
git push
```

### Step 2: Update plan Progress section

All checkboxes should be `[x]`. Commit the plan file update:

```bash
git add docs/plans/<plan>.md
git commit -m "docs: mark plan complete"
git push
```

### Step 3: Final summary

Print:

```
✅ All tasks complete!

Progress:
✅ Task 1: <title>
✅ Task 2: <title>
...
```

### Step 4: Finish branch

**REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`

## Resume After Interruption

If user pastes a resume prompt:
1. Read `.state.json` — it has current state
2. Skip completed tasks
3. Resume from first `pending` or `in_progress` task
4. Continue per-task loop as normal

## Red Flags

**Never:**
- Skip the resume prompt display at start
- Let an agent read the plan file themselves (provide full text)
- Move to Architect before Developer is done
- Skip Architect review
- Proceed to next task if Architect returns CHANGES_REQUIRED
- Delete `.state.json` before all tasks are complete
- Push to main/master
