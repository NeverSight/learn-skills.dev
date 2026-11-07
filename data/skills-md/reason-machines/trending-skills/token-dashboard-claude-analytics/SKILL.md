---
name: token-dashboard-claude-analytics
description: Local token cost analytics dashboard for Claude Code sessions — reads JSONL transcripts and provides per-prompt cost breakdowns, heatmaps, and usage insights.
triggers:
  - show me my Claude Code token usage
  - analyze my Claude Code costs
  - set up token dashboard for Claude
  - track how much I'm spending on Claude Code
  - visualize Claude Code session costs
  - find expensive prompts in Claude Code
  - monitor token usage across projects
  - install token dashboard locally
---

# Token Dashboard — Claude Code Analytics

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Token Dashboard reads the JSONL transcripts Claude Code writes to `~/.claude/projects/` and turns them into per-prompt cost analytics, tool/file heatmaps, cache analytics, project comparisons, and a rule-based tips engine. Everything runs locally — no data leaves your machine.

## Installation

```bash
git clone https://github.com/nateherkai/token-dashboard.git
cd token-dashboard
python3 cli.py dashboard
```

No `pip install`. No Node.js. No build step. Requires Python 3.8+.

**Windows:**
```bash
git clone https://github.com/nateherkai/token-dashboard.git
cd token-dashboard
py -3 cli.py dashboard
```

## Key CLI Commands

```bash
# Start the full dashboard UI at http://127.0.0.1:8080
python3 cli.py dashboard

# Populate/refresh the SQLite cache, then exit
python3 cli.py scan

# Print today's totals in the terminal
python3 cli.py today

# Print all-time totals in the terminal
python3 cli.py stats

# Show active optimization tips in terminal
python3 cli.py tips

# Dashboard with options
python3 cli.py dashboard --no-open    # don't auto-open browser
python3 cli.py dashboard --no-scan    # skip initial scan, use cached DB only
python3 cli.py dashboard --projects-dir /path/to/projects --db /path/to/cache.db
```

## Configuration

### Environment Variables

```bash
# Change port (default: 8080)
PORT=9000 python3 cli.py dashboard

# Change bind address (WARNING: keep 127.0.0.1 — 0.0.0.0 exposes data on network)
HOST=127.0.0.1 python3 cli.py dashboard

# Custom projects directory
CLAUDE_PROJECTS_DIR=/custom/path python3 cli.py dashboard

# Custom SQLite cache location
TOKEN_DASHBOARD_DB=/custom/path/cache.db python3 cli.py dashboard
```

### Pricing Configuration

Edit `pricing.json` directly to update model prices or add plans:

```json
{
  "models": {
    "claude-opus-4-5": {
      "input": 15.00,
      "output": 75.00,
      "cache_write": 18.75,
      "cache_read": 1.50
    }
  },
  "plans": {
    "api": { "label": "API", "multiplier": 1.0 },
    "pro": { "label": "Pro ($20/mo)", "multiplier": 0.0 },
    "max": { "label": "Max ($100/mo)", "multiplier": 0.0 }
  }
}
```

## Data Sources

Claude Code writes session JSONL files here:

| OS | Path |
|---|---|
| macOS / Linux | `~/.claude/projects/<project-slug>/<session-id>.jsonl` |
| Windows | `C:\Users\<you>\.claude\projects\<project-slug>\<session-id>.jsonl` |

The dashboard only reads these files — never modifies them. It caches results in SQLite at `~/.claude/token-dashboard.db`.

## Dashboard Tabs

| Tab | What it shows |
|---|---|
| **Overview** | All-time totals, daily charts, cost by plan, top tools, recent sessions |
| **Prompts** | Most expensive user prompts ranked by tokens; click to see tool calls and result sizes |
| **Sessions** | Turn-by-turn view with per-turn tokens and tool calls |
| **Projects** | Per-project comparison: tokens, sessions, files touched |
| **Skills** | Most-invoked skills and their token costs |
| **Tips** | Rule-based suggestions (repeated file reads, oversized tool results, low cache-hit rate) |
| **Settings** | Switch between API / Pro / Max pricing plans |

## API Endpoints

The dashboard exposes JSON endpoints at `http://127.0.0.1:8080/api/`:

```bash
# Overview stats
curl http://127.0.0.1:8080/api/overview

# Most expensive prompts
curl http://127.0.0.1:8080/api/prompts

# Session list
curl http://127.0.0.1:8080/api/sessions

# Single session detail
curl http://127.0.0.1:8080/api/sessions/<session-id>

# Project comparison
curl http://127.0.0.1:8080/api/projects

# Optimization tips
curl http://127.0.0.1:8080/api/tips
```

