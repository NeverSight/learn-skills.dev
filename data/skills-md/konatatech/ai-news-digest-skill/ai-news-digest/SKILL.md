---
name: ai-news-digest
description: Automatically fetch, deduplicate, rank, and deliver AI news digests from multiple sources (Hacker News, TechCrunch, 机器之心, 量子位, etc.). Use this skill when the user wants to get AI news summaries, create daily/weekly AI briefings, or stay updated on AI developments. Supports email delivery, Markdown export, and Obsidian integration.
version: 1.0.0
author: Tsunagi
---

# AI News Digest Skill

## Overview

This skill automatically aggregates AI news from 8+ authoritative sources (both English and Chinese), intelligently deduplicates articles, ranks them by importance, and delivers formatted digests via email with Markdown attachments.

**Key Features:**
- 🌐 Multi-source aggregation (RSS-based, no scraping issues)
- 🧹 Smart deduplication (similarity detection)
- 📊 Intelligent ranking (heat score, recency, importance)
- 📧 Email delivery with HTML + Markdown attachment
- 📝 Auto-save to Obsidian vault
- ⏰ Flexible time ranges (hourly, daily, weekly)

## Quick Start

### Generate and Email Today's Digest
```bash
cd /data/workspace/TsunagiConfig/skills/ai-news-digest
python scripts/generate_digest.py
```

This will:
1. Fetch news from the past 24 hours
2. Deduplicate and rank articles
3. Generate HTML email + Markdown file
4. Send to your configured email
5. Save to Obsidian (if configured)

### Get Last 6 Hours of Breaking News
```bash
python scripts/generate_digest.py --hours 6
```

### Weekly Summary (Last 7 Days)
```bash
python scripts/generate_digest.py --days 7
```

## News Sources

| Source | Type | RSS Feed | Language |
|--------|------|----------|----------|
| Hacker News | Tech News | https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI | EN |
| TechCrunch AI | Industry | https://techcrunch.com/category/artificial-intelligence/feed/ | EN |
| The Verge AI | Consumer Tech | https://www.theverge.com/ai-artificial-intelligence/rss/index.xml | EN |
| OpenAI Blog | Official | https://openai.com/blog/rss.xml | EN |
| 机器之心 | Research | https://www.jiqizhixin.com/rss | CN |
| 量子位 | Industry | https://www.qbitai.com/feed | CN |
| AI科技评论 | Academic | (Custom RSS) | CN |
| 36氪AI | Business | (Custom RSS) | CN |

All sources use RSS feeds for stability (no web scraping SSL issues).

## Usage Examples

### 1. Manual One-Time Digest
```bash
# Default: last 24 hours, send email, save to Obsidian
python scripts/generate_digest.py

# Last 12 hours, no email
python scripts/generate_digest.py --hours 12 --no-email

# Last 3 days, custom output path
python scripts/generate_digest.py --days 3 --output ~/Desktop/ai_digest.md
```

### 2. Scheduled Daily Digest (Cron)
```bash
# Add to crontab: Daily at 8 AM
0 8 * * * cd /data/workspace/TsunagiConfig/skills/ai-news-digest && python scripts/generate_digest.py --hours 24
```

### 3. Use as Python Module
```python
from scripts.fetch_news import fetch_all_news
from scripts.process_news import deduplicate_and_rank

# Fetch news from last 48 hours
articles = fetch_all_news(hours=48)
print(f"Fetched {len(articles)} articles")

# Process and rank
top_articles = deduplicate_and_rank(articles, top_n=15)

# Generate Markdown
from scripts.generate_digest import format_markdown
markdown = format_markdown(top_articles)
print(markdown)
```

### 4. Email Only (No File Output)
```python
from scripts.generate_digest import send_digest_email

articles = [...]  # Your processed articles
send_digest_email(
    articles=articles,
    recipient="your@email.com",
    subject="AI News Digest - 2024-01-15"
)
```

## Configuration

### Email Settings (Optional)
Edit `config/email.json` if you want to add email delivery:
```json
{
  "smtp_host": "smtp.example.com",
  "smtp_port": 587,
  "sender": "your-email@example.com",
  "auth_code": "your-smtp-auth-code",
  "recipient": "recipient@example.com"
}
```

**Note:** Email functionality is optional. The skill works without it, generating Markdown reports only.

### News Sources
Edit `config/sources.json` to add/remove sources:
```json
{
  "sources": [
    {
      "name": "Hacker News",
      "url": "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI",
      "type": "api",
      "language": "en",
      "enabled": true
    },
    {
      "name": "机器之心",
      "url": "https://www.jiqizhixin.com/rss",
      "type": "rss",
      "language": "zh",
      "enabled": true
    }
  ]
}
```

### Obsidian Integration
Edit `config/obsidian.json`:
```json
{
  "vault_path": "/data/workspace/obsidian/Daily Notes",
  "enabled": true,
  "filename_format": "AI Digest - {date}.md"
}
```

## Output Format

