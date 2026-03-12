---
name: openrouter-usage
description: "Track OpenRouter API spending — credit balance, per-model cost breakdown, and spending projections from OpenClaw session logs."
metadata: { "openclaw": { "emoji": "💰", "requires": { "bins": ["openrouter-usage"] } } }
---

# openrouter-usage

Track your OpenRouter spending directly from your OpenClaw agent. Shows credit balance, per-model cost/token breakdown, and spending projections.

## Trigger

Use when the user asks about OpenRouter credits, costs, spending, balance, usage, billing, or the `/usage` command.

## Commands

### Full report (recommended — combines everything)

```bash
openrouter-usage report              # credits + today's usage + projection
openrouter-usage report --week       # credits + last 7 days
openrouter-usage report --month      # credits + last 30 days
```

### Credit balance only

```bash
openrouter-usage credits
```

### Per-model breakdown only

```bash
openrouter-usage sessions --today
openrouter-usage sessions --week
openrouter-usage sessions --month
openrouter-usage sessions --date 2026-02-25
openrouter-usage sessions --from 2026-02-01 --to 2026-02-15
```

### Filtering and output

```bash
openrouter-usage report --agent main          # specific agent only
openrouter-usage report --format json         # JSON output
openrouter-usage sessions --today --utc       # use UTC instead of local timezone
```

## Notes

- API key auto-discovered from OpenClaw auth store or `OPENROUTER_API_KEY` env var.
- Session parsing is fully local — reads `~/.openclaw/agents/*/sessions/*.jsonl`.
- Date filters use local timezone by default. Pass `--utc` to override.
- Zero dependencies beyond Python 3 stdlib.
