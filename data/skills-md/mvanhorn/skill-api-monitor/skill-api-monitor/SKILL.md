---
name: skill-api-monitor
description: Monitor APIs used by your Moltbot/Clawdbot skills and recommend updates when new features are released.
metadata:
  moltbot:
    emoji: "🔍"
---

# Skill API Monitor 🔍

Automatically checks the APIs behind your Moltbot skills for new features and recommends updates.

Works for **any GitHub user** - just pass your username.

## Quick Start

```bash
# Interactive setup (first time)
python3 {baseDir}/scripts/check.py --setup

# Or specify your GitHub username directly
python3 {baseDir}/scripts/check.py --github-user YOUR_USERNAME --discover
```

The `--setup` command will:
1. Ask for your GitHub username
2. Discover your public Moltbot/Clawdbot skills
3. Show which APIs were detected
4. Optionally save your username for future runs

## Usage

```bash
# Discover your public skills
python3 {baseDir}/scripts/check.py --github-user YOUR_USERNAME --discover

# Full check with 7-day lookback
python3 {baseDir}/scripts/check.py --github-user YOUR_USERNAME --days 7

# After setup, you can omit --github-user
python3 {baseDir}/scripts/check.py --days 7
```

## What it does

1. **Discovers** your public Moltbot/Clawdbot skills from GitHub
   - Matches `moltbot-skill-*`, `clawdbot-skill-*` repos
   - Also detects repos with SKILL.md containing Moltbot metadata
   
2. **Auto-detects** which API each skill uses by reading SKILL.md
   - Parallel.ai, Supabase, Tesla, xAI, Remotion, etc.
   - Pattern matching against 15+ known APIs
   
3. **Scans** changelogs and docs for recent updates
   - Looks for recent dates (last N days)
   - Finds keywords: API, feature, update, release, etc.
   
4. **Reports** recommendations
   - "Parallel.ai has updates - review for skill enhancement"

## Options

| Flag | Description |
|------|-------------|
| `--github-user`, `-u` | **Required**: Your GitHub username |
| `--days`, `-d` | Days to look back (default: 7) |
| `--discover` | Just list skills without checking APIs |
| `--dry-run` | Same as --discover |
| `--include-x` | Also search X/Twitter (slower) |
| `--skill`, `-s` | Check specific skill only |
| `--json`, `-j` | Output as JSON |

## Supported APIs (auto-detected)

The skill auto-detects these APIs from your SKILL.md content:

| API | Detection Keywords | Changelog URL |
|-----|-------------------|---------------|
| Parallel.ai | parallel.ai, parallel | parallel.ai/blog |
| Supabase | supabase | supabase.com/changelog |
| Tesla | tesla, fleet api | developer.tesla.com |
| xAI/Grok | x.ai, xai, grok | docs.x.ai |
| Remotion | remotion | remotion.dev/changelog |
| Google Gemini | gemini, ai.google | ai.google.dev |
| Polymarket | polymarket, gamma | docs.polymarket.com |
| Spotify | spotify | developer.spotify.com |
| Manus | manus | manus.ai |
| And more... | | |

## Example Output

```
📊 SKILL API MONITOR REPORT
   User: yourname
   Date: 2026-01-28
   Lookback: 7 days

🔔 parallel (Parallel.ai)
   [Changelog/Blog] Recent update (January 28, 2026): New authenticated page access...
   💡 Review Parallel.ai updates - potential skill enhancement

🔔 supabase (Supabase)
   [Changelog/Blog] Recent update (Jan 26, 2026): New realtime features...
   💡 Review Supabase updates

✅ No updates: polymarket, tesla, xai

📈 Checked 9 skills
```

## Adding API Detection Patterns

Edit `scripts/skill_apis.json` to add new API patterns:

```json
{
  "my-api": {
    "name": "My API",
    "docs": "https://docs.my-api.com",
    "changelog": "https://my-api.com/changelog",
    "twitter": "@myapi"
  }
}
```

## Automatic Weekly Checks

This skill doesn't run automatically - you set up your own schedule.

### Moltbot Cron (Recommended)

Ask your agent:
> "Set up a weekly cron to run skill-api-monitor every Sunday"

### System Cron

```bash
# crontab -e
0 10 * * 0 python3 /path/to/check.py --github-user YOUR_USERNAME --days 7
```

### Manual

```bash
python3 {baseDir}/scripts/check.py --github-user YOUR_USERNAME --days 7
```

## Requirements

- `gh` CLI (GitHub CLI) - for discovering repos
- Python 3.10+
- `curl` - for fetching changelogs

## Environment Variables

- `SKILL_API_MONITOR_USER` - Default GitHub username (optional)
