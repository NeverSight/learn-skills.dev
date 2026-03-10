---
name: seo-off-page-backlinks
description: Expert guide for off-page SEO and backlink analysis. Use when analyzing backlink profiles, assessing domain authority, planning link building strategies, evaluating link quality, identifying toxic backlinks, understanding anchor text distribution, or performing competitor backlink analysis.
---

# Off-Page SEO & Backlink Analysis

---

## Backlink Quality Assessment Framework

Not all backlinks are equal. Evaluate every backlink across these six dimensions before determining its value.

### Six Dimensions of Link Quality

| Dimension | Weight | What to Evaluate |
|-----------|--------|-----------------|
| **Relevance** | 25% | Is the linking site/page topically related to your content? |
| **Authority** | 20% | What is the linking domain's authority (DR/DA)? |
| **Placement** | 15% | Where on the page does the link appear? (editorial body > sidebar > footer) |
| **Anchor Text** | 15% | Is the anchor text descriptive, branded, or spammy? |
| **Follow Status** | 10% | Is the link dofollow, nofollow, sponsored, or UGC? |
| **Traffic** | 15% | Does the linking page receive organic traffic? |

### Relevance Hierarchy

Relevance is the most important factor. A link from a relevant DR 40 site often outperforms a link from an irrelevant DR 80 site.

```
Tier 1 (Best):  Same niche, same topic, same audience
Tier 2 (Good):  Related niche, overlapping audience
Tier 3 (OK):    General authority site (news, education, government)
Tier 4 (Weak):  Unrelated niche, no audience overlap
Tier 5 (Risk):  Completely irrelevant, different language, spammy vertical
```

### Placement Value

```
Highest:  In-content editorial link (surrounded by relevant text)
High:     Author bio on a relevant guest post
Medium:   Resource page / curated list
Low:      Sidebar widget or blogroll
Lowest:   Footer link, site-wide link, comment link
```

**MCP Tool:** Use `analyze_backlinks` with a target URL to retrieve the full backlink profile with per-link quality metrics.

---

## Domain Authority / Domain Rating

### What They Measure

| Metric | Provider | Scale | Based On |
|--------|----------|-------|----------|
| Domain Rating (DR) | Ahrefs | 0-100 | Quantity and quality of backlinks to the domain |
| Domain Authority (DA) | Moz | 0-100 | Link profile, MozRank, MozTrust, and other factors |
| Authority Score | Semrush | 0-100 | Backlinks, organic traffic, and spam signals |

### Interpretation Guide

| Score Range | Interpretation | Typical Sites |
|-------------|---------------|---------------|
| 80-100 | Elite authority | Google, Wikipedia, NYT, government domains |
| 60-79 | Very strong | Major brands, popular publications, large media |
| 40-59 | Strong | Established businesses, popular niche blogs |
| 20-39 | Moderate | Small businesses, newer sites with some traction |
| 10-19 | Low | New sites, small blogs, thin content sites |
| 0-9 | Very low | Brand new domains, parked domains, spam sites |

### Limitations (Important)

- DA/DR are **third-party estimates**, not Google metrics. Google does not use them.
- They can be manipulated (PBNs, link spam can inflate DR).
- A high-DR site with no relevance to your niche passes less real value than a moderate-DR relevant site.
- DR/DA do not account for page-level authority — a DR 70 site may have individual pages with zero backlinks.
- Always evaluate **page-level metrics** in addition to domain-level metrics.
- DR/DA can drop or rise due to tool recalculations, not actual link changes.

**MCP Tool:** Use `analyze_domain_authority` to retrieve DR/DA scores along with trust signals and spam indicators for any domain.

---

## Anchor Text Optimization

Anchor text distribution is a critical ranking signal and a common penalty trigger when over-optimized.

### Anchor Text Types

| Type | Definition | Example (for a page about "best running shoes") |
|------|-----------|------------------------------------------------|
| **Branded** | Company/site name | "Nike", "RunnerWorld.com" |
| **Exact-match** | Exact target keyword | "best running shoes" |
| **Partial-match** | Contains target keyword + other words | "guide to the best running shoes for beginners" |
| **Generic** | Non-descriptive text | "click here", "read more", "this article" |
| **Naked URL** | Raw URL as anchor | "https://runnerworld.com/best-shoes" |
| **Branded + keyword** | Brand combined with keyword | "RunnerWorld's best running shoes list" |
| **Image link** | Image used as link (alt text = anchor) | `<img alt="running shoes comparison chart">` |

### Ideal Anchor Text Distribution

Target these approximate ratios for a natural-looking profile:

