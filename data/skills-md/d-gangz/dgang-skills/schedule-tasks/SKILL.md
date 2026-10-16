---
name: schedule-tasks
description: Create, list, delete, and analyze persistent Claude Desktop scheduled tasks. Use this skill when the user says "scheduled task", or wants to create, manage, or analyze a task that persists beyond the current session. Also trigger when the user wants to review or improve a scheduled task's prompt based on past run logs. Do NOT use this skill for session-scoped work like "create a recurring job", "remind me in 20 minutes", "check this every 5 min while I work", or any ephemeral in-session scheduling — those use the built-in CronCreate/CronList/CronDelete tools instead.
disable-model-invocation: true
---

# Claude Code Scheduled Tasks

Manage scheduled tasks that run Claude Code headlessly inside Claude Desktop on a cron schedule. Four operations: **create**, **list**, **delete**, and **analyze logs to improve prompts**.

All operations default to the current project directory (`$PWD`) as the target folder.

## Key Paths

- **SKILL.md prompts**: `~/.claude/scheduled-tasks/{task-name}/SKILL.md`
- **Schedule config**: `~/Library/Application Support/Claude/claude-code-sessions/{project-id}/{agent-session-id}/scheduled-tasks.json`
- **Session metadata**: Same directory as config, in `local_{run-id}.json` files
- **Session transcripts**: `~/.claude/projects/{project-hash}/{cli-session-id}.jsonl` (shared with regular CLI sessions)

## Operations

### 1. Create a Scheduled Task

Gather these from the user (use AskUserQuestion if anything is unclear):
- **Task name** (kebab-case, e.g. `daily-review`)
- **Description** (short, shown in Desktop UI)
- **Prompt** (the full instructions for what the task should do)
- **Cron expression** (in local timezone — remind the user of this)
- **Model** (default: `claude-opus-4-6`)

The project folder defaults to `$PWD`. Don't ask unless the user wants a different folder.

Run the bundled create script:

```bash
bash <skill-path>/scripts/create-scheduled-task.sh \
  "<name>" "<description>" "<prompt>" "<cron>" "<model>" "<folder>"
```

If the prompt is long or complex, write it to a temp file first and pass `@/path/to/file` as the prompt argument — the script handles this.

After creation, remind the user:
1. **Restart Claude Desktop** to load the new task.
2. **Click "Run Now" on the task in Claude Desktop**, then immediately stop the run. The task must be triggered manually at least once before the cron schedule will take effect — without this initial run, subsequent scheduled runs will not execute.

**Common cron expressions (local timezone):**
- `0 8 * * *` — daily at 8 AM
- `0 8 * * 1-5` — weekdays at 8 AM
- `30 23 * * *` — daily at 11:30 PM
- `0 9 * * 1` — every Monday at 9 AM
- `*/5 * * * *` — every 5 minutes (warn about API costs)

**SKILL.md writing tips** (share with user if they're drafting the prompt):
- Be self-contained — each run starts fresh with no prior context
- Write in second-person imperative ("Check the inbox...", "Run the test suite...")
- Include all file paths, tool names, and success criteria
- Think about what tools/skills the task will need access to

### 2. List Scheduled Tasks

Run the bundled list script:

```bash
bash <skill-path>/scripts/list-scheduled-tasks.sh
```

This auto-discovers all `scheduled-tasks.json` files in `claude-code-sessions/` and prints every task with its schedule, status, model, and last run time. If the user only cares about tasks for the current project, filter by checking `cwd` against `$PWD`.

### 3. Delete a Scheduled Task

First, list tasks for the current project so the user can confirm which one to delete. If multiple tasks exist, use AskUserQuestion to let them pick.

Run the bundled delete script:

```bash
bash <skill-path>/scripts/delete-scheduled-task.sh "<task-name>"
```

This removes the JSON entry, deletes the SKILL.md directory, and cleans up orphaned session metadata.

After deletion, remind the user: **Restart Claude Desktop to stop the scheduler.**

### 4. Analyze Logs and Improve a Scheduled Task Prompt

This is an autonomous analysis workflow. The goal is to read past session transcripts, identify problems, and directly fix the SKILL.md prompt.

**Step 1: Identify which task to analyze**

Find all `scheduled-tasks.json` files in `claude-code-sessions/` and filter for tasks whose `cwd` matches the current project (`$PWD`). If multiple tasks match, use AskUserQuestion to let the user pick which one.

Note the task's `id` and `filePath` (the SKILL.md location).

**Step 2: Find recent session logs**

Session metadata lives in the same directory as `scheduled-tasks.json`. Search `local_*.json` metadata files for the task's `scheduledTaskId`:

```
Grep: pattern="scheduledTaskId.*<task-id>", path="<base-dir>", glob="local_*.json"
```

Sort by modification time and pick the 3-5 most recent runs.

**Step 3: Read session metadata**

For each recent run, read the `local_{run-id}.json` file. Extract:
- `cliSessionId` — the key to find the transcript
- `scheduledTaskId` — confirms this is a scheduled task run
- `createdAt` / `lastActivityAt` — to understand timing
- `title` — to confirm it's the right task

**Step 4: Read conversation transcripts**

Claude Code scheduled task transcripts live in the standard CLI session location:
```
~/.claude/projects/{project-hash}/{cliSessionId}.jsonl
```

The `{project-hash}` is the project path with `/` replaced by `-` (e.g. `-Users-gang-gang-personal-kbos`).

Each line is a JSON object. Focus on:
- `"type":"assistant"` messages with `"type":"tool_use"` — what tools were called
- `"type":"assistant"` messages with `"type":"text"` — Claude's reasoning
- Error messages, retries, tool call failures
- Steps that seem wasteful or off-track

**Step 5: Check sub-agent logs if present**

Sub-agent transcripts are in:
```
~/.claude/projects/{project-hash}/{cliSessionId}/subagents/
```

Glob for `*.jsonl` files there and read any that exist.

**Step 6: Synthesize findings and fix the prompt**

After reading 3-5 recent transcripts, identify patterns:
- **Recurring errors** — the same tool call failing across runs
- **Wasted steps** — the task doing unnecessary work
- **Getting stuck** — loops, retries, confusion
- **Skipped steps** — parts of the prompt being ignored
- **Inconsistency** — works sometimes, fails other times

Then edit the SKILL.md directly at the path from Step 1. Apply these improvement patterns:

| Problem | Fix |
|---|---|
| Getting stuck or off-track | Add phase structure with checkpoints |
| Skipping steps | Add "do NOT stop until X is complete" guardrails |
| Using wrong tools | Add specific tool instructions |
| Taking too long | Reduce scope or split into sub-tasks |
| Sub-agents returning poor results | Add "Return a comprehensive report" preamble |
| Confused after skill/sub-agent completes | Add "When a skill completes, that is NOT the end of your task" |

Present a summary of findings and changes to the user. Include specific examples from the transcripts to justify each change.

**Note on SKILL.md changes:** Content changes take effect on the next run without restarting Claude Desktop — each run copies the SKILL.md fresh.
