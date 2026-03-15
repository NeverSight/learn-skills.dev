---
name: session-export
description: Exports the current AI chat session to a Markdown file. Use this skill when the user wants to export, save, sync, or backup their conversation/chat/session content. Supports both raw export and optional summarization.
license: Apache-2.0
metadata:
  author: crossoverJie
  version: "1.0"
---

# Session Export Skill

Exports AI chat session conversations to readable Markdown files. Supports two modes for cross-agent compatibility.

## Prerequisites

- **Python 3** (standard library only, no external dependencies)

## Usage

### Mode 1: Claude Code Log Export (Preferred)

When running inside Claude Code, the script reads the full JSONL session logs for complete, accurate export (including messages that may have been compressed from context).

```bash
python3 skills/session-export/session_export.py --output-dir <directory> [options]
```

#### Options

- `--output-dir`: Directory to save the exported markdown (env: `SESSION_EXPORT_OUTPUT_DIR`, default: current directory)
- `--cwd`: Project working directory to locate session logs (default: current directory)
- `--session-id`: Export a specific session ID (default: most recent)
- `--name`: Custom filename for the exported markdown (without .md extension). AI should summarize the session topic as the name
- `--summarize`: Request a summary to be generated after export
- `--no-subagents`: Exclude subagent conversations
- `--max-tool-output`: Max characters per tool output in export (default: 5000)

#### Examples

**Export current session:**
```bash
python3 skills/session-export/session_export.py --output-dir /tmp/sessions
```

**Export a specific session:**
```bash
python3 skills/session-export/session_export.py --session-id abc12345-... --output-dir ~/exports
```

**Export without subagent conversations:**
```bash
python3 skills/session-export/session_export.py --output-dir ./exports --no-subagents
```

**Export with summary:**
```bash
python3 skills/session-export/session_export.py --output-dir ./exports --summarize
```

### Mode 2: AI Fallback Export

When the script exits with code **2** (Claude Code logs not found), the AI should fall back to writing the conversation directly from its current context:

1. Create a markdown file in the specified output directory using the same format:
   - YAML frontmatter with `session_id`, `project`, `exported_at`, `message_count`, `export_mode: ai-context`
   - Each message as `## User` / `## Assistant` with timestamps if available
   - File named `session-fallback-<YYYY-MM-DD-HHMMSS>.md`
2. Write each message from the current conversation context verbatim
3. Note: messages compressed from context earlier in the conversation may be lost in this mode

### Summarize Mode

When `--summarize` is passed:

- **Claude Code mode**: After the script exports the raw conversation, read the exported file and generate a concise summary saved as `*-summary.md` alongside the original
- **Fallback mode**: After writing the raw conversation, generate the summary file

The summary should include:
- Key topics discussed
- Decisions made
- Code changes performed
- Outstanding issues or follow-ups

## Output

**Success (exit code 0):**
```
Exported to: /tmp/sessions/session-1e2b749d-2026-02-06-210100.md
Session: 1e2b749d-f2c1-4a91-b248-6331e48abd6a
Messages: 42
Subagents: 3
```

**Fallback needed (exit code 2):**
```
Claude Code log directory not found (~/.claude/projects/).
FALLBACK_MODE: AI should write conversation from context directly.
```
