---
name: what-did-i-get-done
description: Summarize authored git commits over a time period into a concise status update. Use when preparing weekly reviews, retrospectives, shipped-work recaps, or any requested date range.
---

## Workflow

1. Resolve concrete date range.
2. Read commits by current git user email in range.
3. Exclude merges and uncommitted work.
4. Synthesize important shipped changes.
5. State actual range.

Be concise and dense. Prioritize substantial behavior/architecture; omit formatting/import/minor rename. Never infer motive; describe functionally.

Output one short status summary, real range, optional 2-5 major bullets. Weekly/retro adds brief likely bug-fix/tech-debt/net-new classification.
