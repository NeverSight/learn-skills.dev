---
name: ai-news-briefing
description: Use when an agent needs a concise AI or ML news briefing from RSS sources, or must gather and rank daily AI news into a short list.
---

# AI News Briefing

## Overview
This skill aggregates AI-related RSS items and returns a ranked Top 10 plus markdown and JSON outputs.

## When to Use
- You need a daily AI or ML news briefing from multiple RSS sources.
- You need a ranked short list with summaries and sources.
- You need a ready-to-share markdown briefing.

## When Not to Use
- You need full articles or long-form summaries.
- You need real-time breaking news beyond RSS refresh rates.

## Quick Reference
- CLI: `python -m ai_news_skill --query "AI" --limit 100 --format markdown`
- Python: `from ai_news_skill.main import run_ai_news`
- Output keys: `query`, `total_candidates`, `returned_count`, `top10`, `ai_input`, `markdown`, `errors`
- `top10` fields: `title`, `summary`, `url`, `source`
- `limit` is per-source, not global

## Implementation

### CLI
```bash
python -m ai_news_skill --query "AI" --limit 100 --format markdown
python -m ai_news_skill --query "LLM safety" --limit 50 --format json
```

### Python API
```python
from ai_news_skill.main import run_ai_news

result = run_ai_news(query="AI", limit=100)
print(result["markdown"])
```

## Common Mistakes
| Mistake | Fix |
| --- | --- |
| Writing a `skill.json` instead of a root `SKILL.md` with frontmatter | Use `SKILL.md` at repo root with `name` and `description` frontmatter |
| Omitting the README install instructions for `npx skills add` | Add `npx skills add <owner>/<repo>` to README |
| Treating `limit` as a global limit instead of per-source | Treat `--limit` as a per-source cap |

## Red Flags
- No `SKILL.md` at repo root.
- README lacks install and usage examples.
