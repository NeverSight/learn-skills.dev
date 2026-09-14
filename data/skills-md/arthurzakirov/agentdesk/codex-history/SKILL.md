---
name: codex-history
description: Access OpenAI Codex CLI conversation history to continue work started in Codex, or to find a past Codex chat by topic or keyword. Use when the user says "codex history", "continue from codex", "what was I doing in codex", "pick up from codex", "codex session", "find the codex chat about X", or wants to resume or locate a task that was started in Codex CLI.
---

# Codex History

Resume work started in OpenAI Codex CLI by reading its conversation history.

## Data Locations

There are two `history.jsonl` files and, depending on Codex version, session files or SQLite state:

| Source | Path | Content |
| --- | --- | --- |
| Global prompt index | `~/.codex/history.jsonl` | User prompts with `session_id` links |
| Per-project prompt index | `<project-root>/.codex/history.jsonl` | Same format, scoped to one repo |
| Session logs (legacy) | `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` | Full conversations |
| SQLite state | `~/.codex/state_5.sqlite` | Newer storage, may contain thread data |

Session files may not exist in newer versions, so prefer `history.jsonl` first and treat session JSONL as an optional richer source.

## Workflow

### Step 0: Search By Keyword

When the user describes the chat by topic rather than session ID, search prompt text across the global and per-project history files.

### Step 1: Search By Session ID

Check both global and per-project history files because the session may have started in another repo.

### Step 2: List Recent Sessions

If the user does not know which session they want, show recent prompts with timestamps and session IDs.

### Step 3: Try To Find A Session JSONL File

If a matching session log exists, use it for richer extraction. Do not fail the workflow if it does not exist.

### Step 4: Extract Conversation

- If a session JSONL exists, extract user and assistant messages plus relevant tool calls.
- If it does not, reconstruct the task flow from `history.jsonl` entries for the same `session_id`.

### Step 5: Pick Up The Work

After reading the history:

1. Summarize what Codex was working on.
2. Note incomplete steps or terminal errors.
3. Confirm what the user wants to continue.
4. Resume from the last useful state.

## Tips

- Session logs can be large, so extract rather than reading raw JSONL manually.
- `cwd` metadata is useful for locating the repo Codex worked in.
- If the user says "continue from codex" without specifics, start by showing recent sessions.
