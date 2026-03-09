---
name: rss-automation
description: "RSS feed aggregation and monitoring. Parse RSS/Atom feeds, filter entries, track new items, and integrate with notification channels for automated content monitoring."
---

# RSS Automation

Monitor and aggregate RSS/Atom feeds for automated content tracking and notification.

## Capabilities

- Parse RSS 2.0 and Atom feeds
- Filter entries by keywords, date, author
- Track seen/new entries to avoid duplicates
- Push new items to Telegram, Slack, or other channels
- Schedule periodic feed checks via cron

## Usage

### Parse a Feed

```python
import feedparser

feed = feedparser.parse("https://example.com/feed.xml")
for entry in feed.entries[:10]:
    print(f"{entry.title} - {entry.link}")
    print(f"  Published: {entry.get('published', 'N/A')}")
```

### Monitor Multiple Feeds

```python
import feedparser, json, hashlib
from pathlib import Path

SEEN_FILE = Path("~/.openclaw/rss-seen.json").expanduser()

def load_seen():
    if SEEN_FILE.exists():
        return json.loads(SEEN_FILE.read_text())
    return {}

def save_seen(seen):
    SEEN_FILE.write_text(json.dumps(seen))

def check_feed(url, seen):
    feed = feedparser.parse(url)
    new_entries = []
    for entry in feed.entries:
        entry_id = hashlib.md5(entry.link.encode()).hexdigest()
        if entry_id not in seen.get(url, []):
            new_entries.append(entry)
            seen.setdefault(url, []).append(entry_id)
    return new_entries
```

### Cron Integration

Set up a cron job to check feeds periodically:
```
Schedule: every 2 hours
Payload: "Check RSS feeds and push new items"
```

## Dependencies

```bash
pip install feedparser
```

## Feed Sources Examples

| Source | Feed URL |
|--------|----------|
| Hacker News | https://hnrss.org/frontpage |
| TechCrunch | https://techcrunch.com/feed/ |
| ArXiv CS.AI | http://arxiv.org/rss/cs.AI |
| GitHub Trending | Use web scraping instead |

## Important Notes

- Some feeds require User-Agent headers
- Rate limit feed checks (don't poll more than every 15 minutes)
- Store seen entries persistently to survive restarts
