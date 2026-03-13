---
name: cc-history
description: Reference documentation for analyzing Claude Code conversation history files
---

# Claude Code History Analysis

Reference documentation for querying and analyzing Claude Code's conversation history. Use shell commands and jq to extract information from JSONL conversation files.

## Directory Structure

```
~/.claude/projects/{encoded-path}/
  |-- {session-uuid}.jsonl          # Main conversation
  |-- {session-uuid}/
      |-- subagents/
      |   |-- agent-{hash}.jsonl    # Subagent conversations
      |-- tool-results/             # Large tool outputs
```

## Project Path Resolution

Convert working directory to project directory:

```bash
PROJECT_DIR="~/.claude/projects/$(echo "$PWD" | sed 's|^/|-|; s|/\.|--|g; s|/|-|g')"
```

Encoding rules:

- Leading `/` becomes `-`
- Regular `/` becomes `-`
- `/.` (hidden directory) becomes `--`

Examples:

- `/Users/bill/.claude` -> `-Users-bill--claude`
- `/Users/bill/git/myproject` -> `-Users-bill-git-myproject`

## Message Types

| Type              | Description                                   |
| ----------------- | --------------------------------------------- |
| `user`            | User input messages                           |
| `assistant`       | Model responses (thinking, tool_use, text)    |
| `system`          | System messages                               |
| `queue-operation` | Background task notifications (subagent done) |

## Message Structure

Each line in a JSONL file is a message object:

```json
{
  "type": "assistant",
  "uuid": "abc123",
  "parentUuid": "xyz789",
  "timestamp": "2025-01-15T19:39:16.000Z",
  "sessionId": "session-uuid",
  "message": {
    "role": "assistant",
    "content": [...],
    "usage": {
      "input_tokens": 20000,
      "output_tokens": 500,
      "cache_read_input_tokens": 15000,
      "cache_creation_input_tokens": 5000
    }
  }
}
```

Assistant message content blocks:

- `type: "thinking"` - Model thinking (has `thinking` field)
- `type: "tool_use"` - Tool invocation (has `name`, `input` fields)
- `type: "text"` - Text response (has `text` field)

## Common Queries

### Find Conversations

```bash
# List by modification time (most recent first)
ls -lt "$PROJECT_DIR"/*.jsonl

# Find by date
ls -la "$PROJECT_DIR"/*.jsonl | grep "Jan 15"

# Find by content
grep -l "search term" "$PROJECT_DIR"/*.jsonl
```

### Extract Messages

```bash
# Get message by line number (1-indexed)
sed -n '42p' file.jsonl | jq .

# Get message by uuid
jq -c 'select(.uuid=="abc123")' file.jsonl

# All user messages
jq -c 'select(.type=="user")' file.jsonl

# All assistant messages
jq -c 'select(.type=="assistant")' file.jsonl
```

### Tool Call Analysis

```bash
# List all tool calls
jq -c 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | {name, input}' file.jsonl

# Count tool calls by name
jq -c 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use") | .name' file.jsonl | sort | uniq -c | sort -rn

# Find specific tool calls
jq -c 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Bash")' file.jsonl
```

### Skill Invocation Detection

Pattern: `python3 -m skills\.([a-z_]+)\.`

```bash
# Find all skill invocations
grep -oE "python3 -m skills\.[a-z_]+" file.jsonl | sort -u

# Find conversations using a specific skill
grep -l "python3 -m skills\.planner\." "$PROJECT_DIR"/*.jsonl
```

### Token Usage

```bash
# Total tokens in conversation
jq -s '[.[].message.usage? | select(.) | .input_tokens + .output_tokens] | add' file.jsonl

# Token breakdown
jq -s '[.[].message.usage? | select(.)] | {
  input: (map(.input_tokens) | add),
  output: (map(.output_tokens) | add),
  cached: (map(.cache_read_input_tokens // 0) | add)
}' file.jsonl

# Token progression over time
jq -c 'select(.type=="assistant") | {ts: .timestamp[11:19], inp: .message.usage.input_tokens, out: .message.usage.output_tokens}' file.jsonl
```

### Taxonomy Aggregation

```bash
# Count messages by type
jq -s 'group_by(.type) | map({type: .[0].type, count: length})' file.jsonl

# Character count in user messages
jq -s '[.[] | select(.type=="user") | .message.content | length] | add' file.jsonl

# Thinking block character count
jq -s '[.[] | select(.type=="assistant") | .message.content[]? | select(.type=="thinking") | .thinking | length] | add' file.jsonl
```

### Subagent Analysis

```bash
# List subagents for a session
ls "${SESSION_DIR}/subagents/"

# Get subagent task description (first user message)
jq -c 'select(.type=="user") | .message.content' agent-*.jsonl | head -1

# Find Task tool calls in parent (these spawn subagents)
jq -c 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Task") | .input' file.jsonl
```

## Correlation

Subagent files (`agent-{hash}.jsonl`) don't link directly to parent Task calls. To correlate:

1. List all subagent files under `{session}/subagents/`
2. Read first user message of each for task description
3. Match description to Task tool_use blocks in parent conversation
