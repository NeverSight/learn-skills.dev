---
name: session-search
description: Recover prior Feynman work from session transcripts. Use the optional /search command only when it is installed and visible; otherwise search local session JSONL files directly.
---

# Session Search

Use the `/search` command to search prior Feynman sessions interactively only when the optional session-search package is installed and the command is visible. Otherwise, search session JSONL files directly via bash.

## Interactive search

```
/search <query>
```

Opens the session search UI when the optional package is loaded. Supports `resume <sessionPath>` to continue a found session.

## Direct file search

Session transcripts are stored as JSONL files in `~/.feynman/sessions/`. Each line is a JSON record with `type` (session, message, model_change) and `message.content` fields.

```bash
grep -ril "scaling laws" ~/.feynman/sessions/
```

For structured search across sessions, use the interactive `/search` command when it is visible. If it is unavailable, direct file search is the supported fallback.
