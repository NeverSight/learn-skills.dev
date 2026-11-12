---
name: claude-mem
description: Persistent memory compression system for Claude Code and AI coding agents. Compresses conversation transcripts, knowledge graphs, and project context into compact memory snapshots that survive across sessions. Use when you want Claude Code to remember previous work, decisions, and context without re-loading full conversation history. Features transcript-based compression, multi-agent memory sharing, team cowork sessions, and cross-tool support (Cursor, Grok, Windsurf, OMP, Hermes, Pi, and more).
---

# Claude-Mem

Persistent memory compression system built for Claude Code.

## What It Does

Claude-Mem compresses conversation transcripts and project context into compact memory snapshots that persist across sessions, enabling:

- **Cross-session memory:** Claude remembers what was done in previous sessions without manually re-loading context
- **Knowledge graph compression:** Project knowledge is distilled into structured memory entries
- **Team cowork:** Share memory across multiple agents working on the same project
- **Multi-tool support:** Works with Claude Code, Cursor, Grok Bot, Windsurf, OMP, Hermes, Pi, and more

## Installation

```bash
npx claude-mem install
```

Or via the Claude Code plugin marketplace:
```bash
/plugin marketplace add thedotmack/claude-mem
```

## How It Works

1. **Compress:** At the end of a session, Claude-Mem analyzes the conversation transcript and extracts key decisions, code changes, and context
2. **Store:** Compressed memory is stored as structured YAML/JSON in your project's `.claude-mem/` directory
3. **Load:** On the next session start, memory is loaded and injected into Claude's context window
4. **Cowork:** Multiple agents can read and write to the shared memory store

## Commands

```
/mem compress          # Compress current session into memory
/mem load              # Load project memory at session start
/mem status            # Show what's in memory
/mem search <query>    # Search memory for specific information
/mem forget <topic>    # Remove memory entries
/mem cowork            # Enable multi-agent memory sharing
```

## Configuration

Memory is stored in `.claude-mem/` in your project root (add to `.gitignore` if private). Configure in `.claude-mem/config.json`:

```json
{
  "compression": "aggressive",
  "max_entries": 100,
  "include": ["decisions", "code_changes", "context"],
  "cowork": false
}
```

## Reference

- **Source:** [github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
- **License:** Apache 2.0