| Anchor Type | Target % | Risk if Over-Indexed |
|-------------|----------|---------------------|
| Branded | 30-40% | Low risk |
| Naked URL | 15-20% | Low risk |
| Generic | 10-15% | Low risk |
| Partial-match | 10-15% | Medium risk if excessive |
| Branded + keyword | 5-10% | Medium risk |
| Exact-match | 3-8% | **High risk** if >10% |
| Image/other | 5-10% | Low risk |

### Red Flags

- Exact-match anchor text exceeding 10-15% of total profile
- Sudden spike of exact-match anchors (unnatural pattern)
- Identical anchor text from many different domains
- Anchor text in a foreign language on English-language pages
- Over-optimized anchors on footer/sidebar site-wide links

---

## Link Building Strategies Overview

### Strategy Comparison

| Strategy | Difficulty | Scalability | Link Quality | Time to Results |
|----------|-----------|-------------|-------------|-----------------|
| **Content marketing** (linkable assets) | Medium | High | High | 2-6 months |
| **Digital PR / data studies** | High | Medium | Very High | 1-3 months |
| **Broken link building** | Medium | Medium | Medium-High | 1-2 months |
| **Resource page outreach** | Low-Medium | Medium | Medium-High | 2-4 weeks |
| **HARO / journalist queries** | Medium | Low | Very High | 1-4 weeks |
| **Guest posting** | Low-Medium | Medium | Medium | 2-4 weeks |
| **Unlinked brand mentions** | Low | Low | High | 1-2 weeks |

### Content Marketing / Linkable Assets

Create content specifically designed to attract links:
- **Original research & data studies** — surveys, industry benchmarks, analysis
- **Comprehensive guides** — ultimate guides, definitive resources
- **Free tools & calculators** — interactive tools that solve problems
- **Infographics & visual assets** — data visualizations, comparison charts
- **Templates & frameworks** — downloadable resources others reference

### Digital PR

Combine data-driven content with journalist outreach:
1. Create original research or data analysis
2. Write a press release or pitch angle
3. Build a media list of relevant journalists/publications
4. Pitch the story with data, visuals, and expert quotes
5. Follow up and provide additional assets as requested

### Unlinked Brand Mentions

Find pages that mention your brand but do not link to you:
1. Search `"your brand" -site:yourdomain.com` in Google
2. Use Ahrefs Content Explorer or brand monitoring tools
3. Contact the site owner and request a link be added to the mention
4. Success rate is typically 10-20% (high, since they already know you)

See [LINK_BUILDING_PLAYBOOKS.md](LINK_BUILDING_PLAYBOOKS.md) for detailed step-by-step playbooks with outreach templates.

---

## Toxic Backlink Identification

Toxic backlinks can suppress your rankings or trigger manual actions. Identify them early.

### Quick Toxic Signals Checklist

| Signal | Severity |
|--------|----------|
| Link from a known PBN (private blog network) | High |
| Link from a site in a completely unrelated language | Medium-High |
| Link from a link farm (thousands of outbound links, no real content) | High |
| Exact-match anchor from low-quality directory | Medium |
| Sitewide footer/sidebar link from unrelated site | Medium |
| Link from a hacked or malware-flagged domain | High |
| Link from a site with DR 0-5 and no traffic | Low-Medium |
| Link from adult/gambling/pharma site (if unrelated to your niche) | High |
| Paid link with no `rel="sponsored"` attribute | High |
| Comment spam links | Low |

### PBN Detection Signals

- Multiple linking domains share the same IP address or hosting provider
- Thin content with no real audience or social presence
- Interlinking pattern between a cluster of small sites
- Recent domain registration with immediate high DR
- No branded search volume, no social profiles, no real business presence
- Content is AI-generated filler with links injected

See [TOXIC_LINK_PATTERNS.md](TOXIC_LINK_PATTERNS.md) for 20+ detailed toxic patterns with detection criteria and recommended actions.

---

## Competitor Backlink Gap Analysis

### Methodology

1. **Identify competitors** — select 3-5 direct SERP competitors for your target keywords
2. **Export backlink profiles** — pull referring domains for each competitor
3. **Find the gap** — identify domains that link to competitors but not to you
4. **Filter for quality** — remove low-authority, irrelevant, or toxic domains from the gap list
5. **Prioritize targets** — rank remaining domains by authority, relevance, and likelihood of linking
6. **Analyze link context** — understand why each site linked to your competitor (guest post, resource mention, editorial link)
7. **Create outreach plan** — develop a pitch that offers equal or better value to each target site

### Gap Analysis Framework

```
Your site:       example.com
Competitor A:    competitor-a.com    → 450 referring domains
Competitor B:    competitor-b.com    → 380 referring domains
Competitor C:    competitor-c.com    → 520 referring domains

Gap domains (link to 2+ competitors but not you):  85 domains
Filtered (DR 30+, relevant):                       42 domains
Priority targets:                                   15-20 domains
```

### Prioritization Criteria

