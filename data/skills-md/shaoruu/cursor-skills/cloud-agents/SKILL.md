---
name: cloud-agents
description: Manage Cursor Cloud Agents via the API. Launch agents, list running agents, check status, get conversation history, send follow-ups, stop or delete agents, and pull agent branch changes into the local repo. Use when the user mentions cloud agents, background agents, launching a task on a repo, checking agent status, or pulling agent changes.
disable-model-invocation: true
---

# Cloud Agents

Manage Cursor Cloud Agents through the REST API at `https://api.cursor.com/v0`.

## Prerequisites

- `CURSOR_API_KEY` environment variable must be set
- `jq` must be installed (used by the helper script)
- If the key is not set, ask the user to provide it or set it: `export CURSOR_API_KEY=<key>`
- Keys are created at https://cursor.com/settings

## Inferring the Repository

When the user does not specify a repo URL, infer it from the current working directory:

```bash
git remote get-url origin
```

This gives you the GitHub URL to pass to `launch`. Also infer the current branch with `git branch --show-current` to use as the `ref` unless the user specifies otherwise.

## Error Handling

If any step fails (API call, git operation, image encoding, etc.), do not attempt to automatically fix or retry. Instead, clearly report the error to the user: what command failed, the error message, and suggest what they can do about it. Let the user decide the next step.

## Helper Script

All API calls go through `scripts/cloud-agent.sh` (relative to this skill directory). Execute it via the Shell tool.

```bash
SKILL_DIR="$HOME/.cursor/skills/cloud-agents"
"$SKILL_DIR/scripts/cloud-agent.sh" <command> [args...]
```

## Commands Reference

### List agents

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" list          # default 20
"$SKILL_DIR/scripts/cloud-agent.sh" list 50        # up to 100
```

Pipe through jq for readable output:

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" list | jq '.agents[] | {id, name, status, branch: .target.branchName, pr: .target.prUrl}'
```

### Check agent status

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" status <agent_id> | jq .
```

Statuses: `CREATING`, `RUNNING`, `FINISHED`, `STOPPED`, `ERROR`

### Get conversation history

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" conversation <agent_id> | jq '.messages[] | {type, text}'
```

### Launch a new agent

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" launch \
  "https://github.com/org/repo" \
  "Your prompt here" \
  main \       # ref (optional, default: main)
  true \       # auto-create PR (optional, default: false)
  "" \         # model (optional, empty = auto)
  "my-branch"  # custom branch name (optional)
```

### Launch agent on an existing PR

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" launch-pr \
  "https://github.com/org/repo/pull/123" \
  "Fix the failing tests"
```

### Send follow-up

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" followup <agent_id> "Also add tests"
```

### Attaching images

Images can be appended as trailing file paths to `launch`, `launch-pr`, and `followup` (max 5). The script base64-encodes them and extracts dimensions via `sips`.

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" launch \
  "https://github.com/org/repo" \
  "Implement this design" \
  main false "" "" \
  /path/to/mockup.png /path/to/reference.jpg
```

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" followup <agent_id> \
  "The button should look like this instead" \
  /path/to/screenshot.png
```

When the user attaches an image in the conversation, resolve its absolute file path and pass it as a trailing argument.

### Stop / Delete

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" stop <agent_id>
"$SKILL_DIR/scripts/cloud-agent.sh" delete <agent_id>
```

### Utility

```bash
"$SKILL_DIR/scripts/cloud-agent.sh" me       # API key info
"$SKILL_DIR/scripts/cloud-agent.sh" models   # available models
"$SKILL_DIR/scripts/cloud-agent.sh" repos    # accessible GitHub repos (rate-limited: 1/min)
```

## Pulling Agent Changes Locally

After an agent finishes (or while it's running), pull its changes into the local repo.

### Step 1: Get the agent's branch name

```bash
BRANCH=$("$SKILL_DIR/scripts/cloud-agent.sh" status <agent_id> | jq -r '.target.branchName')
```

### Step 2: Fetch and checkout

```bash
git fetch --all
git checkout "$BRANCH"
git pull origin "$BRANCH"
```

### Step 3: Cherry-pick onto current branch (alternative)

If the user wants to apply agent commits onto their current branch instead of switching:

```bash
git fetch --all
CURRENT=$(git branch --show-current)

# Find commits the agent made (commits on agent branch not on current)
COMMITS=$(git log --oneline "$CURRENT".."origin/$BRANCH" --reverse --format='%H')

for commit in $COMMITS; do
  git cherry-pick "$commit"
done
```

### Step 4: Merge (alternative)

```bash
git fetch --all
git merge "origin/$BRANCH"
```

### Step 5: Diff review

```bash
git fetch --all
git diff HEAD..."origin/$BRANCH"
```

## Workflow: Launch and Monitor

1. Launch the agent
2. Poll status every 15-30 seconds until `FINISHED` or `ERROR`
3. If `FINISHED`, show summary and ask user how to apply changes (checkout / cherry-pick / merge)
4. If `ERROR`, show conversation to diagnose

## Workflow: Review Running Agents

1. List agents, filter by `RUNNING` status
2. For each, show id, name, branch, time since creation
3. Offer to check conversation, send follow-up, or stop