### Markdown Structure
```markdown
# AI News Digest - 2024-01-15

**Time Range:** Last 24 hours  
**Total Articles:** 38 → 15 after deduplication  
**Generated:** 2024-01-15 08:00:00

---

## 🔥 Top Stories (Score ≥ 8.0)

### 1. OpenAI Announces GPT-5 with Multimodal Reasoning
- **Source:** OpenAI Blog | **Published:** 2 hours ago
- **Score:** 9.2/10 | **Category:** Product Launch
- **Summary:** OpenAI unveiled GPT-5, featuring advanced multimodal reasoning capabilities across text, images, and audio. The model shows significant improvements in complex problem-solving tasks.
- **Link:** [Read More](https://openai.com/blog/gpt-5-announcement)

---

## 📊 Industry News (Score 6.0-7.9)

### 2. Google DeepMind's AlphaFold 3 Predicts Protein Structures
...

---

## 🌏 Chinese AI Updates

### 8. 字节跳动发布新一代大模型"豆包Pro"
- **来源:** 量子位 | **发布:** 5小时前
...

---

## 📈 Statistics
- Total sources checked: 8
- Articles fetched: 38
- After deduplication: 15
- English articles: 10
- Chinese articles: 5
```

### Email HTML Format
- Clean, responsive HTML design
- Clickable headlines
- Category badges (🔥 Hot, 📊 Industry, 🌏 Chinese)
- Markdown file attached as `.md`

## Command-Line Options

```bash
python scripts/generate_digest.py [OPTIONS]

Options:
  --hours N          Time range in hours (default: 24)
  --days N           Time range in days (overrides --hours)
  --output PATH      Output Markdown file path
  --send-email       Send via email (default: true)
  --no-email         Skip email sending
  --save-obsidian    Save to Obsidian (default: true if configured)
  --top-n N          Number of top articles to include (default: 15)
  --min-score FLOAT  Minimum score threshold (default: 5.0)
  --debug            Enable debug logging
```

## Common Tasks

### Test News Fetching
```bash
python scripts/test_digest.py
```
Output:
```
✓ Fetched 16 articles from Hacker News
✓ Fetched 22 articles from 机器之心
✓ Total: 38 articles
✓ After deduplication: 15 articles
```

### Debug RSS Feed Issues
```python
from scripts.fetch_news import test_single_source

# Test a specific source
test_single_source("https://www.jiqizhixin.com/rss")
```

### Custom Scoring Algorithm
Edit `scripts/process_news.py`:
```python
def calculate_score(article):
    score = 0.0
    
    # Recency (0-3 points)
    hours_ago = (datetime.now() - article['published']).total_seconds() / 3600
    if hours_ago < 6:
        score += 3.0
    elif hours_ago < 24:
        score += 2.0
    else:
        score += 1.0
    
    # Keyword boost (0-4 points)
    hot_keywords = ['GPT', 'OpenAI', 'breakthrough', 'AGI']
    for keyword in hot_keywords:
        if keyword.lower() in article['title'].lower():
            score += 1.0
    
    # Source authority (0-3 points)
    authority_map = {
        'OpenAI Blog': 3.0,
        'Hacker News': 2.5,
        '机器之心': 2.5
    }
    score += authority_map.get(article['source'], 1.0)
    
    return min(score, 10.0)
```

## Troubleshooting

### Issue: No articles fetched
```bash
# Check internet connectivity
curl -I https://www.jiqizhixin.com/rss

# Test RSS parsing
python -c "import feedparser; print(feedparser.parse('https://www.jiqizhixin.com/rss'))"
```

### Issue: Email not sending
```bash
# Test email config
node /data/workspace/send_report_email.js

# Check SMTP credentials in config/email.json
```

### Issue: Too many duplicate articles
Adjust similarity threshold in `scripts/process_news.py`:
```python
SIMILARITY_THRESHOLD = 0.75  # Lower = stricter deduplication (default: 0.8)
```

## Quick Reference

| Task | Command | Time |
|------|---------|------|
| Daily digest | `python scripts/generate_digest.py` | ~10s |
| Breaking news (6h) | `python scripts/generate_digest.py --hours 6` | ~8s |
| Weekly summary | `python scripts/generate_digest.py --days 7` | ~15s |
| Test fetching | `python scripts/test_digest.py` | ~5s |
| Email only | `python scripts/generate_digest.py --no-obsidian` | ~10s |

## Installation

Before using this skill, install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `feedparser` - RSS feed parsing
- `beautifulsoup4` - HTML content extraction
- `requests` - HTTP requests
- `python-dateutil` - Date/time handling
- `numpy` - Similarity calculations

**System Requirements:**
- Python 3.8+
- Internet connection
- Optional: Node.js 14+ (for email sending via nodemailer)

## Next Steps

- For API reference and data structures, see `references/api_reference.md`
- For advanced customization, see `references/advanced_usage.md`
- To add new news sources, edit `config/sources.json`
- To integrate with other tools, use the Python module API

## License

MIT License - Free to use and modify