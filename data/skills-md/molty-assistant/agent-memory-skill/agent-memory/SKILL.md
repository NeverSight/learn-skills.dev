---
name: agent-memory
version: 1.0.0
description: Memory management for AI agents - list, search, summarize, and maintain your memory files. Includes AI-powered digest.
homepage: https://github.com/molty-assistant/agent-memory
metadata: {"openclaw":{"emoji":"🧠","category":"productivity","requires":{"bins":["node"]}}}
---

# Agent Memory (memctl)

Memory management CLI for AI agents. Organize, search, and maintain your memory files.

## Install

```bash
npm install -g agent-memory
```

Or clone and build:
```bash
git clone https://github.com/molty-assistant/agent-memory.git
cd agent-memory && npm install && npm run build
```

## Commands

### List memory files
```bash
memctl list              # List all
memctl ls --recent 5     # Show recent
```

### Search across files
```bash
memctl search "query"              # Find mentions
memctl s "project" --context 3     # With context lines
```

### Summary stats
```bash
memctl summary           # Last 7 days stats
memctl sum --days 30     # Last 30 days
```

### Check for gaps
```bash
memctl gaps              # Missing daily entries (30 days)
memctl gaps --days 7     # Check last week
```

### Create today's file
```bash
memctl touch             # Creates YYYY-MM-DD.md if missing
```

### AI-powered digest (requires Gemini API key)
```bash
export GEMINI_API_KEY=your_key
memctl digest            # AI summary of last 7 days
memctl ai --days 3       # Last 3 days
memctl digest -o out.md  # Save to file
```

## Configuration

Memory directory is found automatically:
1. `$MEMORY_DIR` environment variable
2. `./memory` in current directory
3. `~/.openclaw/workspace/memory`

## Use Cases

**Daily check:**
```bash
memctl gaps --days 7 && memctl touch
```

**Weekly review:**
```bash
memctl digest --days 7 -o weekly-digest.md
```

**Find context:**
```bash
memctl search "project name"
```

## Integration

Add to your `HEARTBEAT.md`:
```markdown
## Memory Maintenance
- `memctl gaps` to check for missing entries
- `memctl touch` to create today's file
- `memctl digest` for weekly AI summary
```
