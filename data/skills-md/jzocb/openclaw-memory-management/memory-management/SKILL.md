---
name: memory-management
description: |
  Manage AI agent memory with P0/P1/P2 priority system and auto-archival.
  Use when: setting up memory management, cleaning up MEMORY.md, creating
  lessons files, configuring auto-archive cron, or reviewing memory structure.
  Reduces token usage by 70-80% while maintaining recall via semantic search.
---

# Memory Management Skill

Manage agent memory efficiently using a three-layer architecture with automatic archival.

## Quick Setup

1. Format MEMORY.md with priority tags:
```markdown
- [P0] Core identity item (never expires)
- [P1][2026-02-10] Active project (90-day TTL)
- [P2][2026-02-10] Temporary item (30-day TTL)
```

2. Set up auto-archive cron:
```bash
0 4 * * * python3 ~/.openclaw/workspace/scripts/memory-janitor.py
```

3. Store lessons in `memory/lessons/*.jsonl`:
```json
{"id": "lesson-001", "date": "2026-02-10", "category": "infra", "title": "Problem title", "problem": "What happened", "solution": "How to fix", "tags": ["tag1"]}
```

## Three-Layer Architecture

**Layer 1: Hot Memory (MEMORY.md)**
- Always loaded, ≤200 lines
- P0: Core identity, never expires
- P1: Active projects, 90-day TTL  
- P2: Temporary, 30-day TTL

**Layer 2: Cold Memory (searchable)**
- `memory/lessons/*.jsonl` — structured lessons
- `memory/archive/` — expired content
- Use `memory_search` to recall

**Layer 3: Raw Logs**
- `memory/YYYY-MM-DD.md` — daily logs
- Not loaded automatically

## Priority Guidelines

| Priority | Use For | TTL |
|----------|---------|-----|
| P0 | User identity, preferences, safety rules | Never |
| P1 | Active projects, current strategies | 90 days |
| P2 | Debug notes, one-time events | 30 days |

## Core Principles (max 5 in AGENTS.md)

Keep only essential rules in AGENTS.md. Other lessons go to `lessons/*.jsonl`.

Example 5 rules:
1. Real money = correctness > speed
2. External actions require confirmation
3. Check both cron systems (system + OpenClaw)
4. Long-running processes need setsid isolation
5. Read platform rules before trading

## When Memory Gets Too Large

Run janitor with stats:
```bash
python3 scripts/memory-janitor.py --stats
```

If >200 lines:
1. Review P0 entries — are they all truly permanent?
2. Add dates to P1/P2 entries missing them
3. Move detailed content to `lessons/*.jsonl`
4. Run `--dry-run` then archive
