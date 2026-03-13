---
name: agent-transcript
description: Find and export agent chat session transcripts. Use when the user asks to export, save, find, or share a session transcript from any coding agent (Claude Code, Codex, Kiro, Cursor, Gemini CLI, etc.), wants to create an image of their conversation, or mentions agentpng.
allowed-tools: Bash Read Glob Grep
metadata:
  author: siegerts
  version: "1.0"
---

# Agent Transcript

Find and export chat session transcripts from coding agents. Supports Claude Code, Codex, Kiro, Cursor, Gemini CLI, Copilot CLI, and ChatGPT.

## How to export

When the user asks to export or find a session transcript, follow these steps:

1. Determine which agent produced the session (see transcript locations below)
2. Locate the transcript file on disk, or instruct the user how to export it from their IDE
3. Copy the file to a user-accessible location (e.g. Desktop or current directory)
4. Tell the user what they can do with it (e.g. share, archive, or use with [agentpng](https://agentpng.dev) to create a shareable image)

IMPORTANT: Always copy the raw transcript file. Do NOT reformat, summarize, truncate, or convert the content. Downstream tools expect the native format.

## Transcript locations by agent

### Claude Code

JSONL files at `~/.claude/projects/<project-path-hash>/<session-id>.jsonl`

Finding the current session:
- The session ID is `${CLAUDE_SESSION_ID}`
- List project directories: `ls ~/.claude/projects/`
- Find JSONL files: `find ~/.claude/projects/ -name "*.jsonl" -type f | head -20`
- Find the most recent session: `ls -t ~/.claude/projects/*//*.jsonl 2>/dev/null | head -5`

Copy the `.jsonl` file as-is.

### Codex (OpenAI)

JSONL files organized by date under `$CODEX_HOME/sessions/` (defaults to `~/.codex/sessions/`, or `%USERPROFILE%\.codex\sessions\` on Windows):

```
$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl
```

Example: `~/.codex/sessions/2026/03/07/rollout-2026-03-07T10-42-09-019cc8f6-963f-7b40-aa1e-3de0bec66698.jsonl`

Archived sessions are stored flat at `$CODEX_HOME/archived_sessions/`.

Finding the current session:
- There is no `$CODEX_SESSION_ID` env variable — use file timestamps and paths instead
- Session index: `$CODEX_HOME/history.jsonl` — each line has `session_id`, `ts`, and `text` (the user prompt)
- Find today's sessions: `ls -lt ~/.codex/sessions/$(date +%Y/%m/%d)/ 2>/dev/null`
- Find the most recent session across all dates: `find ~/.codex/sessions/ -name "rollout-*.jsonl" -type f -print0 | xargs -0 ls -t | head -5`
- Find sessions for a specific project by matching `cwd` in the first record: `head -1 <file> | grep "$(pwd)"`
- The first JSONL record is always `type: "session_meta"` containing `id`, `cwd`, `model_provider`, and `cli_version`

Copy the `.jsonl` file as-is.

### Gemini CLI

JSON or JSONL files at `~/.gemini/tmp/<project>/checkpoints/`

Copy the file as-is.

### Cursor

Requires in-app export. Tell the user: **Chat > ... (menu) > Export Chat**. This produces a `.md` file.

### Kiro

Requires in-app export. Tell the user: **Right-click the chat tab > Export Conversation**. This produces a `.md` file.

Kiro spec files can be copied directly from `.kiro/specs/<feature>/tasks.md`.

### ChatGPT

Requires a data export. Tell the user: **Settings > Data Controls > Export**. The export contains `conversations.json`.

### Copilot CLI

Copy terminal output directly. The format uses `User:` / `Copilot:` prefixes with `$` prompts.

### CLI terminal output (Claude Code, Codex, Kiro)

Raw terminal output can also be copied directly from Claude Code, Codex, or Kiro CLI sessions. The user selects and copies the full terminal text. Tools like agentpng auto-detect the CLI variant and parse the prompt markers, tool calls, and responses.

### Any other agent

If the user's agent isn't listed above, try these approaches in order:

1. **Check for session files on disk** — look in `~/.<agent-name>/` or `~/.config/<agent-name>/` for `.jsonl`, `.json`, `.md`, or `.log` files. Common patterns: `sessions/`, `history/`, `conversations/`, `logs/`
2. **Check for an in-app export** — most IDE-based agents have an export option in the chat or conversation menu
3. **Copy terminal output** — for CLI agents, the user can select and copy the full terminal text

If none of those produce a usable file, format the conversation as plain text with `User:` and `Assistant:` role prefixes separated by blank lines:

    User: What does this function do?

    Assistant: This function calculates the factorial of a number recursively.

This generic format is widely supported by transcript tools.

## Common file types

Transcript files are typically: `.jsonl`, `.json`, `.txt`, `.md`, `.log`

## Output instructions

When copying a transcript file for the user:

1. Use a clear filename like `session-export.jsonl` or keep the original name
2. Copy to the current working directory or Desktop
3. Confirm the file path and size
4. Suggest next steps: archive, share, or use with [agentpng](https://agentpng.dev) to turn it into a shareable image

For detailed format specifications per agent, see [formats.md](references/formats.md).
