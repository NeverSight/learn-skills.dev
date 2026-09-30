---
name: rss-fetch
description: RSS feed API for fetching news and articles. Use when user mentions "RSS", "feed", "RSS reader", "fetch feed", or asks to get news from RSS sources.
---

## How to Use

### 1. Fetch Raw RSS Feed

```bash
curl -s "https://hnrss.org/frontpage" | head -100
```

### 2. Parse RSS with xmllint

Extract titles from RSS feed:

```bash
curl -s "https://hnrss.org/frontpage" | xmllint --xpath '//item/title/text()' - 2>/dev/null
```

Extract titles and links:

```bash
curl -s "https://hnrss.org/frontpage" | xmllint --format - | grep -E '<title>|<link>' | head -20
```

### 3. Get Items with Details

```bash
curl -s "https://hnrss.org/frontpage" | xmllint --xpath '//item' - 2>/dev/null | xmllint --format - | head -50
```

### 4. Parse Atom Feeds

Atom feeds use `<entry>` instead of `<item>`:

```bash
curl -s "https://github.com/blog.atom" | xmllint --xpath '//entry/title/text()' - 2>/dev/null
```

## Popular RSS Feeds

| Source | URL |
|--------|-----|
| Hacker News | `https://hnrss.org/frontpage` |
| HN Best | `https://hnrss.org/best` |
| TechCrunch | `https://techcrunch.com/feed/` |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/index` |
| The Verge | `https://www.theverge.com/rss/index.xml` |
| Reddit (any sub) | `https://www.reddit.com/r/programming/.rss` |
| GitHub Blog | `https://github.blog/feed/` |

## Examples

### Fetch Hacker News Top Stories

```bash
curl -s "https://hnrss.org/frontpage?count=10" | xmllint --xpath '//item/title/text()' - 2>/dev/null | tr '\n' '\n'
```

### Get Story Links

```bash
curl -s "https://hnrss.org/frontpage?count=5" | grep -oP '<link>\K[^<]+' | grep -v hnrss
```

### Fetch Multiple Feeds

```bash
FEEDS=(
  "https://hnrss.org/frontpage?count=5"
  "https://techcrunch.com/feed/"
)

for feed in "${FEEDS[@]}"; do
  echo "=== $feed ==="
  curl -s "$feed" | xmllint --xpath '//item/title/text()' - 2>/dev/null | head -5
  echo ""
done
```

### Extract Title, Link, and Date

```bash
curl -s "https://hnrss.org/frontpage?count=3" | xmllint --format - | awk '
  /<item>/ { in_item=1 }
  /<\/item>/ { in_item=0; print "---" }
  in_item && /<title>/ { gsub(/<[^>]*>/, ""); print "Title: " $0 }
  in_item && /<link>/ { gsub(/<[^>]*>/, ""); print "Link: " $0 }
  in_item && /<pubDate>/ { gsub(/<[^>]*>/, ""); print "Date: " $0 }
  '
```

### Save Feed to File

```bash
curl -s "https://hnrss.org/frontpage" -o /tmp/hn-feed.xml
xmllint --xpath '//item/title/text()' /tmp/hn-feed.xml
```

## HN RSS Options

Hacker News RSS (`hnrss.org`) supports parameters:

| Parameter | Description |
|-----------|-------------|
| `count=N` | Number of items (default 20) |
| `points=N` | Minimum points |
| `comments=N` | Minimum comments |
| `q=keyword` | Search keyword |

```bash
# Top stories with 100+ points
curl -s "https://hnrss.org/frontpage?points=100&count=10"

# Search for "AI" topics
curl -s "https://hnrss.org/frontpage?q=AI&count=10"
```

## RSS vs Atom Format

| Element | RSS | Atom |
|---------|-----|------|
| Container | `<item>` | `<entry>` |
| Title | `<title>` | `<title>` |
| Link | `<link>` | `<link href="...">` |
| Summary | `<description>` | `<summary>` |
| Date | `<pubDate>` | `<published>` |

## Guidelines

1. **Check feed format**: Use `head` first to see if it's RSS or Atom
2. **Use xmllint**: Best tool for XPath queries on XML
3. **Handle errors**: Some feeds may be slow or rate-limited
4. **Respect robots.txt**: Don't hammer feeds with requests
5. **Cache results**: Feeds don't update every second
