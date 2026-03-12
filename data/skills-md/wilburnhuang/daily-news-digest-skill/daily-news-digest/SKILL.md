---
name: daily-news-digest
description: Generate daily Tech & GNSS news digest blog posts for cheng-blog. Use when user asks to create a daily news digest, generate tech news, or mentions "/daily-news". Sources news from Bloomberg Tech YouTube channel (primary), with 3-day lookback for weekend coverage. Creates MDX posts with Tech News and GNSS News sections. GNSS news sourced from Inside GNSS, GPS World, and major company newsrooms (Trimble, Hexagon, Topcon, etc.).
---

# Daily Tech & GNSS News Digest Generator

Generate daily news digest blog posts sourced primarily from Bloomberg Tech YouTube channel.

## Workflow

### 1. Determine Target Date
- Use today's date for the digest title and filename
- For news content: prioritize today's news, but go back up to 3 days to cover weekends

### 2. Fetch Tech News from Bloomberg Tech

Search for Bloomberg Tech coverage using these queries:
```
Bloomberg Technology YouTube January [DAY] [YEAR]
Bloomberg Tech Asia January [YEAR]
Bloomberg Tech Europe January [YEAR]
```

**Source Priority:**
1. Bloomberg Tech (main US show) - primary source
2. Bloomberg Tech Asia - for Asian market/tech news
3. Bloomberg Tech Europe - for European tech news

**Date Priority:**
1. Today's episode - lead stories
2. Past 3 days - only HUGE news (major deals, IPOs, regulatory actions)

### 3. Fetch GNSS News

**Primary Sources (check first):**
1. **Inside GNSS** - insidegnss.com (industry-leading publication)
2. **GPS World** - gpsworld.com

**Company Newsrooms (check 2-3 with recent activity):**
- Trimble: investor.trimble.com/news-releases
- Hexagon: hexagon.com/company/newsroom
- Topcon: topconpositioning.com/news
- Quectel: quectel.com/news
- Swift Navigation: swiftnav.com/newsroom
- u-blox: u-blox.com/en/newsroom
- Septentrio: septentrio.com/en/company/news
- CHC Navigation: chcnav.com/news
- Unicorecomm: unicorecomm.com/news

**Efficient Search Strategy:**
```
# Start with aggregated industry news
site:insidegnss.com news [current month] [YEAR]
site:gpsworld.com news [current month] [YEAR]

# Then search for major company announcements
"GNSS" OR "positioning" news (Trimble OR Hexagon OR Topcon) [current month] [YEAR]
"precision navigation" OR "RTK" OR "PPP" announcement [current month] [YEAR]

# Only if needed - check specific company newsrooms
site:trimble.com news release [current month] [YEAR]
```

**Efficiency Rule:** Stop after finding 2-3 solid GNSS stories. Don't exhaustively check every company newsroom - prioritize Inside GNSS and GPS World as they aggregate industry news.

### 4. Generate Article

Create MDX file at: `src/content/posts/[YYYY-MM-DD]-daily-tech-gnss-news.mdx`

See [references/article-template.md](references/article-template.md) for structure.

**Tech News Section Structure:**
- Lead story (biggest news from today)
- 2-3 major stories (mix of today + huge news from past 3 days)
- Additional Headlines (bullet list of 3-5 smaller items)

**GNSS News Section Structure:**
- 1-2 full stories with context
- Focus on: autonomous vehicles, precision agriculture, GPS-denied navigation, new products

### 5. Commit (if requested)

Use commit message format:
```
feat: add daily tech & GNSS news digest for [DATE]
```

## Quality Guidelines

- Bold key figures (**$1 billion**, **6 gigawatts**)
- Include company names and specific numbers
- Attribute sources ("Bloomberg reports...", "According to...")
- Keep paragraphs concise (3-4 sentences max)
- Key Takeaways: exactly 3 bullet points summarizing main themes
