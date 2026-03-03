---
name: performance-optimization
description: Best practices for Claude Code performance optimization, context management, storage cleanup, and troubleshooting slowdowns
allowed-tools: Read, Bash, Glob, Grep
---

# Performance Optimization Skill

Comprehensive guidance for optimizing Claude Code performance. This skill covers storage management, context window optimization, and troubleshooting common performance issues.

## When to Use This Skill

**Keywords:** slow, performance, lag, storage, cleanup, cache, context, compact, clear, sessions, agents, bloat, optimization, speed

**Use this skill when:**

- Claude Code is running slowly
- Storage is accumulating
- Context window is getting full
- Planning performance maintenance
- Learning best practices for efficient usage

## Quick Reference

### Immediate Actions for Slowdowns

| Symptom | Quick Fix | Command |
|---------|-----------|---------|
| General slowness | Clean storage | `/cleanup-sessions 7` |
| Input lag | Reset context | `/clear` |
| API errors | Check status | `/check-api-status` |
| Unknown cause | Full diagnostic | `/diagnose-performance` |

### Performance Commands

| Command | Purpose |
|---------|---------|
| `/user-config storage` | Analyze storage usage |
| `/user-config cleanup-sessions [days]` | Remove old session files |
| `/user-config cleanup-agents [days]` | Remove old agent files |
| `/user-config prune-cache [days]` | Comprehensive cleanup |
| `/diagnose-performance` | Full diagnostic |
| `/list sessions` | View recent sessions |
| `/user-config session-stats` | Session statistics |
| `/check-api-status` | API status check |
| `/check-context` | Context window analysis |

## Core Concepts

### 1. Storage Management

Claude Code stores conversation history in `~/.claude/`:

```text
~/.claude/
├── projects/           # Session history (can grow large!)
│   └── {project-hash}/
│       ├── {session-id}.jsonl     # Conversation transcripts
│       └── agent-{id}.jsonl       # Subagent transcripts
├── todos/              # Todo state
├── statsig/            # Analytics cache
└── history.jsonl       # Command history
```

**Key insight:** The `projects/` folder grows indefinitely with usage. Heavy users can accumulate 1GB+ of session data.

**See:** `references/storage-management.md` for detailed guidance.

### 2. Context Window Management

Claude Code uses a 200K token context window. Performance degrades as it fills:

| Usage | Status | Action |
|-------|--------|--------|
| < 50% | Healthy | No action |
| 50-75% | Monitor | Consider compacting |
| 75-85% | Warning | Run /compact or /clear |
| > 85% | Critical | Immediate action |

**Key commands:**

- `/clear` - Complete context reset
- `/compact` - Intelligent summarization
- `/cost` - View token usage

**See:** `references/context-management.md` for detailed guidance.

### 3. Known Issues

Several GitHub issues document known performance problems:

> **Note:** Issue numbers below are point-in-time references and may have been closed,
> merged, or superseded. For current issues, spawn the `claude-code-issue-researcher`
> agent or query `docs-management: "performance issues"` for updated tracking.

| Issue | Description | Workaround |
|-------|-------------|------------|
| #10881 | Performance degrades in long sessions | Restart periodically |
| #14552 | Input lag at high context | Use /clear at 75% |
| #14476 | Regression even at 30k tokens | Update to latest version |
| #1497 | Keyboard responsiveness issues | Restart Claude Code |

**See:** `references/known-issues.md` for detailed tracking.

## Best Practices

### Daily Maintenance

1. **Start fresh when possible** - New session = fresh context
2. **Use /clear between major tasks** - Don't let context rot
3. **Monitor storage periodically** - Run `/check-claude-storage` weekly

### Heavy Usage Patterns

1. **Use subagents for large operations** - Isolates context bloat
2. **Break large tasks into sessions** - Smaller = faster
3. **Clean storage weekly** - `/cleanup-sessions 7`

### Performance Optimization

1. **Keep CLAUDE.md lean** - Large memory files slow startup
2. **Use progressive disclosure** - Load context on-demand
3. **Prefer focused queries** - Specific > broad

## Troubleshooting Flowchart

```text
Claude Code is slow
        │
        ├─> Check storage: /check-claude-storage
        │   └─> If >500MB: /cleanup-sessions 7
        │
        ├─> Check context: /check-context
        │   └─> If WARNING+: /clear or /compact
        │
        ├─> Check API: /check-api-status
        │   └─> If degraded: Wait or reduce load
        │
        └─> Full diagnostic: /diagnose-performance
            └─> Follow recommendations
```

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `docs-management` | For official Claude Code documentation |
| `memory-management` | For CLAUDE.md optimization |

## References

Load these for detailed guidance:

- `references/context-management.md` - Context window optimization
- `references/storage-management.md` - Storage cleanup strategies
- `references/known-issues.md` - GitHub issues and workarounds

## Version History

- **v1.0.0** (2025-12-26): Initial release
  - Core performance guidance
  - Command reference
  - Best practices
  - Reference documents

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
