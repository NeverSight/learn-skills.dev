---
name: ahrefs-tool
description: When the user wants backlink analysis, link gap analysis, competitor link profiles, referring domain data, or link building research. Trigger on "backlinks," "who links to," "link profile," "referring domains," "link gap," "Ahrefs," "link building research," or "why do they outrank me" (often a link authority issue).
metadata:
  version: 1.0.0
  author: Garrett Smith
---

# Ahrefs Tool

> **Note:** LocalSEOData (`localseodata-tool`) now has `backlink_summary` and `backlink_gap` endpoints. Use LocalSEOData for quick backlink overviews and gap analysis. Ahrefs remains the preferred tool for deep link analysis — anchor text profiles, lost/new links, referring domain details, and content gap analysis.

Ahrefs has an official MCP server. When connected, use it for backlink analysis and link-focused competitive intelligence. Ahrefs has the largest backlink index — it's the authoritative source for link data.

## When to Use Ahrefs vs Other Tools

| You Need | Use Ahrefs | Use Instead |
|----------|-----------|-------------|
| Backlink profile for a domain | ✅ Best backlink database | — |
| Referring domains count/list | ✅ | — |
| Link gap (who links to competitor but not you) | ✅ Best for this | — |
| Lost/broken backlinks | ✅ | — |
| Anchor text analysis | ✅ | — |
| Keyword search volume | ⚠️ Can do it | Semrush (better keyword tool) |
| Keyword gap analysis | ⚠️ Can do it | Semrush (preferred for keywords) |
| Content Explorer (find linkable content) | ✅ Unique to Ahrefs | — |
| Technical site audit | ⚠️ Has one | Screaming Frog (more detailed) |
| SERP data | ❌ | SerpAPI |
| Local pack rankings | ❌ | Local Falcon |
| Citation data | ❌ | BrightLocal |

## Core Workflows

### Analyze a Business's Link Profile

**When:** User asks "why aren't we ranking?" or needs to understand link authority.

**What to pull:**
1. **Domain Rating (DR)**: Overall link authority score (0-100)
2. **Referring Domains**: Unique domains linking to the site (more important than total backlinks)
3. **Backlink list**: Individual backlinks with source, anchor text, follow/nofollow, first seen date
4. **Referring domains by DR**: Quality distribution of linking domains

**How to interpret for local:**
- DR 20-40: Typical for local businesses
- DR 40-60: Strong local site, likely has press or industry links
- DR 60+: Very strong, probably a brand or large multi-location
- Referring domains matter more than total backlinks (10 links from 10 domains > 50 links from 2 domains)
- Local relevance matters: 1 link from a local news site > 10 links from random blogs

**Red flags:**
- Sudden spike in referring domains (could be spam or negative SEO)
- Mostly nofollow links (limited authority transfer)
- Anchor text heavily keyword-stuffed (penalty risk)
- Links from irrelevant or low-quality sites

### Link Gap Analysis (Competitor vs You)

**When:** User wants to find link building opportunities from competitor profiles.

**What to pull:**
1. **Link Intersect**: Domains that link to competitors but NOT to user's site
2. Filter by DR 20+ (skip low-quality)
3. Filter by dofollow links
4. Sort by referring domain authority

**What to look for:**
- Local directories linking to competitors but not you → citation opportunity
- Local news/media sites → PR opportunity
- Industry associations or organizations → membership/sponsorship opportunity
- Local blogs or community sites → content/relationship opportunity
- .edu or .gov sites → high authority, worth extra effort

**How to prioritize opportunities:**
1. Local relevance (local site > random site)
2. Domain authority (DR 30+ preferred)
3. Dofollow status (dofollow > nofollow for SEO, but nofollow still has value)
4. Achievability (directory listings are easy, editorial links take effort)

### Lost Link Recovery

**When:** Rankings dropped and you suspect link loss, or routine maintenance.

**What to pull:**
1. **Lost backlinks** (filtered by recent timeframe)
2. Filter by referring domain DR 20+
3. Check if the linking page is gone (404) or the link was removed

**What to do:**
- Page 404'd → Reach out and ask to update the link
- Link removed → Understand why (content changed? contact changed?)
- Domain expired → Check if link was valuable enough to pursue alternative
- High-DR losses → Priority recovery targets

### Anchor Text Analysis

**When:** Checking for over-optimization or understanding link profile health.

**What healthy local anchor text looks like:**
- Brand name (40-60%): "Smith Plumbing," "smithplumbing.com"
- Generic (15-25%): "click here," "website," "learn more"
- Location-based (10-20%): "plumber in Buffalo," "Buffalo NY plumbing"
- Exact match keywords (under 10%): "emergency plumber" — too much of this is a penalty risk

### Content Explorer (Find Linkable Content Ideas)

**When:** User needs content ideas that attract links.

- Search for topics in your industry + location
- Find content that got the most links in your space
- Analyze what made it linkable (data, tools, guides, local research)
- Create something better for your market

## Key Metrics and What They Mean

| Metric | What It Is | Local SEO Context |
|--------|-----------|-------------------|
| Domain Rating (DR) | Ahrefs' authority score (0-100) | Compare to local competitors, not national brands |
| Referring Domains | Unique domains linking to you | The #1 link metric — more unique domains = more authority |
| URL Rating (UR) | Authority of a specific page | Useful for comparing location page authority |
| Dofollow % | Percentage of links passing authority | Below 50% dofollow is weak |
| Anchor text distribution | What text is used in links | Over-optimized anchors can trigger penalties |
| Link velocity | Rate of new links acquired | Steady growth is healthy, spikes are suspicious |

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Competitor has 3x more referring domains | Build a link acquisition strategy | `local-link-building` |
| Found link gap opportunities (directories) | These are citation opportunities | `local-citations` |
| Found link gap opportunities (editorial/media) | Build targeted outreach campaigns | `local-link-building` |
| Anchor text over-optimized | Diversify with brand and generic anchors going forward | `local-link-building` |
| Lost high-value links | Outreach to recover, then build replacements | `local-link-building` |
| Link profile is fine but still not ranking locally | Links aren't the issue — check GBP, reviews, proximity | `geogrid-analysis`, `gbp-optimization` |
| Need this data in a client report | Include link profile comparison in deliverables | `client-deliverables` |

**Default next step:** Link analysis always raises the question "is this a link problem or something else?" If the link profile is comparable to competitors, the issue is likely GBP, reviews, or relevance — not links.