## Real Code Examples

### Scripting Against the SQLite Cache

After running `python3 cli.py scan`, query the cache directly:

```python
import sqlite3
import os

db_path = os.path.expanduser("~/.claude/token-dashboard.db")
conn = sqlite3.connect(db_path)

# Get top 10 most expensive prompts
cursor = conn.execute("""
    SELECT
        project_slug,
        session_id,
        input_tokens,
        output_tokens,
        cache_read_tokens,
        cost_usd,
        substr(user_text, 1, 80) as prompt_preview
    FROM turns
    ORDER BY cost_usd DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"${row[5]:.4f} | {row[0]} | {row[6]}")

conn.close()
```

### Get Daily Token Totals

```python
import sqlite3
import os

db_path = os.path.expanduser("~/.claude/token-dashboard.db")
conn = sqlite3.connect(db_path)

cursor = conn.execute("""
    SELECT
        date(created_at) as day,
        SUM(input_tokens) as total_input,
        SUM(output_tokens) as total_output,
        SUM(cache_read_tokens) as total_cache_read,
        SUM(cost_usd) as total_cost
    FROM turns
    GROUP BY date(created_at)
    ORDER BY day DESC
    LIMIT 30
""")

for row in cursor.fetchall():
    print(f"{row[0]}: ${row[4]:.4f} ({row[1]} in, {row[2]} out, {row[3]} cached)")

conn.close()
```

### Programmatic Scan via Python

```python
import sys
import os

# Add the project root to path
sys.path.insert(0, '/path/to/token-dashboard')

from token_dashboard.scanner import Scanner

projects_dir = os.path.expanduser("~/.claude/projects")
db_path = os.path.expanduser("~/.claude/token-dashboard.db")

scanner = Scanner(projects_dir=projects_dir, db_path=db_path)
scanner.scan()
print("Scan complete")
```

### Fetch Overview Stats Programmatically

```python
import urllib.request
import json

# Requires dashboard to be running: python3 cli.py dashboard --no-open
with urllib.request.urlopen("http://127.0.0.1:8080/api/overview") as resp:
    data = json.loads(resp.read())

print(f"Total sessions: {data['total_sessions']}")
print(f"Total cost (API): ${data['total_cost_usd']:.2f}")
print(f"Cache hit rate: {data['cache_hit_rate']:.1%}")
```

## Common Patterns

### Reset and Rebuild the Cache

```bash
rm ~/.claude/token-dashboard.db
python3 cli.py scan
```

### Run on a Different Port to Avoid Conflicts

```bash
PORT=9090 python3 cli.py dashboard
```

### Export Tips to File

```bash
python3 cli.py tips > optimization-tips.txt
```

### Automate Daily Stats Logging

```bash
# Add to crontab: 0 9 * * * /path/to/daily-stats.sh
cd /path/to/token-dashboard && python3 cli.py today >> ~/claude-usage-log.txt
```

### Point at a Different Projects Directory

```bash
# If Claude Code projects are in a non-standard location
python3 cli.py dashboard --projects-dir ~/work/.claude/projects
```

## Troubleshooting

| Problem | Solution |
|---|---|
| "No data" / empty charts | Run `python3 cli.py scan` then reload |
| Port 8080 in use | `PORT=9000 python3 cli.py dashboard` |
| Numbers stuck/wrong | Delete `~/.claude/token-dashboard.db`, re-run `python3 cli.py scan` |
| Two instances running | Stop all instances first — they fight over the SQLite DB |
| `python3` not found on Windows | Use `py -3` instead |
| No sessions found | Ensure Claude Code has been used and files exist in `~/.claude/projects/` |

## Architecture Overview

```
cli.py
  └─► token_dashboard/scanner.py   # reads JSONL, dedupes by message.id, writes SQLite
  └─► token_dashboard/server.py    # serves /api/* JSON routes + web/ static files
        └─► web/                   # vanilla JS + vendored ECharts, no build step
pricing.json                       # editable model/plan pricing
~/.claude/token-dashboard.db       # SQLite cache (auto-created)
```

**Deduplication note:** Claude Code writes each assistant response 2–3 times during streaming. The scanner dedupes by `message.id` so tallies match actual API billing — expect lower numbers than tools that sum every raw JSONL row.
