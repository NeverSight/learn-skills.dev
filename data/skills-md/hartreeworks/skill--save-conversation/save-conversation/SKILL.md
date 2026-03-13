---
name: save-conversation
description: This skill should be used when the user asks to "save this conversation", "save conversation", "export conversation", "save our chat", "create a transcript", or mentions wanting to share or archive the current conversation. Exports Claude Code conversations to readable markdown files.
---

# Save conversation

Export the current Claude Code conversation to a clean, readable markdown file.

## How it works

Claude Code automatically stores conversation history in `.jsonl` files at `~/.claude/projects/[project-folder]/[session-id].jsonl`. This skill parses those logs and transforms them into nicely formatted markdown.

## Usage

When the user invokes this skill:

1. Identify the current session ID and project folder path
2. Run the export script with appropriate arguments
3. Report the saved file path to the user

### Basic invocation

```bash
python3 ~/.claude/skills/save-conversation/scripts/export.py \
  --session-id SESSION_UUID \
  --project-path PROJECT_FOLDER_NAME \
  --topic "optional-topic-slug"
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--session-id` | Yes | The current session UUID |
| `--project-path` | Yes | The encoded project folder name (e.g., `-Users-ph--claude-skills`) |
| `--topic` | No | Topic slug for filename; defaults to session slug from the log |

### Finding the arguments

**Session ID**: Available from the conversation context. Look for the `sessionId` field in the conversation or check the most recently modified `.jsonl` file in the project folder.

**Project path**: Derived from the current working directory by replacing `/` with `-` and prefixing with `-`. For example:
- `/Users/ph/.claude/skills` → `-Users-ph--claude-skills`

## Output format

The script produces a markdown file with this structure:

```markdown
# Conversation: {topic}

**Date:** YYYY-MM-DD HH:MM
**Session:** {session-id}

---

## User

{user message content}

---

## Claude

{assistant response}

> Used tool: ToolName

---

## User

{next user message}

...
```

### What gets included

- **User messages**: Full text content
- **Assistant text responses**: All prose/explanation content
- **Tool usage**: Single-line summaries (e.g., `> Used tool: Bash`)

### What gets excluded

- Thinking blocks (internal reasoning)
- Tool outputs (keeps transcript clean)
- File history snapshots (internal state)
- Raw JSON metadata

## Output location

Saved files go to:
```
~/.claude/skills/save-conversation/transcripts/YYYY-MM-DD-{topic}.md
```

## Workflow

To save the current conversation:

1. Note the session ID from context (or find via `ls -lt ~/.claude/projects/[project-path]/*.jsonl | head -1`)
2. Determine the project path from the current working directory
3. Run the export script
4. Confirm the file was saved and report the path

### Example

```bash
# For a conversation in /Users/ph/.claude/skills with session 50e09818-de5f-4fa8-8769-92f3ea6f974c
python3 ~/.claude/skills/save-conversation/scripts/export.py \
  --session-id "50e09818-de5f-4fa8-8769-92f3ea6f974c" \
  --project-path "-Users-ph--claude-skills" \
  --topic "save-conversation-skill"
```

## Scripts

### `scripts/export.py`

Main export script. Parses `.jsonl` conversation logs and outputs clean markdown.

Features:
- Extracts user messages and assistant text responses
- Summarises tool usage without verbose output
- Skips thinking blocks and internal metadata
- Generates timestamped filenames with topic slugs
- Creates the transcripts directory if needed
