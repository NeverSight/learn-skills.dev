---
name: skills-dashboard
description: Scrape skills.sh and generate an interactive HTML dashboard showing skill distribution by publisher, installs, and categories. Rerun anytime to get fresh data.
allowed-tools: Read Write Edit Bash WebFetch
---

# Skills Dashboard Generator

Scrape the [skills.sh](https://skills.sh/) registry and produce an interactive Plotly.js dashboard showing who publishes the most skills, who has the most installs, and how adoption is distributed.

## When to Use This Skill

- Generating a fresh snapshot of the skills.sh ecosystem
- Comparing publishers by skill count vs install count
- Exploring the power-law distribution of skill adoption
- Answering "who dominates the skills ecosystem?"

## How It Works

1. **Scrape** - Fetch `https://skills.sh/api/search` with broad 2-char queries to discover all skills
2. **Aggregate** - Group by owner (GitHub org/user) and repo, compute counts and totals
3. **Render** - Generate a self-contained HTML file with Plotly.js charts

## Running

Generate the dashboard with the scraper script:

```bash
python3 scripts/scrape_and_build.py
```

This writes `index.html` to the current directory.

To write to a specific path:

```bash
python3 scripts/scrape_and_build.py --output /path/to/dashboard.html
```

## Dashboard Contents

| Chart | What It Shows |
|-------|---------------|
| **Treemap** | Install share by publisher, click to drill into individual skills |
| **Bar: Skill Count** | Top 25 publishers by number of skills published |
| **Bar: Total Installs** | Top 25 publishers by total install volume |
| **Histogram** | Log-scale distribution showing the long tail of installs |
| **Top 30 Skills** | The 30 most-installed individual skills |

## Data Source

All data comes from the `skills.sh/api/search` endpoint. Each entry has:

```json
{
  "source": "owner/repo",
  "skillId": "skill-name",
  "name": "skill-name",
  "installs": 12345
}
```

## Generate It Yourself

**Install the skill:**

```bash
npx skills add olshansk/agent-skills
```

Select `skills-dashboard` when prompted.

**Then:**

1. Launch your agent CLI of choice (Claude Code, Codex, Gemini CLI, OpenCode)
2. Ask it to "build the skills ecosystem dashboard"

No API keys needed — the skill scrapes the public skills.sh registry and outputs a self-contained HTML file.