| Factor | Weight |
|--------|--------|
| Links to 3+ competitors (not just one) | High priority |
| DR 40+ with real organic traffic | High priority |
| Topically relevant to your niche | Required |
| Resource page or "best of" list format | Easier outreach |
| Recently published or updated content | More likely to respond |

**MCP Tool:** Use `analyze_backlinks` on competitor domains to export their backlink profiles for gap analysis.

---

## Disavow File Creation

### When to Disavow

Disavow links **only** when:
- You have received a **manual action** from Google for unnatural links
- You have a clear history of paid/spammy link building that you cannot get removed
- You are seeing an obvious **negative SEO attack** with hundreds of toxic links

**Do NOT disavow** when:
- Links are simply low-quality but not spammy (Google ignores these)
- You are "cleaning up" a natural profile that has a few weak links
- A third-party tool flags links as "toxic" based only on low DA

### Disavow File Format

The disavow file is a plain text file (`.txt`) uploaded to Google Search Console.

```
# Disavow file for example.com
# Generated: 2026-02-26
# Reason: Manual action - unnatural inbound links

# Individual URLs to disavow
https://spamsite.com/page-with-link.html
https://another-spam.com/directory/listing.html

# Entire domains to disavow (use domain: prefix)
domain:linkfarm-network.com
domain:pbn-cluster-site.net
domain:cheap-directory-spam.org
```

### Google Disavow Tool Instructions

1. Go to [Google Disavow Links Tool](https://search.google.com/search-console/disavow-links)
2. Select your property
3. Upload the `.txt` disavow file
4. Google will process the file (may take weeks to take effect)
5. Resubmit a reconsideration request if you have a manual action

---

## Link Velocity

### Natural vs Unnatural Growth

| Pattern | Interpretation |
|---------|---------------|
| Gradual, steady increase over months | Natural — content gaining traction organically |
| Sudden spike followed by sustained plateau | Typical for viral content or major PR hit |
| Sudden spike followed by complete stop | Suspicious — possibly purchased links |
| Perfectly linear growth (same # of links per week) | Unnatural — automated or purchased |
| Burst of links from same C-class IP range | PBN or coordinated scheme |
| Seasonal spikes aligned with industry events | Natural — correlates with real-world activity |

### Guidelines

- New sites naturally acquire links slowly (5-20/month initially)
- Established sites may acquire hundreds per month organically
- A sudden 10x increase with no corresponding content or PR event is a red flag
- Link velocity should roughly correlate with content publishing velocity and brand visibility
- After a major content campaign, a spike is expected and natural

---

## Internal Link Equity Distribution

While internal linking is technically "on-page," its role in distributing link equity (PageRank) across your site is a critical off-page consideration.

### Principles

- **Link equity flows through internal links** — pages with strong backlink profiles should link to important pages that need a rankings boost
- **Deeper pages need internal links** — pages 3+ clicks from the homepage receive less crawled equity
- **Hub pages concentrate equity** — create pillar/hub pages that consolidate authority and distribute it to cluster pages
- **Limit outbound links per page** — equity is split among all links on a page; fewer outbound links = more equity per link
- **Fix broken internal links** — broken links waste equity and create dead ends

### Equity Flow Strategy

```
External backlinks → Homepage (high authority)
                   → Key landing pages
                   → Pillar content

Homepage → Pillar pages (via navigation + in-content links)
Pillar pages → Cluster/supporting pages (via contextual links)
Cluster pages → Related cluster pages + back to pillar (hub & spoke)
```

### Identifying Equity Distribution Problems

- **Orphan pages:** pages with zero internal links pointing to them
- **Equity hoarding:** important pages linked only from the homepage, not from other high-authority pages
- **Deep pages:** pages requiring 4+ clicks to reach from homepage
- **Link dilution:** pages with 200+ outbound links splitting equity too thin

---

## Related Skills

- **seo-on-page-optimization** — for on-page elements, meta tags, and content optimization
- **seo-technical-audit** — for crawlability, indexing, and Core Web Vitals
- **seo-content-strategy** — for creating linkable content assets
- **seo-mcp-tools-expert** — for advanced MCP tool usage

## Key MCP Tools for Off-Page SEO

| Tool | Use For |
|------|---------|
| `analyze_backlinks` | Full backlink profile analysis, competitor gap analysis, link quality scoring |
| `analyze_domain_authority` | DR/DA scores, trust signals, spam indicators |

See [LINK_QUALITY_SCORING.md](LINK_QUALITY_SCORING.md) for the detailed 6-dimension link scoring model.
See [LINK_BUILDING_PLAYBOOKS.md](LINK_BUILDING_PLAYBOOKS.md) for step-by-step playbooks with outreach templates.
See [TOXIC_LINK_PATTERNS.md](TOXIC_LINK_PATTERNS.md) for 20+ toxic backlink patterns with detection criteria.
