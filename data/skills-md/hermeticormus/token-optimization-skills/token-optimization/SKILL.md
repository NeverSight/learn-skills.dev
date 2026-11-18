---
name: token-optimization
description: Claude Code token optimization — CLAUDE_AUTOCOMPACT_PCT_OVERRIDE, MAX_THINKING_TOKENS, behavioral patterns for selective reads, grep-first discovery, and cache awareness. Use to reduce cost on multi-day projects or recurring sessions.
license: MIT
---

# Token optimization

## Two env vars

```bash
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70
export MAX_THINKING_TOKENS=16000
```

## Patterns

- Read with offset/limit, not whole files
- Grep before Read
- Compact at phase transitions
- Don't leave prompts cold > 5min (cache TTL)
- Separate sessions: routine vs. complex

## When to raise thinking budget

Architecture, debugging, refactoring, critical review.

## When to lower

File ops, lint fixes, trivial edits, lookups.

---

Full content at https://github.com/HermeticOrmus/token-optimization-skills.
